from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest
from markdown2 import Markdown

from . import util
from .forms import CreatePageForm

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


# TODO: Save markup data to file, upload to /entries directory
# Processes New Page Form data
def create_page(request):
    # If request is POST we need to process the data
    if request.method == "POST":
        # Create form instance and populate it with data from the request
        form = CreatePageForm(request.POST)

        # Check for validity
        if form.is_valid():
            # Check if new entry already exists in entry directory
            new_title = form.cleaned_data["entry_title"]
            if new_title.lower() in [entry.lower() for entry in util.list_entries()]:
               return HttpResponseBadRequest("Invalid request: duplicate entry found.")



            return redirect("index")

    # If GET or any other method, create blank form
    else:
        form = CreatePageForm()

    return render(request, "encyclopedia/createpage.html", {"form": form})