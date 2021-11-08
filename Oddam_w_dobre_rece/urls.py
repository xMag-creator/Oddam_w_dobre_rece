"""Oddam_w_dobre_rece URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from give_to_good_hands.views import LandingPageView, AddDonationView, LoginView, RegisterView, LogoutView, \
    ConfirmationView, UserProfilView, ChangeDonationStatusView, EditUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('add_donation/', AddDonationView.as_view(), name='add_donation'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('confirmation/', ConfirmationView.as_view(), name='confirmation'),
    path('user_profil/', UserProfilView.as_view(), name='user_profil'),
    path('change_donation_status/<int:pk>/', ChangeDonationStatusView.as_view(), name='change_donation_status'),
    path('edit_user/', EditUserView.as_view(), name='edit_user'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
