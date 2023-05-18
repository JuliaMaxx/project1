from django.shortcuts import render
from markdown import markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


# create a django form for searching entries
class SearchForm(forms.Form):
    entry = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search', 'autocomplete':'off'}), label="")

# create a dgango form for creating a new entry
class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}), label="")
    mdtext = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20, 'style': "height:300px", 'placeholder': 'MarkDown content'}))
    save = forms.CharField(widget=forms.TextInput(attrs={'type': 'submit','value': 'Save'}))

# create a django form for editing entries
class EditForm(forms.Form):
    mdtext = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 20, 'style': "height:300px"}))
    save = forms.CharField(widget=forms.TextInput(attrs={'type': 'submit','value': 'Save'}))


def index(request):
    # if user accessed website via GET
    if request.method == "GET":
        return render(request, "encyclopedia/index.html", {
            "form": SearchForm(),
            "entries": util.list_entries(),
            })
    # if user accessed website via POST
    else:
        form = SearchForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            # get the entry
            entry = form.cleaned_data["entry"]
            # get the list of all the entries
            entries = util.list_entries()
            # initilalize a list of all encyclopedia entries that have the query as a substring
            results = []
            # if typed in entry is not in the encyclopedia
            if entry not in entries:
                # check if given entry is a substring of existing entries
                for e in entries:
                    if entry in e:
                        results.append(e)
                # if there are search results - display them
                if results:
                    return render(request, "encyclopedia/search_results.html", {"form": SearchForm(), "entries": results})
                # if there are no search results - display 404 error
                else:
                    return render(request, "encyclopedia/error.html", {"form": SearchForm()})
            else:
                # if the entry is in the encyclopedia - redirect user to that entry's page
                return HttpResponseRedirect(f"/wiki/{entry}")


def search(request, entry):
    # get the list of all the entries
    entries = util.list_entries()
    # if given entry is in the list
    if entry in entries:
        # get the content of that entry
        md = util.get_entry(entry)
        # convert to html
        entry_content = markdown(md)
        # display entry's page
        return render(request, "encyclopedia/entry.html", {
            "form": SearchForm(),
            "entry": entry_content, "title":entry
        })
    else:
        # if not found - display 404 error
        return render(request, "encyclopedia/error.html", {"form": SearchForm()})
    
def new(request):
    # if the method is GET - display a form for creating new entry
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {"form": SearchForm(), "form1":NewEntryForm()})
    # if the method is POST
    else:
        form = NewEntryForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            # get the title of an entry
            title = form.cleaned_data["title"]
            # get MarkDown content
            md = form.cleaned_data["mdtext"]
            # get the list of all entries
            entries = util.list_entries()
            # if the title is already taken - alert the user about that
            if title in entries:
                return render(request, "encyclopedia/new.html", {"form": SearchForm(), "form1":NewEntryForm(), "taken":True})
            # if the title is not taken - save the new entry
            else:
                    util.save_entry(title, md)
                    return HttpResponseRedirect(f"/wiki/{title}")
            
def rand(request):
    # get the list of all the entries
    list = util.list_entries()
    # randomly choose one entry
    random_entry = random.choice(list)
    # redirectuser to that entry's page
    return HttpResponseRedirect(f"/wiki/{random_entry}")

def edit(request, entry):
    # get the content of the given entry
    content = util.get_entry(entry)
    info={'mdtext':content}
    # if the method is POST
    if request.method == 'POST':
        form = EditForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            # get new content for the entry
            new_content= form.cleaned_data['mdtext']
            # save the entry
            util.save_entry(entry, new_content)
            # redirect user to that entry's page
            return HttpResponseRedirect(f"/wiki/{entry}")
    # if the method is GET
    else:
        # prepopulate the textarea with the old content of the entry
        form = EditForm(initial=info)
        # display a form for editing to the user
        return render(request, "encyclopedia/edit.html", {"form": SearchForm(), "edit_form":form, "title":entry})


            