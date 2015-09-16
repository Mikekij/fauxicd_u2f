from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.template import RequestContext
from json import dumps, loads
from web.models import *
from web.forms import IcdForm,UserForm,UserProfileForm, NewTfaRegistrationForm, NewTfaAuthenticationForm
from web.hardware_control import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
import os

from u2flib_server import u2f_v2 as u2f

#app homepage
def index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for demo
    context_dict = {'icd_list': icd_list}

    return render(request, 'web/index.html',context_dict)


#user views
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else: #invalid form
            print user_form.errors, profile_form.errors
    else: #not a POST
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
        'web/register.html',
        {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
        )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/web/new_tfa_registration')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'web/login.html', {})


### U2F Registration
def new_tfa_registration(request):

    #tfa_registration = TfaRegistration()

    #u2f ||= U2F::U2F.new(request.base_url)

    #registration_requests = @u2f.registration_requests

    # Store challenges. We need them for the verification step
    #session[:challenges] = @registration_requests.map(&:challenge)

    # Fetch existing Registrations from your db and generate SignRequests
    #key_handles = TfaRegistration.all.map(&:key_handle)
    #sign_requests = u2f.authentication_requests(key_handles)

    APP_ID = 'https://dev.medcrypt.com:8000'
    #APP_ID = 'https://' + request.get_host()

    registrationRequest = u2f.start_register(APP_ID)

    new_tfa_registration_form = NewTfaRegistrationForm(request.POST)

    context_dict = {'app_id': APP_ID, 'registrationRequest': registrationRequest, 'new_tfa_registration_form': new_tfa_registration_form}

    #registration_requests =

    return render(request, 'web/new_tfa_registration.html',context_dict)


def create_tfa_registration(request):
    current_user = request.user
    response = request.POST["response"]
    original_request = request.POST["original_request"]

    print "Request data: " + original_request
    print "Response data: " + response

    result = u2f.complete_register(original_request, response)
    print "result: " + str(result[0])

    if result:
        #pass
        tfa_registration = TfaRegistration(key_handle = result[0]['keyHandle'], public_key = result[0]['publicKey'], user_id = current_user.id, last_authenticated_at = datetime.now())
        tfa_registration.save()

        print "pass path"
        context_dict = {'result': str(result[0]), 'response': response}
        return render(request, 'web/create_tfa_registration.html',context_dict)
    else:
        #fail
        context_dict = {'result': str(result[0]), 'response': response}
        return render(request, 'web/create_tfa_registration.html',context_dict)

###authentication_requests
def new_tfa_authentication(request):
    current_user = request.user

    #tfa_registration = TfaRegistration()

    #u2f ||= U2F::U2F.new(request.base_url)

    #registration_requests = @u2f.registration_requests

    # Store challenges. We need them for the verification step
    #session[:challenges] = @registration_requests.map(&:challenge)

    # Fetch existing Registrations from your db and generate SignRequests
    #key_handles = TfaRegistration.all.map(&:key_handle)
    #sign_requests = u2f.authentication_requests(key_handles)

    APP_ID = 'https://dev.medcrypt.com:8000'

    #APP_ID = 'https://' + request.get_host()
    tfa_registration = TfaRegistration.objects.get(user_id = current_user.id)
    start_data = {}
    start_data['keyHandle'] = str(tfa_registration.key_handle)
    start_data['appId'] = APP_ID

    sign_request = u2f.start_authenticate(start_data)

    new_tfa_authentication_form = NewTfaAuthenticationForm(request.POST)

    context_dict = {'sign_request': sign_request, 'new_tfa_authentication_form': new_tfa_authentication_form}

    return render(request, 'web/new_tfa_authentication.html',context_dict)


