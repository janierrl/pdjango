from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from typing import Union
from django.http import HttpRequest, HttpResponse
from ..forms.user_form import CustomUserChangeForm, CustomAuthenticationForm


def signup(request: HttpRequest) -> Union[HttpResponse, HttpResponse]:
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']

            try:
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()
                login(request, user)
                messages.success(
                    request, 'Your account has been created successfully.')
                return redirect('home')
            except IntegrityError:
                messages.error(request, 'User already exists.')
        else:
            errors = user_form.errors
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'Error in field "{
                                   field}": {error}')

        return render(request, "authentication/register.html", {
            "form": user_form
        })

    return render(request, "authentication/register.html", {
        "form": UserCreationForm()
    })


def signin(request: HttpRequest) -> Union[HttpResponse, HttpResponse]:
    if request.method == "POST":
        login_form = AuthenticationForm(request, request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, 'Username or password is incorrect.')
        else:
            errors = login_form.errors
            for field, field_errors in errors.items():
                for error in field_errors:
                    messages.error(request, f'Error in field "{
                                   field}": {error}')

    return render(request, "authentication/login.html", {
        "form": AuthenticationForm()
    })


@login_required
def signout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("home")


@login_required
def manage_account(request: HttpRequest) -> Union[HttpResponse, HttpResponse]:
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user_form.save()
            password_form.save()
            update_session_auth_hash(request, request.user)
            messages.success(
                request, 'Your account details have been updated and your password has been changed.')
            return redirect('home')
        else:
            for field, errors in user_form.errors.items():
                for error in errors:
                    if field == 'email' and 'Enter a valid email address.' in error:
                        messages.error(
                            request, 'Please enter a valid email address.')
                    else:
                        messages.error(request, f'Error in field "{
                                       field}": {error}')

            for field, errors in password_form.errors.items():
                for error in errors:
                    if field == 'old_password' and 'Incorrect password' in error:
                        messages.error(
                            request, 'Your current password is incorrect.')
                    elif field == 'new_password2' and 'The two password fields didn\'t match' in error:
                        messages.error(
                            request, 'The new passwords do not match.')
                    else:
                        messages.error(request, f'Error in field "{
                                       field}": {error}')

            messages.error(request, 'Please correct the errors below.')

    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'authentication/manage_account.html', {
        'user_form': user_form,
        'password_form': password_form
    })


@login_required
def delete_account(request: HttpRequest) -> Union[HttpResponse, HttpResponse]:
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                request, username=request.user.username, password=form.cleaned_data['password'])
            if user is not None:
                request.user.delete()
                messages.success(request, 'Your account has been deleted.')
                return redirect('home')
            else:
                messages.error(
                    request, 'Incorrect password. Account deletion failed.')

    else:
        form = CustomAuthenticationForm()

    return render(request, 'authentication/delete_account.html', {
        'form': form
    })
