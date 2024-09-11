from django.shortcuts import render
from django.http import Http404
from markdown2 import Markdown

from . import util


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