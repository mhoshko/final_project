from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from books.forms import LoginForm, JoinForm, BookForm, ReviewForm, HideCompletedBooksForm, ProfileForm, AddBookForm, HideOtherReviewsForm, HideOthers, SearchUsersForm
from rest_framework import permissions
from books.models import Book, Review, UserProfile, BookGenre
from books.serializers import BookSerializer, BookGenreSerializer, UserSerializer, ReviewSerializer, ProfileSerializer


def checkAuth(request):
    if(request.user.is_authenticated):
        return True
    else:
        return False

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    num_pages = 0
    num_pages_overall = 0
    profile = UserProfile.objects.get(user=request.user)

    if request.method == "POST":
        profile = UserProfile.objects.get(user=request.user)
        completed_form = HideOthers(request.POST, instance=profile)
        if(completed_form.is_valid()):
            completed_form.save()

    try:
        profile = UserProfile.objects.get(user=request.user)
        is_hidden = HideOthers(instance=profile)
    except:
        is_hidden = HideOthers()
    hidden_checked = is_hidden['hide_others'].value()
    if hidden_checked:
        books_completed = Book.objects.filter(UserProfile=profile, completed=True).count()
        books_pending = Book.objects.filter(UserProfile=profile, completed=False).count()
        recommended = Review.objects.filter(UserProfile=profile, recommendation=True).count()
        not_recommended = Review.objects.filter(UserProfile=profile, recommendation=False).count()
        stars = list(Review.objects.filter(UserProfile=profile).values_list('stars', flat=True))

    else:
        books_completed = Book.objects.filter(completed=True).count()
        books_pending = Book.objects.filter(completed=False).count()
        recommended = Review.objects.filter(recommendation=True).count()
        not_recommended = Review.objects.filter(recommendation=False).count()
        stars = list(Review.objects.values_list('stars', flat=True))

    pages_read = list(Book.objects.select_related().filter(UserProfile=profile).values_list('length', flat=True))
    for page in pages_read:
        num_pages += page
    pages_read_overall = list(Book.objects.select_related().values_list('length', flat=True))
    for page in pages_read_overall:
        num_pages_overall += page

    context = {
        "books_completed": books_completed,
        "books_pending": books_pending,
        "stars": stars,
        "recommended": recommended,
        "is_hidden": is_hidden,
        "num_pages": num_pages,
        "num_pages_overall": num_pages_overall,
        "hidden_checked": hidden_checked,
        "not_recommended": not_recommended,
        "profile": profile,
        "is_user": checkAuth(request),
    }
    return render(request, 'index.html', context=context)

@login_required(login_url='/login/')
def reviews(request):
    if (not BookGenre.objects.all()):
        BookGenre.objects.create(genre="Romance")
        BookGenre.objects.create(genre="Mystery")
        BookGenre.objects.create(genre="Fantasy and Science Fiction")
        BookGenre.objects.create(genre="Thrillers and Horror")
        BookGenre.objects.create(genre="Young Adult")
        BookGenre.objects.create(genre="Children's Fiction")
        BookGenre.objects.create(genre="Inspirational, Self-Help, and Religious")
        BookGenre.objects.create(genre="Biography, Autobiography, and Memoir")

    if request.method == "POST":
        profile = UserProfile.objects.get(user=request.user)
        completed_form = HideOtherReviewsForm(request.POST, instance=profile)
        if(completed_form.is_valid()):
            completed_form.save()

    try:
        profile = UserProfile.objects.get(user=request.user)
        is_hidden = HideOtherReviewsForm(instance=profile)
    except:
        is_hidden = HideOtherReviewsForm()
    hidden_checked = is_hidden['reviews_view_hide_others'].value()
    if hidden_checked:
        profile = UserProfile.objects.get(user=request.user)
        my_reviews = Review.objects.filter(UserProfile=profile)
    else:
        profile = UserProfile.objects.get(user=request.user)
        try:
            my_reviews = Review.objects.all()
        except:
            my_reviews = None

    #my_reviews = Review.objects.all()
    my_books = Book.objects.all()
    context = {
        "is_user": checkAuth(request),
        "user": request.user,
        "reviews": my_reviews,
        'is_hidden': is_hidden,
        "profile": profile,
        "books": my_books,
    }
    return render(request, 'reviews.html', context=context)


