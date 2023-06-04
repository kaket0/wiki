from cgitb import html
import re
from tkinter import Button
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.core.files.storage import default_storage
from random import choices

from . import util
from  markdown2 import markdown

class NewArticle(forms.Form):
    title = forms.CharField(label="Назва")
    textArticle = forms.CharField(label="", widget=forms.Textarea)
    # text_MD = forms.CharField(widget=forms.Textarea)
    
def list_md(filenames1):
    return list(sorted(re.sub(r"\.md$", "", filename)  for filename in filenames1 if filename.endswith(".md")))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    # file = f"entries/{title}.md"
    return render(request, "encyclopedia/wiki.html", {
        "article": markdown(util.get_entry(title)),
        "title": title
    })

def article(request):
    if request.method == "POST":
        form = NewArticle(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            # title = form.data["title"]
            # textArticle = form.data["textArticle"]
            textArticle = form.cleaned_data["textArticle"]
            if  not util.save_entry_new(title, textArticle):
                eror= f"Error save article - {title}.md. File exists!"
                return render(request, "encyclopedia/article.html",{
                "eror":eror,
                "NewArticle": form
                })
            else:
                return HttpResponseRedirect(f"wiki/{title}")
                # return render(request, "encyclopedia/wiki.html", {
                # "article":  markdown(util.get_entry(title)) 
                # }) 
    # return HttpResponseRedirect("wiki")
    return render(request, "encyclopedia/article.html", {
            "NewArticle": NewArticle()
        }) 

def search(request):
    q = str(request.GET['q'])
    # qq = request.GET
    filenames1 =[]
    _, filenames = default_storage.listdir("entries")
    for filename in filenames:
        if str(filename).lower() == (q + ".md").lower():
            return HttpResponseRedirect(f"wiki/{q}")
        if str(filename).lower().find(q.lower())!=-1:
            filenames1.append(filename)
    ls = list_md(filenames1)
    return render(request, "encyclopedia/search.html", {
        "entries": ls,
        "q": q
        })


def random(request):
    rardom = choices(util.list_entries(), k=1)
    return HttpResponseRedirect(f"wiki/{rardom[0]}")

def edit(request, title):
    if request.method == "GET":
        title = str(request.GET['title'])
        textArticle = util.get_entry(title) 
        default_data = {'title': title, 'textArticle': textArticle }
        form = NewArticle(default_data)
        # form.fields["title"].widget_attrs['readonly']= True
        form.fields["title"].widget.attrs['readonly'] = True
        return render(request,"encyclopedia/edit.html", {
            "form": form,
            "title":title
        
        }) 
       
    if request.method == "POST":
        form = NewArticle(request.POST)
        # form.fields["title"].editable = False
        form.fields["title"].widget.attrs['readonly'] = True
        if form.is_valid():
            title = form.cleaned_data["title"]
            textArticle = form.cleaned_data["textArticle"]
            util.save_entry(title, textArticle)
            return HttpResponseRedirect(f"/wiki/{title}")
        else:
            return render(request,"encyclopedia/edit.html", {
            
            "form": form,
            "title":title
            })
    # 
    # q1 = request.POST
    # file = f"entries/{article}.md"
    return render(request,"encyclopedia/edit.html", {
            
            "form": form,
            "title":title
        
        }) 