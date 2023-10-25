from django.urls import path
from main.views import show_main, register, login_user, logout_user, show_json, show_json_by_id, show_book_entry_by_id, search_by_title, show_book_entry

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
    path('entry/', show_book_entry , name='show_entry')
]