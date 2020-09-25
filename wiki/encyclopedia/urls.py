from django.urls import path

from . import views     

urlpatterns = [
    path("", views.index, name="index"),  
    path("wiki/<title>", views.entry, name="entry"),    
    path ("add", views.add, name= "add"), 
    path ("create_page", views.create_page, name= "create_page"),
    path("random/", views.random_page, name="random"),
    path("search", views.search, name="search")     

]
