from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^item/create', views.Create_item_Form.as_view() , name="create_item"),
    url(r'^item/show/(\d+)', views.show_item , name="show_item"),
    url(r'^item/search_results', views.search_results , name="search_results"),
    url(r'^item/search', views.search_item_Form.as_view() , name="search_item"),
    url(r'^item/delete/(\d+)', views.delete_item , name="delete_item"),
    url(r'^item/edit/(?P<pk>\d+)', views.ItemUpdate.as_view() , name="edit_item"),
]
