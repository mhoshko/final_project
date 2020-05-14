"""final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from books import views
from rest_framework import routers
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'books', views.BookViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'book-genre', views.GenreViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('join/', views.join, name='join'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('reviews/', views.reviews, name='reviews'),
    path('books/', views.books, name='books'),
    path('add_book/', views.add_book, name='add_book'),
    path('add_review/', views.add_review, name='add_review'),
    # path('profile/', views.profile, name='profile'),
    path('createProfile/', views.createProfile, name='createProfile'),
    path('profile/<username>/', views.profile, name='profile'),
    path('api/v1/', include(router.urls)),
    path('api-auth/v1/', include('rest_framework.urls', namespace='rest_framework')),
    path('reviews/edit_review/<int:id>/', views.edit_review, name='edit_review')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
