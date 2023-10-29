from django.urls import path
from main.views import show_main, register, login_user, logout_user, show_json, show_json_by_id, show_book_entry_by_id, search_by_title, show_book_entry, create_custom_entry, create_catalog_entry, BookListAPIView, get_entry_by_id, edit_entry, show_book_entry_other
from main.views import get_books_by_id, delete_entry, get_books, get_books_by_tag, show_users, delete_user, copy_entry, get_posts_json, reject_tag, create_post, accept_tag
app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('json/', show_json, name='show_json'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'),
    path('search_title', search_by_title, name='search-title'),
    path('entry/<int:id>/', show_book_entry_by_id , name='show_entry_by_id'),
    path('entry/', show_book_entry , name='show_entry'),
    path('create-custom-entry/', create_custom_entry, name = 'create_custom_entry' ),
    path('create-catalog-entry/', create_catalog_entry, name = "create_catalog_entry"),
    path('BookAPIView/', BookListAPIView.as_view(), name = "BookAPIView"),
    path('get-books-by-id/<int:id>', get_books_by_id, name='get_books_by_id'),
    path('get-books/', get_books, name='get_books'),
    path('get-books/<str:tag>', get_books_by_tag, name='get_books_by_tag'),
    path('get-entry-by-id/<int:id>', get_entry_by_id, name = "get_entry_by_id"),
    path('edit-entry/<int:id>', edit_entry, name = "edit_entry"),
    path('entry/<str:username>', show_book_entry_other , name='show_entry_other'),
    path('delete-entry/<int:id>', delete_entry, name = "delete_entry"),
    path('show-other-users/', show_users, name="show_other_users"),
    path('delete-user/<str:username>', delete_user, name='delete_user'),
    path('create-post/', create_post, name='create_post'),
    path('copy-entry/', copy_entry, name='copy_entry'),
    path('get-posts/', get_posts_json, name='get_posts_json'),
    path('reject-tag/<int:id>', reject_tag, name='reject_tag'),
    path('accept-tag/<int:id>', accept_tag, name='accept_tag'),
]
