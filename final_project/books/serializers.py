from books.models import Book, Review, BookGenre, UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        user = UserSerializer()
        model = UserProfile
        exclude = ('books_view_hide_completed', 'reviews_view_hide_others', 'hide_others')

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        UserProfile = ProfileSerializer()
        model = Book
        fields = '__all__'

class BookGenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BookGenre
        fields = '__all__'

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        UserProfile = ProfileSerializer()
        book = BookSerializer()
        model = Review
        fields = '__all__'
