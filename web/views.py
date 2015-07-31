from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from web.models import *
from web.forms import IcdForm
#from hardware_contol.app import * #not sure how to effectively import these functions.

def index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for demo
    context_dict = {'icd_list': icd_list}

    return render(request, 'web/index.html',context_dict)

def icd_index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for demo

    context_dict = {'icd_list': icd_list}

    return render(request, 'web/icd_index.html',context_dict)

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

def edit_icd(request, id=None, template_name='web/add_icd.html'):
    #do we have an id?
    if id:
        icd =
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
        else: #if this is a GET
            #render the form
            form = IcdForm()

    else:   #no id in request
        return redirect('icd_index')

    return render(request, 'web/add_icd.html', {'form': form})

def deliver_shock(request):
    context_dict = {}

    return render(request, 'web/deliver_shock.html',context_dict)
