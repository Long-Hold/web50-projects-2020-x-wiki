from django.shortcuts import render, redirect
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


# Displays search results that contain user substrings
def results(request):
    searched = request.GET.get("q", "")
    entries = util.list_entries()

    if searched in entries:
        return redirect("wiki", title=searched)
    
    # If an entry contains the search as a substring, redirect to results page
    queries = [_ for _ in util.list_entries() if searched.upper() in _.upper()]
    return render(request, "encyclopedia/results.html", {
        "queries": queries,
        "searched": searched
    })

