from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView, FormView

from myapp.forms import CustomUserCreationForm, PurchaseForm
from myapp.models import Product, Purchase


def index(request):
    product_list = Product.objects.all()
    user_authenticated = request.user.is_authenticated
    user_admin = request.user.is_staff
    return render(request, 'index.html', {
        'product_list': product_list,
        'user_authenticated': user_authenticated,
        'user_admin': user_admin,
    })


def purchases_list(request):
    purchase_list = Purchase.objects.filter(user=request.user)
    return render(request, 'buy_products.html', {
        'purchase_list': purchase_list
    })


class Login(LoginView):
    success_url = '/'
    template_name = 'login.html'

    def get_success_url(self):
        return self.success_url


class Register(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/'

class ProductCreate(CreateView):
    template_name = 'create_product.html'
    model = Product
    fields = ['title', 'description', 'price', 'stock']
    success_url = '/'


class ProductUpdate(UpdateView):
    template_name = 'update_product.html'
    model = Product
    fields = ['title', 'description', 'price', 'stock']
    success_url = '/'


class PurchaseView(LoginRequiredMixin, FormView):
    template_name = 'purchase.html'
    form_class = PurchaseForm
    success_url = '/'

    def form_valid(self, form):
        product = form.cleaned_data['product']

        quantily = form.cleaned_data['quantily']
        # product = Product.objects.get(pk=product.id)

        if product.stock < quantily:
            form.add_error('quantily', 'На складе недостаточно товаров!')
            return super().form_invalid(form)
        elif self.request.user.bank < product.price:
            form.add_error('На кошельке недостаточно средств!')
            return super().form_invalid(form)
        else:
            purchase = Purchase.objects.create(
                user=self.request.user,
                product=product,
                quantily=quantily
            )
            purchase.save()

            product.stock -= quantily
            product.save()

            self.request.user.bank -= product.price * quantily
            self.request.user.save()

            return super().form_valid(form)
