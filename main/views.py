import datetime, json, requests
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse
from main.models import Book_Entry, Book, Catalog_Entry, Custom_Entry, Post, BookPost, Profile
from main.forms import Book_EntryForm, Custom_EntryForm
from main.serializers import Book_EntrySerializer, BookSerializer, CustomSerializer, BookPostSerializer
from rest_framework.generics import ListAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from taggit.models import Tag
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

types = ["All","Manga","Manhwa","Light Novel","Novel"]
@login_required(login_url='/login')
def show_main(request):
    p = Paginator(Book.objects.all().order_by('pk'), 16)
    page = request.GET.get('page')
    book = p.get_page(page)
    if len(book[0].taggits.all()) == 0:
        adding_tag()
    tags = Tag.objects.all()

    context = {
        'types': types,
        'name': request.user.username,
        'class': 'PBP KKI',
        'book': book,
        'tags': tags,
        'taggits' :tags
    }
    return render(request, 'catalogue.html', context)

@login_required(login_url='/login')
def search_by_title(request):
        searched = request.GET.get('searched')
        if searched == None:
            return render(request, 'catalogue.html', {'searched': searched})
        else:
            books = Book.objects.filter(name__contains = searched)
            book = Book.objects.filter(name__contains = searched).exists()
            tags = Tag.objects.all()
            p = Paginator(books.order_by('pk'), 16)
            page = request.GET.get('page')
            currPage = p.get_page(page)

            return render(request, 'search_title.html',{'searched': searched, 'books': books, 'book': book, 'name': request.user.username, "tags": tags,'currPage':currPage, 'types':types, 'taggits' :tags})

def adding_tag():
    for book in Book.objects.all():
        list = tag_parser(book.tags)
        book.taggits.set(list, clear=True)

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            person = form.save()
            profile = Profile(user = person)
            profile.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        elif User.objects.filter(username = request.POST.get('username')).exists():
            messages.error(request, 'Username already in use')
        else:
            messages.error(request, 'Invalid Password')
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
    p = Paginator(Book.objects.filter(taggits__name=tag).order_by('pk'), 16)
    page = request.GET.get('page')
    book = p.get_page(page)
    tags = Tag.objects.all()
    context = {
        'types': types,
        'tags': tags,
        'book': book,
        'name': request.user.username,
        'taggits' :tags
    }

    return render(request, 'catalogue.html', context)

def get_books_by_type(request, type):
    if type == "All":
        return show_main(request)
    p = Paginator(Book.objects.filter(type = type).order_by('pk'), 16)
    page = request.GET.get('page')
    book = p.get_page(page)
    tags = Tag.objects.all()
    context = {
        'types': types,
        'tags': tags,
        'book': book,
        'name': request.user.username,
        'taggits' :tags
    }

    return render(request, 'catalogue.html', context)

def get_entry_by_id(request, id):
    data = Book_Entry.objects.get(pk = id)
    input = Book_EntrySerializer(data).data
    entry_content = JSONRenderer().render(input).decode('utf-8')
    if hasattr(data, "custom_entry"):
        book = data.custom_entry
        book_content = JSONRenderer().render(CustomSerializer(book).data).decode('utf-8')
    else:
        book = data.catalog_entry.book
        book_content = JSONRenderer().render(BookSerializer(book).data).decode('utf-8')
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

class Book_EntryList(APIView):
    def get(self, request):
        book_entries = Book_Entry.objects.filter(user = request.user)
        serializer = Book_EntrySerializer(book_entries, many=True)
        return Response(serializer.data)

def fetch_tags(request):
    print(request.user)
    data = Tag.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type = "application/json")
    
class Book_Catalog(APIView):
    def get(self, request):
        catalog_books = Book.objects.all()
        serializer = BookSerializer(catalog_books, many=True)
        return Response(serializer.data)
    
