from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import datetime


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("main:login")

    context = {'form': form}
    return render(request, "register.html", context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = redirect("main:show_main")
            response.set_cookie('last_login', str(datetime.datetime.now()))
            messages.success(request, f"Welcome back, {user.username}!")
            return response
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {'form': form})


def logout_user(request):
    logout(request)
    response = redirect("main:login")
    response.delete_cookie('last_login')
    messages.info(request, "You have been logged out successfully.")
    return response


@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    if filter_type == "all":
        products_list = Product.objects.all()
    else:
        products_list = Product.objects.filter(user=request.user)

    context = {
        'title': 'Sport Center',
        'name': request.user.username,
        'npm': '2406430451',
        'class': 'PBP F',
        'products_list': products_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }

    return render(request, "main.html", context)

@login_required(login_url='/login')
def create_products(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        messages.success(request, f"Product '{product_entry.name}' created successfully!")
        return redirect('main:show_main')

    return render(request, "create_product.html", {'form': form})


@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"Product '{product.name}' updated successfully!")
        return redirect('main:show_main')

    return render(request, "edit_product.html", {'form': form})


@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    messages.warning(request, f"Product '{product.name}' has been deleted.")
    product.delete()
    return redirect('main:show_main')



@login_required(login_url='/login')
def show_products(request, id):
    product = get_object_or_404(Product, pk=id)
    product.increment_views()

    context = {'product': product}
    return render(request, "product_details.html", context)



@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = request.POST.get("price")
    description = strip_tags(request.POST.get("description"))
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'
    user = request.user if request.user.is_authenticated else None

    new_product = Product(
        name=name,
        price=price,
        description=description,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)



def show_xml(request):
    product_list = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", product_list), content_type="application/xml")


def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            'id': str(p.id),
            'name': p.name,
            'price': p.price,
            'description': p.description,
            'category': p.category,
            'thumbnail': p.thumbnail,
            'views': p.views,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'is_featured': p.is_featured,
            'user_id': p.user_id,
            'user_username': p.user.username if p.user else None,
        }
        for p in product_list
    ]
    return JsonResponse(data, safe=False)


def show_xml_by_id(request, product_id):
    try:
        product = Product.objects.filter(pk=product_id)
        return HttpResponse(serializers.serialize("xml", product), content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)


def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'category': product.category,
            'thumbnail': product.thumbnail,
            'views': product.views,
            'created_at': product.created_at.isoformat() if product.created_at else None,
            'is_featured': product.is_featured,
            'user_id': product.user_id,
            'user_username': product.user.username if product.user_id else None,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)
