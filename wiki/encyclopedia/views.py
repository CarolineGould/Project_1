from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import random

from . import util

class EntryForm(forms.Form):
    entry_title = forms.CharField(label="New Entry Title")
    entry_text =  forms.CharField(widget=forms.Textarea)    

class SearchForm(forms.Form):
    search_title = forms.CharField()

class EditForm(forms.Form):
    edit_title: forms.CharField()
    edit_text:  forms.CharField(widget=forms.Textarea(attrs={"class" : "content"}))

mark = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/notfound.html",  {
            "title": title
        
        })

    return render(request, "encyclopedia/entry.html", {
        "title": title, 
        "content": mark.convert(content)
    })

def add (request):
    return render  (request, "encyclopedia/add.html", {
        "form": EntryForm()

    })

def create_page (request):
    already_exists = False
    form= EntryForm(request.POST)
    if _check_if_title_exists (form ["entry_title"].value()):
        already_exists = True
    if form.is_valid() and already_exists == False:
        util.save_entry(form ["entry_title"].value(),form ["entry_text"].value() )
        
        return HttpResponseRedirect("wiki/" + form ["entry_title"].value())
    return render (request, "encyclopedia/add.html", {
        "form": form, 
        "already_exists" : already_exists

    })

def _check_if_title_exists (title):
    existing_entries = util.list_entries() 
    for existing_title in existing_entries:
        if title == existing_title:
            return True
    return False

def random_page(request):
    entries = util.list_entries() 
    selected_page = random.choice(entries)
    return HttpResponseRedirect(reverse('entry', args=[selected_page]))

def search (request):
    entries = util.list_entries() 
    form= SearchForm(request.POST)
    search_title  = form ["search_title"].value()
    if util.get_entry(search_title):
        return HttpResponseRedirect(reverse ('entry', args= [search_title]))
    result = filter(lambda title: title.find(search_title) != -1, entries) 
    return render (request, "encyclopedia/search.html", {
       "entries": result
    })

def edit_page(request, title):
    edit=EditForm(initial={"edit_title": name, "edit_text": util.get_entry(name)})
    return render(request, "encyclopedia/edit.html", {
        "edit": EditForm(),
        "content" : util.get_entry(title)
    })