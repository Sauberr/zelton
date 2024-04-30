from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from userauths.forms import ProfileForm, UserRegisterForm
from userauths.models import Profile, User


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"{username} account created successfully")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            login(request, new_user)
            return redirect('core:index')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'userauths/sign-up.html', context)


def login_view(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in!')
        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {user.username} you are now logged in')
                return redirect('core:index')
            else:
                messages.error(request, 'Invalid email or password')

        except:
            messages.error(request, F'User does not exist with {email}')

    return render(request, 'userauths/sign-in.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('userauths:sign-in')


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('core:dashboard')
    else:
        form = ProfileForm()

    context = {'form': form, 'profile': profile}
    return render(request, 'userauths/profile-edit.html', context)

