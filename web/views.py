from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from json import dumps, loads
from web.models import *
from web.forms import IcdForm,UserForm,UserProfileForm
from web.hardware_control import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



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
                return HttpResponseRedirect('/web/tfa_stub')
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

def tfa_stub(request):

    context_dict = {}

    return render(request, 'web/tfa_stub.html',context_dict)

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
