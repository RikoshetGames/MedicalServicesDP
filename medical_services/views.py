from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse
from config import settings
from medical_services.forms import CategoryForm, ServicesForm
from medical_services.models import Category, Service, Cart

from django.urls import reverse_lazy


def home(request):
    return render(request, 'medical_services/home.html')


# Классы категории
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    permission_required = 'medical_services.add_category'
    success_url = reverse_lazy("category_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_services.add_category'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category


class CategoryUpdateView(UpdateView, PermissionRequiredMixin):
    model = Category
    form_class = CategoryForm
    permission_required = 'medical_services.update_category'
    success_url = reverse_lazy("category_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_services.update_category'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class CategoryDeleteView(DeleteView, PermissionRequiredMixin):
    model = Category
    success_url = reverse_lazy("category_list")
    permission_required = 'medical_services.delete_category'
    template_name = "medical_services/category_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_object().category_title
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_services.delete_category'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class CategoryServiceListView(ListView):
    model = Service

    def get_queryset(self):
        category_pk = self.kwargs['pk']
        return Service.objects.filter(category_id=category_pk)


# Классы услуг
class ServiceCreateView(CreateView, PermissionRequiredMixin):
    model = Service
    form_class = ServicesForm
    permission_required = 'medical_services.add_service'
    success_url = reverse_lazy("service_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_services.add_service'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class ServiceListView(ListView):
    model = Service


class ServiceDetailView(DetailView):
    model = Service

    def get(self, request, pk):
        product = Service.objects.get(pk=pk)
        context = {
            'object_list': Service.objects.filter(id=pk),
        }
        return render(request, 'medical_services/service_detail.html', context)


class ServiceUpdateView(UpdateView, PermissionRequiredMixin):
    model = Service
    form_class = ServicesForm
    permission_required = 'medical_services.update_service'
    success_url = reverse_lazy("service_list")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_services.update_service'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class ServiceDeleteView(DeleteView, PermissionRequiredMixin):
    model = Service
    success_url = reverse_lazy("service_list")
    permission_required = 'medical_services.delete_service'
    template_name = "medical_services/service_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = self.get_object().services_title
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('medical_services.delete_service'):
            return HttpResponseForbidden("У вас нет доступа")
        return super().dispatch(request, *args, **kwargs)


class ContactView(View):
    def get(self, request):
        return render(request, 'medical_services/contacts.html')


class ServiceCartView(View):
    model = Cart

    def get(self, request):
        # Получаем объект корзины для текущего пользователя
        cart = Cart.objects.filter(client=request.user).first()

        # Получаем количество услуг в корзине
        services_count = cart.services.count() if cart else 0

        # Получаем список услуг в корзине
        services = cart.services.all() if cart else []

        # Получаем данные о клиенте
        client = cart.client if cart else None

        # Получаем сумму покупок услуг в корзине
        total_price = sum(service.price for service in services)

        # Обновляем контекст
        context = {
            'services_count': services_count,
            'services': services,
            'total_price': total_price,
            'client': client
        }
        return render(request, 'medical_services/shopping_cart.html', context)



def send_cart_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Логика для отправки письма
        message = render_to_string('cart_email.html')
        send_mail(
            subject='Оформление заказа в медицинской клинике',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],  # Замените на адрес получателя
        )
        return HttpResponse('Письмо о заказе отправлено на вашу почту')  # Ответ на успешную отправку
    else:
        return HttpResponse('Ошибка отправки письма о заказе на вашу почту')  # Ответ на недопустимый метод запроса