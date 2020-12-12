from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("list", views.list, name="list"),
    path("list_page/<str:name>", views.list_page, name="list_page"),
    path("category", views.category_list, name="category_list"),
    path("category/<str:category>", views.category, name="category"),
    path("bid", views.bid, name="bid"),
    path("comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_watchlist",views.remove_watchlist, name="remove_watchlist"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("delete/<int:id_num>>", views.delete, name="delete")
]
