import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.urls import reverse
from main.models import Book_Entry, Book, Catalog_Entry
from main.serializers import Book_EntrySerializer
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from taggit.models import Tag

@login_required(login_url='/login')
def show_main(request):
    entries = Book.objects.all()
    p = Paginator(Book.objects.all(), 30)
    page = request.GET.get('page')
    book = p.get_page(page)
    tags = Tag.objects.all()

    context = {
        'name': request.user.username,
        'class': 'PBP KKI',
        'book': book,
        'tags': tags,
    }
    nums = "a" * book.paginator.num_pages
    return render(request, 'catalogue.html', context)

def search_by_title(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(name__contains = searched)

        return render(request, 'templates/catalogue.html',{'searched': searched, 'books': books})
    else:
        return render(request, 'templates/catalogue.html',{})


def show_catalog(request):
    p = Paginator(Book.objects.all(), 30)
    page = request.GET.get('page')
    book_entries = p.get_page(page)

    context = {
        'name': request.user.username,
        'class': 'PBP KKI',
        'book_entries': book_entries,
    }

    return render(request, 'catalogue.html', context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return redirect('main:login')

def tag_parser(tag_string):
    translation = tag_string.maketrans('\'[,]','    ')
    tag_string = tag_string.translate(translation)
    print(tag_string)
    return [t.strip().capitalize() for t in tag_string.split(' ') if t.strip()]

def show_json(request):
    data = Book_Entry.objects.all()
    input = Book_EntrySerializer(data, many = True).data
    return HttpResponse(input, content_type="application/json")

def show_json_by_id(request, id):
    data = Book_Entry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_book_entry(request):
    data = Book_Entry.objects.filter(user = request.user)
    context = {"book_entries": data}
    return render(request, "book_entry.html", context)


def show_book_entry_by_id(request, id):
    data = Book_Entry.objects.select_related("catalog_entry").select_related("custom_entry").get(pk = id)
    context = {"entry": data}
    if hasattr(data, "catalog_entry"):
        book = data.catalog_entry.book
        context["book"] = book
    else:
        context["book"] = data.custom_entry
    
    return render(request, "book_entry_id.html", context)
        


