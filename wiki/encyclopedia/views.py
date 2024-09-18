from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
from markdown2 import Markdown

from . import util


class Search(forms.Form):
    q = forms.CharField(label="", max_length=100)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Retrieves a wiki entry and renders it
def wiki(request, title):
    if title not in util.list_entries():
        raise Http404
    
    content = util.get_entry(title)
    return render(request, "encyclopedia/wiki.html",
                  {"title": title, "content":Markdown().convert(content)}
                  )


# Displays search results that contain user substrings
def results(request):
    searched = request.GET['q']
    if searched.upper() in (name.upper() for name in util.list_entries()):
        return redirect("wiki", name=searched)