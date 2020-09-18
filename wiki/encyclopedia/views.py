from django.shortcuts import render
from markdown2 import Markdown

from . import util

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

