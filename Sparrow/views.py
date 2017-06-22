# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render
import os

# Create your views here.
import json, pickle
from django.http import HttpResponse

from SearchEngine import dosearch,songinfo_loader
from operator import itemgetter
def hsort(items, user_history):
	n = len(items)
	if not user_history:
		return items
	pos = 0
	for item in items:
		pos = pos + 1
		item['sid'] = pos
		if item['SongID'] in user_history:
			if pos >= n/2:
				item['sid'] = pos - (8*pos/n - 3) * user_history[item['SongID']]
			else:
				item['sid'] = pos - (2*pos-2)/(n-2) * user_history[item['SongID']]
	sort_by_pos = sorted(items,key=itemgetter('sid'))
	return sort_by_pos


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
		# sort according to history
		if request.user.is_authenticated():
			user_history = {}
			if os.path.isfile('static/user_history/{}.json'.format(request.user.id)):
				f = open('static/user_history/{}.json'.format(request.user.id), 'r', encoding="utf-8")
				user_history = json.load(f)
			items = hsort(items, user_history)
		# end sort
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
	if stype and stype=='Lyrics':
		items = dosearch.dosearch_lyric(svalue)
		# sort according to history
		if request.user.is_authenticated():
			user_history = {}
			if os.path.isfile('static/user_history/{}.json'.format(request.user.id)):
				f = open('static/user_history/{}.json'.format(request.user.id), 'r', encoding="utf-8")
				user_history = json.load(f)
			items = hsort(items, user_history)
		for item in items:
			item['Highlights'] = item['Highlights'].replace('\n','<br>')
		# end sort
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
	song_info = songinfo_loader.return_songinfo(song_id)
	if request.user.is_authenticated():
		user_history = {}
		if os.path.isfile('static/user_history/{}.json'.format(request.user.id)):
			f = open('static/user_history/{}.json'.format(request.user.id), 'r', encoding="utf-8")
			user_history = json.load(f)
			f.close()
		if song_id in user_history:
			user_history[song_id] = user_history[song_id] + 1
		else:
			user_history[song_id] = 1
		with open('static/user_history/{}.json'.format(request.user.id), 'w') as f:
			json.dump(user_history, f)

	return render(request, 'song.html', {'song_info':song_info})