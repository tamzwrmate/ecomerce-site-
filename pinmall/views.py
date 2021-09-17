# Create your views here.
from typing import Sequence
from django.db.models.query import QuerySet
from django.http import response
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from .forms import CheckoutForm
from django.contrib import messages
from . import forms
from .models import *
import json
from pinmall import forms
import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_protect


class CardListView(generic.ListView):
    model = Item
    queryset = Item.objects.all()
    template_name = "index.html"

class AboutView(generic.TemplateView):
    template_name = "about.html"

class ContactView(generic.TemplateView):
    template_name = "contact.html"


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = "card_detail.html"

class DeatailView(generic.DetailView):
    model = Item
    template_name = "card_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DeatailView, self).get_context_data(**kwargs)
        #get product id from requested url
        item_id = self.kwargs['slug']
        #get product
        item_obj = Item.objects.get(slug=item_id)
        #check if cart exists
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            item_instance = cart_obj.cartproduct_set.filter(item=item_obj)
            # items already exist in cart
            if item_instance.exists():
                cartproduct = item_instance.first()
                cartproduct.quantity += 1
                cartproduct.subtotal += item_obj.price
                cartproduct.save()
                cart_obj.total += item_obj.price
                cart_obj.save()
            # new item has been added to cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, item=item_obj, rate=item_obj.price, quantity=1, subtotal=item_obj.price)
                cart_obj.total += item_obj.price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                    cart=cart_obj, item=item_obj, rate=item_obj.price, quantity=1, subtotal=item_obj.price)
            cart_obj.total += item_obj.price
            cart_obj.save()
             #check if product already exists in cart
        return context

class AddToCartView(generic.TemplateView): 
    model = Item
    template_name = "add_cart.html"

    def get_context_data(self, **kwargs):
        context = super(AddToCartView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context

class CheckoutView(generic.CreateView):
    form_class = CheckoutForm
    success_url = reverse_lazy('pinmall:card')
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        context = super(CheckoutView, self).get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_id = None
        context['cart'] = cart_obj
        return context
    
    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.total = cart_obj.total
            del self.request.session['cart_id']
            pm = form.cleaned_data.get("payment_method")
            order = form.save()
            if pm == 'Interswitch':
                return redirect(reverse('pinmall:interswitch') + '?o_id=' + str(order.id))
        else:
            return redirect('pinmall:home')
        return super().form_valid(form)


class ManageCartView(generic.View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        else:
            pass
        return redirect('pinmall:cart')

class Interswitch(generic.View):
    model = Order

    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        order = Order.objects.get(id=o_id)

        headers = {'Content-Type': 'application/json',
         'Authorization': 'Bearer FLWPUBK_TEST-93008b13a2b9aeff8407243f6d7c3178-X'
         }
        url = 'https://api.flutterwave.com/v3/transactions/verify'
        resp = requests.get(url, headers = headers)

        context = {
            "order": order,
            "resp": resp,
            "url": url,
            "headers": headers,
        }
        if resp.status_code == "successful":
            context["redirect_page"] = reverse_lazy("pinmall:verify-payment")
        else:
            pass
        return render(request, 'flutter.html', context)

class VerifyPayment(generic.View):
    def get(self, request, *args, **kwargs):
        tx_ref = request.GET.get("tx_ref", " ")
        status = request.GET.get("status", " ")
        trans_id = request.GET.get("transaction_id", " ")

        data = {
            "tx_ref": tx_ref,
            "status": status,
            "trans_id": trans_id
        }
        return JsonResponse(data)
