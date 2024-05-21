from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from userauths.forms import User
from userauths.forms import CreateUserForm, UserRegisterForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

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
    users = User.objects.filter(username__icontains=query).order_by("-date_joined")
    items_per_page = 10
    paginator = Paginator(users, items_per_page)

    # Lấy số trang từ tham số truy vấn (nếu có), mặc định là 1
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "users": page_obj.object_list,
        "query": query,
        "page_obj": page_obj,
    }
    return render(request, "core/search.html", context)
