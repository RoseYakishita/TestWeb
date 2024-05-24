from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from userauths.forms import ProfileForm, User, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            # Lấy giá trị ngày sinh từ cleaned_data
            birth_date = form.cleaned_data.get('birth_date')
            new_user = form.save(commit=False)
            new_user.birth_date = birth_date
            new_user.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, Your account was created successfully.")
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request, "userauths/Register.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey you are already Logged In.")
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email") # peanuts@gmail.com
        password = request.POST.get("password") # getmepeanuts

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "Email or Password incorrect! Try again!")

        except:
            messages.warning(request, f"User with {email} does not exist")


    return render(request, "userauths/Sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You've logged out.")
    return redirect("core:index")

@login_required
def profile_update(request):
    profile = request.user  # Lấy thông tin người dùng hiện tại

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            update_session_auth_hash(request, request.user)  # Giữ người dùng đăng nhập sau khi cập nhật
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:index")  # Điều hướng về trang dashboard sau khi cập nhật thành công
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/Edit-profile.html", context)
