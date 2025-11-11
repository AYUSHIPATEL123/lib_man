from django.shortcuts import render,HttpResponse

def home(request):
    return HttpResponse("Library Management System \n version 1.0")