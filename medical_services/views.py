import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, CreateView, UpdateView, TemplateView
from django.urls import reverse
from config import settings
from medical_services.forms import CategoryForm, ServicesForm
from medical_services.models import Category, Service, Cart

from django.urls import reverse_lazy


# Классы категории
class CategoryCreateView(CreateView, PermissionRequiredMixin):
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
        if not request.user.has_perm('medical_services.change_category'):
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
        if not request.user.has_perm('medical_services.change_service'):
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
    """ Контакты """

    def get(self, request):
        return render(request, 'medical_services/contacts.html')

    def post(self, request):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            # Логика для отправки письма администратору
            subject = 'Обращение от посетителя сайта'
            admin_message = f'Имя: {name}\nТелефон: {phone}\nСообщение: {message}'
            send_mail(
                subject=subject,
                message=admin_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Замените на реальный адрес администратора
            )

            messages.success(request, 'Ваше сообщение успешно отправлено. Мы свяжемся с вами в ближайшее время.')

            return redirect(reverse('medical_services:contacts'))  # Редирект на страницу контактов или другую подходящую страницу


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

    def post(self, request):
        cart = Cart.objects.filter(client=request.user).first()
        if cart:
            services = cart.services.all()
            total_price = sum(service.price for service in services)

            # Логика для отправки письма администратору
            context = {'services': services, 'total_price': total_price, 'user': request.user}
            admin_message = render_to_string('medical_services/admin_cart_email.html', context)
            send_mail(
                subject='Новый заказ в медицинской клинике',
                message='Новый заказ в медицинской клинике',
                html_message=admin_message,  # Отправка HTML-сообщения
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],  # Замените на реальный адрес администратора
            )

            # Логика для отправки письма пользователю
            user_message = render_to_string('medical_services/cart_email.html', context)
            send_mail(
                subject='Оформление заказа в медицинской клинике',
                message='Оформление заказа в медицинской клинике',
                html_message=user_message,  # Отправка HTML-сообщения
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
            )

            messages.success(request, 'Спасибо, что выбрали нас!')  # Добавление сообщения "спасибо"

            cart.services.clear()  # Очистка корзины

            return redirect(reverse('medical_services:service_cart'))  # Редирект на страницу корзины
        else:
            return HttpResponse('Ошибка отправки письма о заказе на вашу почту')


class AddToCartView(View):
    def post(self, request, pk):
        json_data = json.loads(request.body)
        service_id = json_data.get('service_id')
        service = Service.objects.get(pk=service_id)

        # Получите объект корзины текущего пользователя или создайте новый
        cart, created = Cart.objects.get_or_create(client=request.user)

        # Добавление услуги в корзину
        cart.services.add(service)

        return JsonResponse({'message': 'Услуга успешно добавлена в корзину.'})


def home(request):
    return render(request, 'medical_services/home.html')

def remove_service(request, service_id):
    if request.method == 'POST':
        service = get_object_or_404(Service, id=service_id)
        cart = Cart.objects.get(client=request.user)
        cart.services.remove(service)
        return redirect(reverse('medical_services:service_cart'))
    else:
        return redirect(reverse('medical_services:service_cart'))

def clear_service(request):
    if request.method == 'POST':
        cart = Cart.objects.get(client=request.user)
        cart.services.clear()
        return redirect(reverse('medical_services:service_cart'))
    else:
        return redirect(reverse('medical_services:service_cart'))


