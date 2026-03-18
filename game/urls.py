from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path('', views.home, name='home'),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Game
    path("game/", views.home, name="home"),
    path("check/", views.check_solution, name="check"),
    path("hint/", views.hint, name="hint"),
    path("update_score/", views.update_score, name="update_score"),
    path("save_score/", views.save_score, name="save_score"),
    path("solve/", views.solve_board, name="solve"),

]
