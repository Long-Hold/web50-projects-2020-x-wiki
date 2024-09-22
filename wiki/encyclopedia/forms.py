from django import forms


# Class responsible for rendering Create Page Form
class CreatePageForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title", max_length=50)
    entry_body = forms.CharField(widget=forms.Textarea, label="")