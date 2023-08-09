from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview

# from .restapis import related methods
from .restapis import get_request, post_request, get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf

from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
# Get an instance of a logger
logger = logging.getLogger(__name__)



def get_dealerships(request):
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/8722802e-f99e-4f64-a264-708e82b32678/dealership-package/get-dealership"

        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {}
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

def get_dealer_details(request, id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8722802e-f99e-4f64-a264-708e82b32678/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8722802e-f99e-4f64-a264-708e82b32678/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8722802e-f99e-4f64-a264-708e82b32678/dealership-package/get-dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id)
    context["dealer"] = dealer
    if request.method == 'GET':
        cars = CarModel.objects.all()
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            form = request.POST
            review["dealership"] = id
            review["review"] = form["content"]
            if(form.get("purchasecheck") == "on"):
                review["purchase"] = True
            else:
                review["purchase"] = False
            if(review["purchase"]):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.make.name
                review["car_model"] = car.name
                review["car_year"] = car.year
            post_url = "https://us-south.functions.appdomain.cloud/api/v1/web/8722802e-f99e-4f64-a264-708e82b32678/dealership-package/post-review"
            json_payload = { "review": review }
            post_request(post_url, json_payload, id=id)
            return redirect("djangoapp:dealer_details", id=id)
    else:
        return redirect("/djangoapp/login")

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...


def static_template_view(request):
    context = {}
    if request.method == "GET":
        return render(request, 'static_template.html', context)

def get_about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def get_contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

def registration_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('djangoapp:index')
    return render(request, 'djangoapp/registration.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
