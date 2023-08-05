#!/usr/bin/env python3

from django.shortcuts import render, redirect
from django.contrib.auth import logout

def home(request):
    logout(request)
    return redirect("quiz:index") # redirect to your page
