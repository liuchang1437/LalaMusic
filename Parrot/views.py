# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
import time
# Create your views here.
from . import myacoustid
from SearchEngine import dosearch,songinfo_loader

def recognize(request):
    if request.method == "POST":   
        mp3file =request.FILES.get("mp3file", None)   
        if not mp3file:  
            messages.warning(request,"No file found.")
            return redirect('/recognize')
        filename = 'static/upload/{}-{}'.format(time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()),mp3file.name)
        destination = open(filename,'wb+')    
        for chunk in mp3file.chunks():      
            destination.write(chunk)  
        destination.close()  
        messages.success(request,"Upload successfully.")
        song = myacoustid.search_fp(filename)
        items = []
        for idx,_ in song:
            items.append(songinfo_loader.return_songinfo(idx))
        return render(request, 'search.html', {'items':items}) 
    return render(request, 'sound_hound.html')