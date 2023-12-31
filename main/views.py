
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from main.models import Product #cek
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.contrib.auth import authenticate, login, logout



@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.filter(user=request.user)
    total_items = products.count()
    context = {
        'name': request.user.username,
        'class': 'PBP E',
        'products': products,
        'total_items' : total_items,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)
def show_xml(request):
    data = Product.objects.all()
def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")



def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login')
def add_product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        quantity = 1  
        product.amount += quantity
        product.save()
    return redirect('main:show_main')

@login_required(login_url='/login')
def subtract_product(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(pk=product_id)
        quantity = 1  
        if product.amount >= quantity:
            product.amount -= quantity
            product.save()
    return redirect('main:show_main')

@login_required(login_url='/login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Memastikan hanya pemilik produk yang dapat menghapusnya
    if product.user == request.user:
        product.delete()
    return redirect('main:show_main')
