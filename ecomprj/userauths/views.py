from django.shortcuts import render, redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from userauths.models import User


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





