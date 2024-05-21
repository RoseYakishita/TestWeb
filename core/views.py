from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from userauths.forms import User
from userauths.forms import CreateUserForm, UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'core/index.html', {'users': users})

class CreateUser(LoginRequiredMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'core/CreateUser.html'
    success_url = reverse_lazy('core/index')
    
class UpdateUser(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username','email', 'first_name', 'last_name', 'phone_number', 'address', 'password']
    template_name = 'core/UpdateUser.html'
    success_url = reverse_lazy('core/index')

class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'core:DeleteUser.html'
    success_url = reverse_lazy('core/index')


def search_view(request):
    query = request.GET.get("q")
    
    if not query:
        # Add an error message if the query is empty
        messages.error(request, "Search query cannot be empty.")
        users = User.objects.none()
    else:
        users = User.objects.filter(username__icontains=query).order_by("-date_joined")

    context = {
        "users": users,
        "query": query,
    }
    return render(request, "core/search.html", context)
