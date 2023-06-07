from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("predict", views.predict, name="predict"),
    path("visualize", views.visualize_view, name="visualize"),
    path("explore_tags", views.explore_tags, name="explore_tags"),

    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("register", views.register_user, name="register"),

    path("update_prediction/<int:prediction_id>/", views.update_prediction, name="update_prediction"),
    path("delete_prediction/<int:prediction_id>/", views.delete_prediction, name="delete_prediction"),

]
