from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from djangoapp.restapis import get_dealers_from_cf, get_dealer_reviews_from_cf
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# Define the login_request view
def login_request(request):

    # Check if the request method is POST
    if request.method == 'POST':
        
        # If it's a POST request, get the username and password from the request
        username = request.POST['username']
        password = request.POST['password']
        
        # Use Django's built-in authenticate function to check if the provided
        # username and password correspond to a valid user
        user = authenticate(username=username, password=password)

        # If the user is valid (i.e., authenticate didn't return None),
        if user is not None:
            
            # Use Django's built-in login function to log the user in
            login(request, user)
            
            # Redirect the user to the index page
            # We use the reverse function to get the URL associated with the 'index' view
            return HttpResponseRedirect(reverse('djangoapp:index'))
        
        # If the user is not valid (i.e., authenticate returned None),
        else:
            
            # Render the login page again, but this time include an error message
            return render(request, 'djangoapp/login.html',  {'error': 'Invalid login'})
    
    # If the request method is not POST (e.g., it's a GET request),
    else:
        
        # Render the login page without an error message
        return render(request, 'djangoapp/login.html')

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')
    
    # für Weiterleitung zu anderer Page: return HttpResponseRedirect(reverse('djangoapp:homepage'))

# Create a `registration_request` view to handle sign up request

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        login(request, user)
        return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/registration.html')



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-de.functions.appdomain.cloud/api/v1/web/5f6babc9-6519-4062-ac30-e2b3b37a1776/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    reviews = get_dealer_reviews_from_cf('https://eu-de.functions.appdomain.cloud/api/v1/web/5f6babc9-6519-4062-ac30-e2b3b37a1776/review-package/get-review.json', dealer_id, "9U8iLU_x5m6heGVVuQuAw1yiui3eqnyWIzDaE_HwMINe")
    context = {"reviews": reviews}
    return HttpResponse(context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.user.is_authenticated:
        form = request.POST
        review = {}
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = form.get('review')
        review["name"] = request.user.username
        review["purchase"] = form.get('purchase')
        if form.get('purchase_date'):
            review["purchase_date"] = form.get('purchase_date')
        review["car_make"] = form.get('car_make')
        review["car_model"] = form.get('car_model')
        review["car_year"] = form.get('car_year')

        json_payload = {}
        json_payload["review"] = review

        url = 'your_cloud_function_url'  # Replace this with the URL of your cloud function
        post_request(url, json_payload, dealerId=dealer_id)
        return redirect('djangoapp:index')  # This redirects to the index page after a review is posted
    else:
        return redirect('djangoapp:login')  # Redirects to the login page if the user is not authenticated


