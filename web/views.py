from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from web.models import *

def index(request):
    text = "Hey now!"
    context_dict = {'text': text}

    return render(request, 'web/index.html',context_dict)

def icd_index(request):
    icd_list = Icd.objects.all() #set the list of ICDs. Should return only one for dmeo

    context_dict = {'icd_list': icd_list}

    return render(request, 'web/icd_index.html',context_dict)