def create_tfa_authentication(request):
    current_user = request.user
    response = request.POST["response"]
    original_request = request.POST["original_request"]

    print "Request data: " + original_request
    print "Response data: " + response

    APP_ID = 'https://dev.medcrypt.com:8000'

    #APP_ID = 'https://' + request.get_host()
    tfa_registration = TfaRegistration.objects.get(user_id = current_user.id)
    start_data = {}
    start_data['keyHandle'] = str(tfa_registration.key_handle)
    start_data['appId'] = APP_ID
    start_data['publicKey'] = str(tfa_registration.public_key)


    result = u2f.verify_authenticate(start_data, original_request, response)
    print "result: " + str(result[0])

    if result:
        print "pass path"
        context_dict = {'result': str(result), 'response': response}
        return render(request, 'web/create_tfa_registration.html',context_dict)
    else:
        #fail
        print "fail path"
        context_dict = {'result': str(result), 'response': response}
        return render(request, 'web/create_tfa_registration.html',context_dict)




@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/web/')

def users(request):
    user_list = User.objects.all() #set the list of Users. Should return only one for demo

    context_dict = {'user_list': user_list}

    return render(request, 'web/users.html',context_dict)

def show_user(request, id=None):
    #is this a get?
    if request.method == 'GET':
        if id:
            user = User.objects.get(id=id)
        else:
            user = None
    else:
        return redirect('users')

    context_dict = {'user': user}
    return render(request, 'web/show_user.html', context_dict)

def edit_user(request, id=None, template_name='web/edit_user.html'):

    #do we have an id?
    if id:
        user = User.objects.get(id=id)
        profile = user.userprofile

        #is this a post?
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=user)
            profile_form = UserProfileForm(request.POST, instance=profile)

            #is it valid?
            if user_form.is_valid() and profile_form.is_valid():
                #save it
                user_form.save(commit=True)
                profile_form.save(commit=True)

                #redirect to index
                return redirect('users')
            else:
                print user_form.errors and profile_form.errors
        else: #if this is a GET
            #render the form
            user_form = UserForm(instance=user)
            profile_form = UserProfileForm(instance=profile)
    else:   #no id in request
        return redirect('users')

    context_dict = {'user_form': user_form, 'profile_form': profile_form, 'user': user, 'profile': profile}
    return render(request, 'web/edit_user.html', context_dict)

#icd views
def icd_index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for demo

    context_dict = {'icd_list': icd_list}

    return render(request, 'web/icd_index.html',context_dict)

def show_icd(request, id=None):
    #is this a get?
    if request.method == 'GET':
        if id:
            icd = Icd.objects.get(id=id)
        else:
            icd = None
    else:
        return redirect('icd_index')

    context_dict = {'icd': icd}
    return render(request, 'web/icd.html', context_dict)

def add_icd(request):
    #is this a post?
    if request.method == 'POST':
        form = IcdForm(request.POST)

        #is it valid?
        if form.is_valid():
            #save it
            form.save(commit=True)

            #redirect to index
            return redirect('icd_index')
        else:
            print form.errors
    else:
        #render the form
        form = IcdForm()

    return render(request, 'web/add_icd.html', {'form': form})

def edit_icd(request, id=None, template_name='web/edit_icd.html'):

    #do we have an id?
    if id:
        this_icd = Icd.objects.get(id=id)
        #is this a post?
        if request.method == 'POST':
            form = IcdForm(request.POST, instance=this_icd)

            #is it valid?
            if form.is_valid():
                #save it
                form.save(commit=True)

                #redirect to index
                return redirect(this_icd.get_absolute_url())
            else:
                print form.errors
        else: #if this is a GET
            #render the form
            form = IcdForm(instance=this_icd)

    else:   #no id in request
        return redirect('icd_index')

    context_dict = {'form': form, 'this_icd': this_icd}
    return render(request, 'web/edit_icd.html', context_dict)

def deliver_shock_page(request):
    context_dict = {}

    return render(request, 'web/deliver_shock_page.html',context_dict)

def deliver_shock_ajax(request):
    if request.user.is_authenticated():
        message = test_handler(None)
    else:
        message = "Gotta log in, dude."

    context_dict = {'message': message}

    return HttpResponse(dumps(context_dict))

def test_api_call(request):
    message = test_handler(None)
    data = {'message': message}

    return HttpResponse(dumps(data), content_type='application/json')
