from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('about-us/', views.AboutUsView.as_view(), name="about-us"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('jobs/', views.JobsView.as_view(), name="jobs"),

    path('register/', views.RegisterView.as_view(), name="register"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('manage_account/', views.ManageAccountView.as_view(), name="manage_account"),
    path('my_offers/', views.MyOffersView.as_view(), name="my_offers"),

    path('offer/<str:pk>/', views.OfferView.as_view(), name="offer"),
    path('create_offer/', views.CreateOfferView.as_view(), name="create_offer"),
]
