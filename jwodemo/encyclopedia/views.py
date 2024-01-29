from django.shortcuts import render
import random
import markdown
from django.shortcuts import redirect
from . import util

def convert_md_to_html(title):
        content = util.get_entry(title)
        markdowner = markdown.Markdown()
        if content == None:
                return None
        else:
            return markdowner.convert(content)

def index(request):
        entries: util.list_entries()
        css_file = util.get_entry("CSS")
        coffee = util.get_entry("coffee")
        return render(request, "jworld/index.html", {
            "entries": util.list_entries()
        })

def entry(request, title):
        html_content = convert_md_to_html(title)
        if html_content == None:
                return render(request, "jworld/error.html", {
                       "message": "This entry does not exist"
                })
        else:
                return render(request, "jworld/entry.html", {
                       "title": title,
                       "content": html_content
                } )
        
def search(request):
       if request.method == "POST":
              entry_search = request.POST['q']
              html_content = convert_md_to_html(entry_search)
              if html_content is not None:
                return render(request, "jworld/entry.html", {
                       "title": entry_search,
                       "content": html_content
                } )    
              else:
                allEntries = util.list_entries()
                recommendation = []
                for entry in allEntries:
                        if entry_search.lower() in entry.lower():
                                recommendation.append(entry)
                return render(request, "jworld/search.html", {
                       "recommendation": recommendation
                })
              
from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    content = forms.CharField(label='Content', widget=forms.Textarea)

def new_page(request):
    if request.method == "GET":
        form = NewPageForm()
        return render(request, "jworld/new.html", {"form": form, "display_image": True})
    else:
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            
            # Check if title or content is blank
            if not title.strip() or not content.strip():
                return render(request, "jworld/error.html", {
                    "message": "Title or content cannot be blank."
                })

            title_exist = util.get_entry(title)
            if title_exist is not None:
                return render(request, "jworld/error.html", {
                    "message": "Entry page already exists"
                })
            else:
                util.save_entry(title, content)
                html_content = convert_md_to_html(title)
                return render(request, "jworld/entry.html", {
                    "title": title,
                    "content": html_content
                })
        else:
            # Form is not valid, render the form again with errors
            return render(request, "jworld/new.html", {"form": form, "display_image": True})
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "jworld/edit.html", {
            "title": title,
            "content": content,
            "display_image": True,  # Pass the display_image variable to the template
        })

       
def save_edit(request):
       if request.method == "POST":
              title = request.POST['title']
              content = request.POST['content']
              util.save_entry(title, content)
              html_content = convert_md_to_html(title)
              return render(request, "jworld/entry.html", {
                              "title": title,
                              "content": html_content
                       })
              

def rand(request):
    allEntries = util.list_entries()
    if not allEntries:
        return redirect('jworld')  # Assuming 'index' is the name of your encyclopedia index URL
    rand_entry = random.choice(allEntries)
    html_content = convert_md_to_html(rand_entry)
    return render(request, "jworld/entry.html", {
        "title": rand_entry,
        "content": html_content,
    })

def delete(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        util.delete_entry(title)
        return render(request, "jworld/deleted.html", {
            "title": title
        })
