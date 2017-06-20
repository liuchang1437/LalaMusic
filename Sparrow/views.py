# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render

# Create your views here.
import json, pickle
from django.http import HttpResponse

from SearchEngine import dosearch

def search(request):
	stype = ''
	svalue = ''
	if 'type' in request.GET:
		stype = request.GET['type']
	if 'value' in request.GET:
		svalue = request.GET['value']
	items = {}
	if stype and stype=='Song/Singer':
		items = dosearch.dosearch(svalue)
		paginator = Paginator(items, 25) # Show 25 contacts per page
		page = request.GET.get('page')
		try:
			items = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			items = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			items = paginator.page(paginator.num_pages)
		return render(request, 'search.html', {'items': items})
	return render(request, 'search.html', {'items': items})

def play_song(request, song_id):
	return render(request, 'song.html')