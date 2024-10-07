from django.urls import path
from .views import *

urlpatterns = [
   path("entries/add/", add_entry, name='add-entry'),
   path("entries/list/", list_entries, name="list-entries")
]