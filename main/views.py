import datetime, json
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from main.models import Book_Entry, Book, Catalog_Entry
from main.forms import Book_EntryForm, Custom_EntryForm
from main.serializers import Book_EntrySerializer, BookSerializer, CustomSerializer
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from taggit.models import Tag

@login_required(login_url='/login')
def show_main(request):
    p = Paginator(Book.objects.all().order_by('pk'), 16)
    page = request.GET.get('page')
    book = p.get_page(page)
    if len(book[0].taggits.all()) == 0:
        adding_tag()
    tags = Tag.objects.all()

    context = {
        'name': request.user.username,
        'class': 'PBP KKI',
        'book': book,
        'tags': tags,
    }
    nums = "a" * book.paginator.num_pages
    return render(request, 'catalogue.html', context)

@login_required(login_url='/login')
def search_by_title(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        books = Book.objects.filter(name__contains = searched)
        book = Book.objects.filter(name__contains = searched).exists()

        return render(request, 'search_title.html',{'searched': searched, 'books': books, 'book': book, 'name': request.user.username})
    else:
        return render(request, 'catalogue.html', {'name': request.user.username})

def adding_tag():
    for book in Book.objects.all():
        list = tag_parser(book.tags)
        book.taggits.set(list, clear=True)

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
            messages.error(request, 'Invalid Username/Password')
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
    return [t.strip().capitalize() for t in tag_string.split(' ') if t.strip()]

def show_json(request):
    data = Book.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_books_by_id(request, id):
    book_item = Book.objects.get(pk=id)
    input = BookSerializer(book_item).data
    serialized_data = JSONRenderer().render(input).decode('utf-8')
    return JsonResponse({"result": "Success", "data": serialized_data})

class BookListAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

def get_books(request):
    data = Book.objects.all()
    input = JSONRenderer().render(BookSerializer(data, many=True).data)
    return HttpResponse(input, content_type="application/json")

def get_books_by_tag(request, tag):
    book = Book.objects.filter(taggits__name = tag).order_by('pk')
    input = JSONRenderer().render(BookSerializer(book, many=True).data)
    return HttpResponse(input, content_type="application/json")


def get_entry_by_id(request, id):
    data = Book_Entry.objects.get(pk = id)
    input = Book_EntrySerializer(data).data
    entry_content = JSONRenderer().render(input).decode('utf-8')
    if hasattr(data, "custom_entry"):
        book = data.custom_entry
    else:
        book = data.catalog_entry.book
    book_content = JSONRenderer().render(CustomSerializer(book).data).decode('utf-8')
    entry_dict = json.loads(entry_content)
    book_dict = json.loads(book_content)
    content = {**entry_dict, **book_dict}
    content_json = json.dumps(content)
    response_data = {
    "result": "Success",
    "data": content_json}
    return JsonResponse(response_data)

def edit_entry(request, id):
    entry = Book_Entry.objects.get(pk = id)

    form = Book_EntryForm(request.POST or None, instance=entry)

    if form.is_valid() and request.method == "POST":
        entry = form.save(commit= False)
        entry.last_read_date = datetime.datetime.now()
        entry.save()
        return HttpResponse(b"EDITED", status=201)

    return HttpResponseNotFound()

def show_json_by_id(request, id):
    data = Book_Entry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required(login_url='/login')
def show_book_entry(request):
    data = Book_Entry.objects.filter(user = request.user)
    context = {"book_entries": data,
               'name':request.user.username,
               'owner': request.user.username,
               'not_owner': "false",
               'is_owner':True
               }
    return render(request, "book_entry.html", context)

@login_required(login_url='/login')
def show_book_entry_other(request, username):
    user = User.objects.get(username = username)
    if user == request.user:
        return show_book_entry(request)
    data = Book_Entry.objects.filter(user = user)
    context = {"book_entries": data,
               'name':request.user.username,
               'owner': username,
               'not_owner': "true",
               'is_owner':False
               }
    return render(request, "book_entry.html", context)

@login_required(login_url='/login')
def show_users(request):
    display_user = User.objects.all()
    context = {'displayuser': display_user}
    return render(request, "user_display.html", context)

@login_required(login_url='/login')
def show_book_entry_by_id(request, id):
    data = Book_Entry.objects.select_related("catalog_entry").select_related("custom_entry").get(pk = id)
    context = {"entry": data}
    if hasattr(data, "catalog_entry"):
        book = data.catalog_entry.book
        context["book"] = book
    else:
        context["book"] = data.custom_entry
    
    return render(request, "book_entry_id.html", context)

@login_required(login_url='/login')
def create_custom_entry(request):
    form = Custom_EntryForm(request.POST or None)
    form_2 = Book_EntryForm(request.POST or None)
    print(form.is_valid())
    print(form_2.is_valid())
    if form.is_valid() and form_2.is_valid() and request.method == "POST":
        print("success")
        book_entry = form_2.save(commit=False)
        book_entry.user = request.user
        book_entry.last_read_date = datetime.datetime.now()
        custom_entry = form.save(commit=False)
        custom_entry.entry = book_entry
        book_entry.save()
        custom_entry.save()
        book = {
            "id" : book_entry.pk,
            "name": custom_entry.name,
            "type": custom_entry.type,
            "LCR" : book_entry.last_chapter_read
            }
        return JsonResponse(book)

    return HttpResponseNotFound()

@login_required(login_url='/login')
def create_catalog_entry(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        status = request.POST.get("status")
        last_chapter_read = request.POST.get("last_chapter_read")
        review = request.POST.get("review")
        rating = request.POST.get("rating")
        last_read_date = datetime.datetime.now()
        user = request.user
        book = Book.objects.get(name = name)

        new_entry = Book_Entry(status=status, last_chapter_read=last_chapter_read, review=review, rating=rating, last_read_date=last_read_date,user=user)
        new_entry.save()
        new_catalog_entry = Catalog_Entry(entry = new_entry, book = book)
        new_catalog_entry.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()


@csrf_exempt
def delete_entry(request, id):
    if request.method == 'POST':
        item = Book_Entry.objects.get(pk = id)
        item.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

