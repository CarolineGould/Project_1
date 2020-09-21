from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util

class EntryForm(forms.Form):
    entry_title = forms.CharField(label="New Entry Title")
    entry_text =  forms.CharField(widget=forms.Textarea)

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
    form= EntryForm(request.POST)
    if form.is_valid():
        return HttpResponseRedirect(reverse("index"))
    return render (request, "encyclopedia/add.html", {
        "form": form
    })