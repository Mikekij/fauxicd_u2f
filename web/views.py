from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from json import dumps, loads
from web.models import *
from web.forms import IcdForm
#from hardware_contol.app import * #not sure how to effectively import these functions.


#app homepage
def index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for demo
    context_dict = {'icd_list': icd_list}

    return render(request, 'web/index.html',context_dict)

def icd_index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for demo

    context_dict = {'icd_list': icd_list}

    return render(request, 'web/icd_index.html',context_dict)


#icd views
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
                return redirect('icd_index')
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
    message = "Shock Handler goes Here"
    context_dict = {'message': message}

    return HttpResponse(dumps(context_dict))
