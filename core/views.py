from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import (
    User, ScoreDetail, Department, Major,
    ClassRoom, Course, TeachDetail, TermScore
)
from .forms import UserProfileForm, RegistrationForm, ScoreDetailForm



def get_redirect_if_exists(request):
    redirect = None

    if request.GET and request.GET.get('next'):
        redirect = str(request.GET.get('next'))
    return redirect



def home_view(request):
    scores = ScoreDetail.objects.all()

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'core/home.html', {'scores': scores})


def login_view(request):
    if request.method == 'POST':
        # Handle form submission
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Successful login
            login(request, user)

            if user.is_superuser:
                return redirect('admin:index')  # Redirect to the admin page
            else:
                return redirect('home')  # Replace 'home' with the name of your home view or URL pattern
        else:
            # Invalid login
            return render(request, 'accounts/login.html', {'error_message': 'Invalid username or password'})
    else:
        # Display login form
        return render(request, 'accounts/login.html')


def registration_view(request):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'You are authenticated as {user}')
    
    context = {}

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # create account and login
            form.save()
            # the username below is the same as: request.POST['username']
            username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get['email'].lower()
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)

            # destination = kwargs.get('next')
            destination = get_redirect_if_exists(request)
            
            if destination:  # if destination is not None
                return redirect(destination)
            return redirect('home')
        else:
            context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'accounts/profile.html', {'user': user})
    # return render(request, 'accounts/profile.html', {'user': request.user}) # work without pk


@login_required
def update_profile_view(request, pk):
    user = User.objects.get(id=pk)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        # form = UserProfileForm(request.POST, instance=request.user) # work without pk
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
    else:
        form = UserProfileForm(instance=user)
        # form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/update_profile.html', {'form': form})


@login_required
def edit_score_detail_view(request, pk):
    score_details = ScoreDetail.objects.get(id=pk)

    if request.method == 'POST':
        form = ScoreDetailForm(request.POST, instance=score_details)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ScoreDetailForm(instance=score_details)
    
    return render(request, 'core/score_detail.html', {'form': form})


@login_required
def dep_view(request):
    deps = Department.objects.all()
    return render(request, 'core/department.html', {'deps': deps})


@login_required
def major_view(request):
    majors = Major.objects.all()
    return render(request, 'core/major.html', {'majors': majors})


@login_required
def class_view(request):
    classrooms = ClassRoom.objects.all()
    return render(request, 'core/class.html', {'classrooms': classrooms})


@login_required
def course_view(request):
    courses = Course.objects.all()
    return render(request, 'core/course.html', {'courses': courses})


@login_required
def teacher_view(request):
    teachers = TeachDetail.objects.all()
    return render(request, 'core/teacher.html', {'teachers': teachers})