@login_required(login_url='/login/')
def add_review(request):
    profile = UserProfile.objects.get(user=request.user)
    my_books = Book.objects.exclude(UserProfile=profile)
    if request.method == 'POST':
        form_1 = BookForm(request.POST)
        form_instance = ReviewForm(request.POST)
        if(form_instance.is_valid() and form_1.is_valid()):
            title = form_1.cleaned_data["title"]
            genre = form_1.cleaned_data["genre"]
            author = form_1.cleaned_data["author"]
            length = form_1.cleaned_data["length"]
            completed = form_1.cleaned_data["completed"]
            bk = Book.objects.create(title=title, genre=genre, author=author, length=length, completed=completed)
            bk.UserProfile.add(profile)

            description = form_instance.cleaned_data["description"]
            stars = form_instance.cleaned_data["stars"]
            recommendation = form_instance.cleaned_data["recommendation"]
            readability = form_instance.cleaned_data["readability"]
            rev = Review.objects.create(UserProfile=profile, description=description, stars=stars, recommendation=recommendation, readability=readability, book=bk)

            return HttpResponseRedirect('../reviews')
    else:
      form_1 = BookForm()
      form_instance = ReviewForm()
    context = {
            'books': my_books,
            "form": form_instance,
            "profile": profile,
            "user": request.user,
            "form1": form_1,
            "is_user": checkAuth(request),
    }
    return render(request, 'add_review.html', context=context)



@login_required(login_url='/login/')
def edit_review(request, id):
    profile = UserProfile.objects.get(user=request.user)
    review = Review.objects.get(id=id)
    if(request.method=='POST'):
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return HttpResponseRedirect("../../")
    else:
        review_form = ReviewForm(instance=review)
    context = {
        "form": review_form,
        "user": request.user,
        "profile": profile,
        "is_user": checkAuth(request),
    }
    return render(request, 'edit_review.html', context=context)



@login_required(login_url='/login/')
def books(request):
    if (not BookGenre.objects.all()):
        BookGenre.objects.create(genre="Romance")
        BookGenre.objects.create(genre="Mystery")
        BookGenre.objects.create(genre="Fantasy and Science Fiction")
        BookGenre.objects.create(genre="Thrillers and Horror")
        BookGenre.objects.create(genre="Young Adult")
        BookGenre.objects.create(genre="Children's Fiction")
        BookGenre.objects.create(genre="Inspirational, Self-Help, and Religious")
        BookGenre.objects.create(genre="Biography, Autobiography, and Memoir")
    val = request.GET.get('toggle_completed', 0)
    if val != 0:
        book = Book.objects.get(id=val)
        book.completed = not book.completed
        book.save()
    delete = request.GET.get('delete', 0)
    if delete != 0:
        Book.objects.filter(id=delete).delete()
        return redirect('/books/')

    if request.method == "POST":
        profile = UserProfile.objects.get(user=request.user)
        completed_form = HideCompletedBooksForm(request.POST, instance=profile)
        if(completed_form.is_valid()):
            completed_form.save()
    try:
        profile = UserProfile.objects.get(user=request.user)
        is_hidden = HideCompletedBooksForm(instance=profile)
    except:
        is_hidden = HideCompletedBooksForm()
    hidden_checked = is_hidden['books_view_hide_completed'].value()
    if hidden_checked:
        profile = UserProfile.objects.get(user=request.user)
        my_books = Book.objects.filter(UserProfile=profile, completed=False)
    else:
        profile = UserProfile.objects.get(user=request.user)
        try:
            my_books = Book.objects.filter(UserProfile=profile)
        except:
            my_books = None
    context = {
        'books': my_books,
        "profile": profile,
        'is_hidden': is_hidden,
        "is_user": checkAuth(request),
    }
    return render(request, 'books.html', context=context)


@login_required(login_url='/login/')
def add_book(request):
    profile = UserProfile.objects.get(user=request.user)
    my_books = Book.objects.exclude(UserProfile=profile)
    if request.method == 'POST':
        form_instance = AddBookForm(request.POST)
        if(form_instance.is_valid()):
            instance = form_instance.save(commit=False)
            book = Book.objects.get(title=instance.title)
            book.UserProfile.add(profile)

            context = {
                    'books': my_books,
                    "form": form_instance,
                    "is_user": checkAuth(request),
            }
            return HttpResponseRedirect('../books')
    else:
      form_instance = AddBookForm()
    context = {
            'books': my_books,
            "form": form_instance,
            "user": request.user,
            "profile": profile,
            "is_user": checkAuth(request),
    }
    return render(request, 'add_book.html', context=context)


@login_required(login_url='/login/')
def single_book(request, id):
    book_title = Book.objects.filter(id=id).values_list('title')
    a = Book.objects.all().values_list('title', flat=True)
    books = Book.objects.all().filter(title__in=book_title)

    reviews = Review.objects.all().filter(book__in=books)
    book_title = str(list(book_title))[3:-4]
    profile = UserProfile.objects.get(user=request.user)

    context = {
        "reviews": reviews,
        "book_title": book_title,
        "is_user": checkAuth(request),
        "user": request.user,
        "profile": profile,
    }
    return render(request, 'single_book.html', context=context)


