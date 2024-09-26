from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseBadRequest
from markdown2 import Markdown

from . import util
from .forms import CreatePageForm, EditEntryForm

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
            new_body = form.cleaned_data["entry_body"]

            # If an entry already exists, inform the user
            if new_title.lower() in [entry.lower() for entry in util.list_entries()]:
                form.add_error("entry_title", "A page with this title already exists.")
                return render(request, "encyclopedia/createpage.html", {"form": form})

            # Prepend the title to the body text to act as a header when the .md file is loaded
            header = f"# {new_title} \n\n"
            final_body = header + new_body

            util.save_entry(new_title, final_body)
            return redirect("wiki", title=new_title)

    # If GET or any other method, create blank form
    else:
        form = CreatePageForm()

    return render(request, "encyclopedia/createpage.html", {"form": form})


# Retrieves the markdown contents and displays them
# On a page where they can be edited by the user
def edit(request, title):
    # If the user has decided to submit their editted page
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            edited_form = form.cleaned_data["entry_body"]
            util.save_entry(title, edited_form)
            return redirect("wiki", title=title)
    
    else:
        entry_content = util.get_entry(title)
        form = EditEntryForm(initial={"entry_body": entry_content})
    
    return render(request, "encyclopedia/edit.html", {"title": title, "form": form})