@login_required(login_url='/login')
def show_book_entry(request):
    data = Book_Entry.objects.filter(user = request.user)
    taggits = Tag.objects.all()
    context = {"book_entries": data,
               'name': request.user.username,
               'owner': request.user,
               'not_owner': "false",
               'is_owner':True,
               'user': request.user,
               'taggits': taggits
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
               'owner': user,
               'not_owner': "true",
               'is_owner':False,
               'user': request.user
               }
    return render(request, "book_entry.html", context)

@login_required(login_url='/login')
def show_users(request):
    display_user = User.objects.all()
    tags = Tag.objects.all()
    bookPosts = BookPost.objects.all()
    posts = Post.objects.all()
    context = {'displayuser': display_user, 'name': request.user.username, 'user':request.user, 'posts': posts, 'taggits' :tags, 'bookPosts': bookPosts}
    return render(request, "user_display.html", context)

@login_required(login_url='/login')
def create_custom_entry(request):
    form = Custom_EntryForm(request.POST or None)
    form_2 = Book_EntryForm(request.POST or None)
    if form.is_valid() and form_2.is_valid() and request.method == "POST":
        list = request.POST.getlist('tag')
        book_entry = form_2.save(commit=False)
        book_entry.user = request.user
        book_entry.last_read_date = datetime.datetime.now()
        custom_entry = form.save(commit=False)
        custom_entry.entry = book_entry
        book_entry.save()
        custom_entry.save()
        if custom_entry.imagelink:
            extension = custom_entry.imagelink[-4:]
            extension1 = custom_entry.imagelink[-5:]
            if extension != ".jpg" and extension != ".gif" and extension != ".png" and extension1 != ".jpeg":
                custom_entry.imagelink = "/static/logos.png"
        else:
            custom_entry.imagelink = "/static/logos.png"
        custom_entry.save()
        custom_entry.taggits.set(list, clear=True)
        if book_entry.status == "P":
            status = "Plan to Read"
        elif book_entry.status == "O":
            status = "On hold"
        elif book_entry.status == "D":
            status = "Dropped"
        elif book_entry.status == "F":
            status = "Finished"
        else:
            status = "Reading"
        if book_entry.rating == None:
            rating = '-'
        else:
            rating = "" + str(book_entry.rating) + "/10"
        book = {
            "id" : book_entry.pk,
            "name": custom_entry.name,
            "type": custom_entry.type,
            "status" : status,
            "imagelink" : custom_entry.imagelink,
            "author" : custom_entry.author,
            "rating" : rating
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
        if rating == '':
            rating = None
        if last_chapter_read == '':
            last_chapter_read = None
        notes = request.POST.get("notes")
        last_read_date = datetime.datetime.now()
        user = request.user
        book = Book.objects.get(name = name)

        new_entry = Book_Entry(status=status, last_chapter_read=last_chapter_read, review=review, rating=rating, last_read_date=last_read_date,user=user, notes = notes)
        new_entry.save()
        new_catalog_entry = Catalog_Entry(entry = new_entry, book = book)
        new_catalog_entry.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@login_required(login_url='/login')
def copy_entry(request):
    if request.method == 'POST':
        id = request.POST.get("pk")
        status = request.POST.get("status")
        last_chapter_read = request.POST.get("last_chapter_read")
        review = request.POST.get("review")
        rating = request.POST.get("rating")
        notes = request.POST.get("notes")
        last_read_date = datetime.datetime.now()
        user = request.user
        og_book_entry = Book_Entry.objects.get(pk = id)
        new_entry = Book_Entry(status=status, last_chapter_read=last_chapter_read, review=review, rating=rating, last_read_date=last_read_date,user=user, notes = notes)
        new_entry.save()
        if hasattr(og_book_entry, "custom_entry"):
            book = og_book_entry.custom_entry
            book.pk = None
            book.entry = new_entry
            book.save()
        else:
            book = og_book_entry.catalog_entry.book
            catalog_entry = Catalog_Entry(entry = new_entry, book = book)
            catalog_entry.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@login_required(login_url='/login')
def delete_user(request, username):
    username = User.objects.filter(username=username)
    username.delete()
    return HttpResponseRedirect(reverse('main:show_other_users'))

@login_required(login_url='/login')
def make_admin(request, username):
    username = User.objects.get(username=username)
    username.is_staff = True
    username.save()
    return HttpResponseRedirect(reverse('main:show_other_users'))

@login_required(login_url='/login')
def revoke_admin(request, username):
    username = User.objects.get(username=username)
    username.is_staff = False
    username.save()
    return HttpResponseRedirect(reverse('main:show_other_users'))

def dummy(request, wow):
    return HttpResponseNotFound()

@csrf_exempt
def delete_entry(request, id):
    if request.method == 'POST':
        item = Book_Entry.objects.get(pk = id)
        item.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

@login_required(login_url='/login')
def create_post(request):
    if request.method == "POST":
        tag = request.POST.get("tag")
        user = request.user
        new_tag = Post(user=user, tag=tag)
        new_tag.save()
        
        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

@login_required(login_url='/login')
def create_book_post(request):
    if request.method == "POST":
        user = request.user
        name = request.POST.get("name")
        imagelink = request.POST.get("imagelink")
        type = request.POST.get("type")
        author = request.POST.get("author")
        description = request.POST.get("description")
        
        if imagelink:
            extension = imagelink[-4:]
            extension1 = imagelink[-5:]
            if extension != ".jpg" and extension != ".gif" and extension != ".png" and extension1 != ".jpeg":
                imagelink = "/static/logos.png"
        else:
            imagelink = "/static/logos.png"
        
        new_book = BookPost(user=user, name=name, imagelink = imagelink, type = type, author = author, description = description)
        new_book.save()
        list = request.POST.getlist('book_tag')
        new_book.taggits.set(list, clear=True)
        
        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()


@login_required(login_url='/login')
@csrf_exempt
def reject_tag(request, id):
    if request.method == "POST":
        tag = Post.objects.get(pk = id)
        tag.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

@login_required(login_url='/login')
@csrf_exempt
def accept_tag(request, id):
    if request.method == "POST":
        post = Post.objects.get(pk = id)
        tag = Tag(name = post.tag)
        tag.save()
        post.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

@login_required(login_url='/login')
@csrf_exempt
def reject_book(request, id):
    if request.method == "POST":
        book = BookPost.objects.get(pk = id)
        book.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

@login_required(login_url='/login')
@csrf_exempt
def accept_book(request, id):
    if request.method == "POST":
        book = BookPost.objects.get(pk = id)
        real_book = Book(name = book.name, imagelink = book.imagelink, type = book.type, author = book.author, description = book.description)
        real_book.save()
        real_book.taggits.set(book.taggits.all(), clear = True) 
        
        book.delete()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

@login_required(login_url='/login')
def get_posts_json(request):
    item = Post.objects.all()
    return HttpResponse(serializers.serialize('json', item, use_natural_foreign_keys=True))

@login_required(login_url='/login')
def get_bookposts_json(request):
    item = BookPost.objects.all()
    return HttpResponse(serializers.serialize('json', item, use_natural_foreign_keys=True))

@login_required(login_url='/login')
def get_book_posts_json(request, id):
    item = BookPost.objects.get(pk = id)
    input = BookPostSerializer(item).data
    serialize_data = JSONRenderer().render(input).decode("utf-8")
    return JsonResponse({"result": "Success", "data": serialize_data})

@login_required(login_url='/login')
@csrf_exempt
def make_favourite(request, id):
    if request.method == "POST":
        profile = Profile.objects.get_or_create(user = request.user)
        profile = profile[0]
        profile.favourite = Book_Entry.objects.get(pk=id)
        profile.save()
        return HttpResponse(b"DELETED", status = 201)
    return HttpResponseNotFound()

@csrf_exempt
def create_custom_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print(data["name"])
        print(data["author"])
        print(data["type"])
        print(data["imagelink"])
        print(data["description"])
        print(data["taggits"])
        print(data["status"])
        print(data["lastChapterRead"])
        print(data["notes"])
        print(data["review"])
        print(data["rating"])
        imagelink = data["imagelink"]
        list = data["taggits"]
        if imagelink:
            extension = imagelink[-4:]
            extension1 = imagelink[-5:]
            if extension != ".jpg" and extension != ".gif" and extension != ".png" and extension1 != ".jpeg":
                imagelink = "/static/logos.png"
        else:
            imagelink = "/static/logos.png"
        print(imagelink)
        new_entry = Book_Entry.objects.create(
            user = request.user,
            status = data["status"],
            last_chapter_read = data["lastChapterRead"],
            last_read_date = datetime.datetime.now(),
            review = data["review"],
            notes = data["notes"],
            rating = data["rating"],
        )
        new_entry.save()
        new_book = Custom_Entry.objects.create(
            entry = new_entry,
            name = data["name"],
            author = data["author"],
            type = data["type"],
            imagelink = imagelink,
            description = data["description"],
        )

        new_book.save()
        new_book.taggits.set(list, clear=True)
        print(new_book)
        print(new_entry)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)
    