@login_required(login_url='/login/')
def search_users(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form_instance = SearchUsersForm(request.POST)
        if(form_instance.is_valid()):
            um = form_instance.cleaned_data["username"]
            #um = form_instance.username
            context = {
                "username": um,
            }

            return redirect('profile', username=um)
    else:
        form_instance = SearchUsersForm()
    context = {
        "form": form_instance,
        "profile": profile,
        "is_user": checkAuth(request),
    }
    return render(request, 'search_users.html', context=context)


@login_required(login_url='/login/')
def createProfile(request):
    instance = get_object_or_404(UserProfile, user=request.user)
    profile = UserProfile.objects.get(user=request.user)
    if request.method == "POST":
        form_instance = ProfileForm(request.POST, request.FILES, instance=instance)
        if(form_instance.is_valid()):
            instance = form_instance.save(commit=False)
            instance.user = request.user
            username = instance.user.username
            instance.save()
            return redirect('profile', username=username)
    else:
        form_instance = ProfileForm()
    context = {
        "form": form_instance,
        "profile": profile,
        "is_user": checkAuth(request),
        "user": request.user,
    }
    return render(request, 'createProfile.html', context=context)


@login_required(login_url='/login/')
def profile(request, username=None):
    num_pages = 0
    num_pages_overall = 0
    use_info = User.objects.get(username=username)
    person = UserProfile.objects.get(user=use_info)
    pic = person.picture.url
    profile = UserProfile.objects.get(user=request.user)


    books_completed = Book.objects.filter(UserProfile=person, completed=True).count()
    books_pending = Book.objects.filter(UserProfile=person, completed=False).count()
    recommended = Review.objects.filter(UserProfile=person, recommendation=True).count()
    not_recommended = Review.objects.filter(UserProfile=person, recommendation=False).count()
    genres = list(Book.objects.filter(UserProfile=person).values_list('genre', flat=True))
    stars = list(Review.objects.filter(UserProfile=person).values_list('stars', flat=True))


    val = request.GET.get('toggle_completed', 0)
    if val != 0:
        book = Book.objects.get(id=val)
        book.completed = not book.completed
        book.save()

    try:
        user_info = User.objects.get(username=username)
        if user_info == request.user:
            is_personal_profile = True
            books = Book.objects.filter(UserProfile=profile)
            reviews = Review.objects.filter(UserProfile=profile)

        else:
            is_personal_profile = False
            books = Book.objects.filter(UserProfile=person)
            reviews = Review.objects.filter(UserProfile=person)
        is_an_account = True
        pages_read = list(Book.objects.select_related().filter(UserProfile=person).values_list('length', flat=True))
        for page in pages_read:
            num_pages += page
        pages_read_overall = list(Book.objects.select_related().values_list('length', flat=True))
        for page in pages_read_overall:
            num_pages_overall += page

        context = {
            "is_user": checkAuth(request),
            "user": request.user,
            "profile": profile,
            "username": username,
            "stars": stars,
            "num_pages": num_pages,
            "num_pages_overall": num_pages_overall,
            "pic": pic,
            "books_completed": books_completed,
            "books_pending": books_pending,
            "recommended": recommended,
            "not_recommended": not_recommended,
            "books": books,
            "reviews": reviews,
            "is_an_account": is_an_account,
            "user_info": user_info,
            "is_personal_profile": is_personal_profile,
        }
        return render(request, 'profile.html', context=context)
    except User.DoesNotExist:
        return HttpResponseRedirect("/")



def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            UserProfile.objects.get_or_create(user=user)
            # Success! Redirect to home page.
            return redirect("/login")
        else:
            # Form invalid, print errors to console
            print(join_form.errors)
            return render(request, 'join.html', {'join_form': join_form})
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form,}
        return render(request, 'join.html', page_data)


def user_login(request):
    if checkAuth(request) == True:
        HttpResponseRedirect('/')
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(request, username=username, password=password)
            # If we have a user

            if user is not None:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to homepage
                    next = request.POST.get('next', '/')
                    return HttpResponseRedirect(next)
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'login.html', {"form": login_form})

        #Nothing has been provided for username or password.
    return render(request, 'login.html', {"form": LoginForm})


@login_required(login_url='/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect("/")



class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Books to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GenreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Book Genres to be viewed or edited.
    """
    queryset = BookGenre.objects.all()
    serializer_class = BookGenreSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Reviews to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users to be viewed or edited.
    """
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
