from django import forms
from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from books.models import Review, Book, UserProfile, BookGenre

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'books_view_hide_completed', 'reviews_view_hide_others']

class ReviewForm(ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'size': '150'}))
    class Meta:
        model = Review
        exclude = ['UserProfile', 'book']

class BookForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'size': '100'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    class Meta:
        model = Book
        exclude = ['UserProfile']

class AddBookForm(ModelForm):
    title = forms.ModelChoiceField(queryset=Book.objects.all().order_by('title'))
    class Meta:
        model = Book
        fields = ['title']

class HideCompletedBooksForm(ModelForm):
    books_view_hide_completed = forms.BooleanField(required=False, label='Hide Completed Books',widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit()'}))
    class Meta:
        model = UserProfile
        fields = ['books_view_hide_completed']
        labels = {
            'books_view_hide_completed': 'Hide Completed Books'
        }

class HideOtherReviewsForm(ModelForm):
    reviews_view_hide_others = forms.BooleanField(required=False, label='Show Only Your Reviews',widget=forms.CheckboxInput(attrs={'onclick': 'this.form.submit()'}))
    class Meta:
        model = UserProfile
        fields = ['reviews_view_hide_others']
        labels = {
            'reviews_view_hide_others': 'Show Only Your Reviews'
        }


class JoinForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

class LoginForm(Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