@csrf_exempt
def create_catalog_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print(data["id"])
        print(data["status"])
        print(data["lastChapterRead"])
        print(data["notes"])
        print(data["review"])
        print(data["rating"])
        new_entry = Book_Entry.objects.create(
            user = request.user,
            status = data["status"],
            last_chapter_read = data["lastChapterRead"],
            last_read_date = datetime.datetime.now(),
            review = data["review"],
            notes = data["notes"],
            rating = data["rating"],
        )
        new_entry.save()
        new_catalog_entry = Catalog_Entry.objects.create(
            entry = new_entry,
            book = Book.objects.get(id = data["id"])
        )

        new_catalog_entry.save()
        print(new_catalog_entry)
        print(new_entry)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def edit_entry_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print(data["id"])
        print(data["status"])
        print(data["lastChapterRead"])
        print(data["notes"])
        print(data["review"])
        print(data["rating"])
        entry = Book_Entry.objects.get(id = data["id"])
        entry.status = data["status"]
        entry.last_chapter_read = int(data["lastChapterRead"])
        entry.last_read_date = datetime.datetime.now()
        entry.review = data["review"]
        entry.notes = data["notes"]
        entry.rating = int(data["rating"])
        entry.save()
        print(entry)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

@csrf_exempt
def delete_entry_flutter(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        print(data["id"])
        entry = Book_Entry.objects.get(id = data["id"])
        entry.delete()
        print(entry)

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

class Other_Users(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer_user = json.loads(serializers.serialize("json", users))
        return Response(serializer_user)

        book_entries = Book_Entry.objects.filter(user = request.user)
        serializer = Book_EntrySerializer(book_entries, many=True)
        return Response(serializer.data)

class Book_EntryList_Flutter(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        book_entries = Book_Entry.objects.filter(user = user)
        serializer = Book_EntrySerializer(book_entries, many=True)
        return Response(serializer.data, status=200)

class Make_Admin_Flutter(APIView):
    def post(self, request, username):
        username = User.objects.get(user = username)
        username.is_staff = True
        username.save()
        return JsonResponse({"status": "success"}, status=200)         

class Revoke_Admin_Flutter(APIView):
    def post(self, request, username):
        username = User.objects.get(username=username)
        username.is_staff = False
        username.save()
        return JsonResponse({"status": "success"}, status=200)    

class Delete_User_Flutter(APIView):
    def post(self, request, username):
        username = User.objects.get(username=username)
        username.delete()
        return JsonResponse({"status": "success"}, status=200)     


