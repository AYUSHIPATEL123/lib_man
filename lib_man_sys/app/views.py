from django.shortcuts import render , redirect ,get_object_or_404
from .forms import CustomUserCreationForm , BookForm , UpdateStatusForm 
from django.contrib import messages
from django.contrib.auth import authenticate , login
from django.contrib.auth.decorators import login_required ,user_passes_test
from .models import Book , BookIssue
from django.contrib import auth
# Create your views here.
def home(request):
    return render(request, 'base.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')   

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('home') 
@login_required(login_url='login')
def books(request):
    try:
        books = Book.objects.filter(available_copies__gt=0)
    except Book.DoesNotExist:
        messages.error(request, 'Book does not exist')
        return redirect('books')
    data = {'books':books}
    return render(request, 'books.html', data)
@login_required(login_url='login')
def book_details(request,book_slug):
    try:
        book = Book.objects.get(slug=book_slug)
    except Book.DoesNotExist:
        messages.error(request, 'Book does not exist')
        return redirect('books')
    data = {'book': book}
    return render(request, 'book_details.html', data)
@login_required(login_url='login')
def request_book(request,book_slug):
    try:
        book = Book.objects.get(slug=book_slug)
    except Book.DoesNotExist:
        messages.error(request, 'Book does not exist')
        return redirect('books')
    if request.method == 'POST':
       user = request.user
       book = book
       BookIssue.objects.create(user=user, book=book, status='REQUESTED')
       messages.success(request, 'Book requested successfully')
       return redirect('book_detail', book_slug=book.slug) 
    return render(request, 'book_details.html', {'book': book})
@login_required(login_url='login')
def user_books(request):
    try:
       if request.user.is_superuser:
           books = BookIssue.objects.all()
       else:
           books = BookIssue.objects.filter(user=request.user)
    except BookIssue.DoesNotExist:
        messages.error(request, 'Book does not exist')
        return redirect('books')    
    data = { 'books':books }
    return render(request, 'user_books.html', data)

def librarian_check(user):
    return user.is_staff 
@login_required(login_url='login')
@user_passes_test(librarian_check)
def update_status(request,id):
    book_issue = get_object_or_404(BookIssue,id=id)
    if request.method == 'POST':
        form = UpdateStatusForm(request.POST,instance=book_issue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book status updated successfully')
            return redirect('dashboard')
    else:
        # this part runs when you open the form page (GET request)
        form = UpdateStatusForm(instance=book_issue)
    return render(request, 'request_man.html', {'form': form, 'issue': book_issue})  
@login_required(login_url='login')
@user_passes_test(librarian_check)
def add_books(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
                form.save()
                messages.success(request, 'Book added successfully')
                return redirect('books')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})


@login_required(login_url='login')
@user_passes_test(librarian_check)
def dashboard(request):
    books = Book.objects.all()
    requests = BookIssue.objects.filter()
    total_books = 0
    for b in books:
        total_books += b.available_copies
    requested_books = BookIssue.objects.filter(status='REQUESTED').count()
    approved_books = BookIssue.objects.filter(status='APPROVED').count()
    returned_books = BookIssue.objects.filter(status='RETURNED').count()
    context = {
        'books':books,
        'requests':requests,
        'total_books':total_books,
        'requested_books':requested_books,
        'approved_books':approved_books,
        'returned_books':returned_books
    }
    return render(request, 'dashboard.html', context)
        