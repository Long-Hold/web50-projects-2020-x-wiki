from django import forms


# Class responsible for rendering Create Page Form
class CreatePageForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title", max_length=50)
    entry_body = forms.CharField(widget=forms.Textarea, label="")


# This class simply displays a pre-populated text-area
# Using an existing entries markdown content
class EditEntryForm(forms.Form):
    entry_body = forms.CharField(widget=forms.Textarea, label="")