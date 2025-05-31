from linecache import checkcache
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from .models import Contact
from django.contrib.auth import login
import requests, json

from rest_framework import viewsets
from .models import Destination, Category, SubCategory, Feedback, Booking, Hotels, Restaurants
from .serializers import DestinationSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
from django.http import HttpResponse
from math import ceil

def index(request):
    return render(request, 'shop/home.html')

@login_required
def booking(request, myid):
    destinations = Destination.objects.filter(id=myid)
    return render(request, 'shop/booking.html', {'destinations': destinations})

def signin(request):
    return render(request, 'shop/sign-in.html')



from django.contrib.auth.models import User
from .models import UserProfile

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        profile_picture = request.FILES.get('profile_picture')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('Main')

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('Main')

        else:

            user = User.objects.create_user(username=username, email=email, password=password)

        # Now update the profile created via signal
        user.userprofile.name = name
        user.userprofile.phone = phone
        user.userprofile.email = email
        user.userprofile.profile_picture = profile_picture
        user.userprofile.save()

        login(request, user)
        return redirect('Main')
    return render(request, 'shop/sign-in.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Main')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'shop/log-in.html', )




def logout_view(request):
    logout(request)
    return redirect('Main')

def profile_view(request):
    my_bookings = Booking.objects.filter(user=request.user).order_by('-checkin')
    return render(request, 'shop/profile.html', {'my_bookings': my_bookings})

def contact_form(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        phone = request.POST.get('phone','')
        remarks = request.POST.get('remarks','')
        email =request.POST.get('email','')
        contact = Contact(name=name, phone=phone, email=email, remarks=remarks)
        contact.save()
    return render(request, 'shop/contact.html')

def hotels(request):
    if request.method == 'GET':
        city = request.GET.get('city','')
        if city:
            hotel = Category.objects.filter(name__iexact='India')
            hotels = Hotels.objects.filter(category__in=hotel)
            print("Hotels count:", hotels.count())
            return render(request, 'shop/hotels.html', {
                'hotels': hotels,
                'category': hotel,
            })
    return render(request, 'shop/hotels.html')

def todo(request):
    import requests

    api_key = '' # Replace with your API key
    city = 'Delhi'  # Example city

    url = f'https://api.api-ninjas.com/v1/tourism?city={city}'

    headers = {
        'X-Api-Key': api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        for place in data:
            print(f"Name: {place['name']}")
            print(f"Description: {place.get('description', 'No description available')}")
            print(f"Address: {place.get('address', 'No address provided')}")
            print('-' * 40)
    else:
        print(f"Error: {response.status_code} - {response.text}")
    return render(request, 'shop/hotels.html')

import requests
from datetime import datetime

def flights(request):
    flights = []
    passengers = 1

    if request.method == 'GET':
        iata_from = request.GET.get('from')
        iata_to = request.GET.get('to')
        travel_date = request.GET.get('date')
        passengers = request.GET.get('passengers', '1')

        try:
            passengers = int(passengers)
            if passengers < 1:
                passengers = 1
        except ValueError:
            passengers = 1

        # Wrap all logic under this check
        if iata_from and iata_to and travel_date:
            api_key = ''
            url = f"http://api.aviationstack.com/v1/flights?access_key={api_key}&dep_iata={iata_from}&arr_iata={iata_to}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json().get('data', [])
                flights = data


            print("Fetched flights:", len(flights))

    return render(request, 'shop/flights.html', {'flights': flights, 'passengers': passengers})


def reviews(request):
    reviews = [
        {
            "name": "Ananya Mehta",
            "location": "Delhi, India",
            "comment": "TripTrop made my Kerala trip unforgettable. Highly recommended!",
            "rating": 5,
            "photo": "https://via.placeholder.com/60?text=A"
        },
        {
            "name": "Rahul Verma",
            "location": "Mumbai, India",
            "comment": "The hotel booking was super smooth. Great platform!",
            "rating": 4,
            "photo": "https://via.placeholder.com/60?text=R"
        },
        {
            "name": "Simran Kapoor",
            "location": "Chandigarh, India",
            "comment": "Loved the curated holiday homes. Will book again.",
            "rating": 5,
            "photo": "https://via.placeholder.com/60?text=S"
        },
        {
            "name": "Arjun Rao",
            "location": "Hyderabad, India",
            "comment": "The restaurant recommendations were top notch!",
            "rating": 4,
            "photo": "https://via.placeholder.com/60?text=AR"
        },
        {
            "name": "Neha Sharma",
            "location": "Bangalore, India",
            "comment": "Amazing experience overall, but the support could improve.",
            "rating": 3,
            "photo": "https://via.placeholder.com/60?text=N"
        },
        {
            "name": "Kunal Jain",
            "location": "Ahmedabad, India",
            "comment": "Booked my adventure tour easily. Thanks, TripTrop!",
            "rating": 5,
            "photo": "https://via.placeholder.com/60?text=K"
        },
        {
            "name": "Isha Rawat",
            "location": "Pune, India",
            "comment": "Clean interface and smooth user flow. Great job.",
            "rating": 4,
            "photo": "https://via.placeholder.com/60?text=I"
        },
        {
            "name": "Dev Mishra",
            "location": "Lucknow, India",
            "comment": "My first trip through TripTrop went really well.",
            "rating": 4,
            "photo": "https://via.placeholder.com/60?text=D"
        },
        {
            "name": "Tanya Joshi",
            "location": "Jaipur, India",
            "comment": "Their ‘Things to Do’ list was so useful!",
            "rating": 5,
            "photo": "https://via.placeholder.com/60?text=T"
        },
        {
            "name": "Aarav Khanna",
            "location": "Indore, India",
            "comment": "Perfect for spontaneous getaways. Kudos!",
            "rating": 5,
            "photo": "https://via.placeholder.com/60?text=AK"
        },

            {
                "name": "Ananya Mehta",
                "location": "Delhi, India",
                "comment": "TripTrop made my Kerala trip unforgettable. Highly recommended!",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=A"
            },
            {
                "name": "Rahul Verma",
                "location": "Mumbai, India",
                "comment": "The hotel booking was super smooth. Great platform!",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=R"
            },
            {
                "name": "Simran Kapoor",
                "location": "Chandigarh, India",
                "comment": "Loved the curated holiday homes. Will book again.",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=S"
            },
            {
                "name": "Arjun Rao",
                "location": "Hyderabad, India",
                "comment": "The restaurant recommendations were top notch!",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=AR"
            },
            {
                "name": "Neha Sharma",
                "location": "Bangalore, India",
                "comment": "Amazing experience overall, but the support could improve.",
                "rating": 3,
                "photo": "https://via.placeholder.com/60?text=N"
            },
            {
                "name": "Kunal Jain",
                "location": "Ahmedabad, India",
                "comment": "Booked my adventure tour easily. Thanks, TripTrop!",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=K"
            },
            {
                "name": "Isha Rawat",
                "location": "Pune, India",
                "comment": "Clean interface and smooth user flow. Great job.",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=I"
            },
            {
                "name": "Dev Mishra",
                "location": "Lucknow, India",
                "comment": "My first trip through TripTrop went really well.",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=D"
            },
            {
                "name": "Tanya Joshi",
                "location": "Jaipur, India",
                "comment": "Their ‘Things to Do’ list was so useful!",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=T"
            },
            {
                "name": "Aarav Khanna",
                "location": "Indore, India",
                "comment": "Perfect for spontaneous getaways. Kudos!",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=AK"
            },
            {
                "name": "Ritika Sen",
                "location": "Kolkata, India",
                "comment": "Super easy to plan a quick trip with TripTrop!",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=RS"
            },
            {
                "name": "Yash Agarwal",
                "location": "Udaipur, India",
                "comment": "Loved the restaurant filters and local guides.",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=Y"
            },
            {
                "name": "Meera Iyer",
                "location": "Chennai, India",
                "comment": "TripTrop helped us find a hidden beach resort!",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=M"
            },
            {
                "name": "Varun Joshi",
                "location": "Shimla, India",
                "comment": "The site is easy to navigate and well-organized.",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=V"
            },
            {
                "name": "Alisha Khan",
                "location": "Srinagar, India",
                "comment": "Booked a romantic stay in Gulmarg — magical experience.",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=AK"
            },
            {
                "name": "Rohit Thakur",
                "location": "Manali, India",
                "comment": "Loved the adventure tour options and tips!",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=RT"
            },
            {
                "name": "Irfan Sheikh",
                "location": "Nagpur, India",
                "comment": "Good experience, but would like more payment options.",
                "rating": 3,
                "photo": "https://via.placeholder.com/60?text=I"
            },
            {
                "name": "Pooja Singh",
                "location": "Ranchi, India",
                "comment": "The feedback system is helpful and transparent.",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=P"
            },
            {
                "name": "Siddharth Malhotra",
                "location": "Agra, India",
                "comment": "Nice user experience and reliable service.",
                "rating": 4,
                "photo": "https://via.placeholder.com/60?text=SM"
            },
            {
                "name": "Nikita Das",
                "location": "Bhubaneswar, India",
                "comment": "TripTrop brought my travel plans to life!",
                "rating": 5,
                "photo": "https://via.placeholder.com/60?text=N"
            },

    ]
    return render(request, 'shop/reviews.html', {'reviews': reviews})

def holiday_home(request):
    restaurants = Category.objects.filter(name__iexact='India')
    rest = Restaurants.objects.filter(category__in=restaurants)
    print("Restaurants queryset:", restaurants)
    print("Restaurant count:", rest.count())
    return render(request, 'shop/holiday-home.html', {
        'restaurants': rest,
        'category': restaurants,
    })

def get_location_id(city):
    url = "https://tripadvisor16.p.rapidapi.com/api/v1/restaurant/searchLocation"
    querystring = {"query": city}

    headers = {
        "X-RapidAPI-Key": "ade9b9e238msh16bf7f5f5db73fcp1cdb41jsn9a6e39f1eeaa",
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        # Assuming the first location is what we want
        location_id = data.get("data", {}).get("locationId", None)
        return location_id
    return None

def restaurants(request):
    if request.method=='GET':
        city=request.GET.get('city')
        if city:
            restaurants = Category.objects.filter(name__iexact='India')
            rest = Restaurants.objects.filter(category__in=restaurants)
            print("Restaurants queryset:", restaurants)
            print("Restaurant count:", rest.count())
            return render(request, 'shop/restaurants.html', {
                'restaurants': rest,
                'category': restaurants,
            })
    return render(request, 'shop/restaurants.html')

def basic(request):
    return render(request, 'shop/basic1.html')

def feedback(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        rating = request.POST.get('rating', '')
        visit_date = request.POST.get('visit_date', '')
        best_part =  request.POST.get('best_part', '')
        remarks = request.POST.get('remarks', '')
        email = request.POST.get('email', '')
        feedback = Feedback(name=name, phone=phone, email=email, remarks=remarks, rating=rating, visit_date=visit_date, best_part=best_part)
        feedback.save()

    return render(request, 'shop/feedback.html')

def luxury(request):
    luxury_categories = SubCategory.objects.filter(name__iexact='Luxury Trips')
    print("Luxury Categories:", luxury_categories)
    destinations = Destination.objects.filter(sub_category__in=luxury_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/luxury.html', {
        'destinations': destinations,
        'sub_category': luxury_categories,
    })
    #return render(request, 'shop/luxury.html')

def family(request):
    family_categories = SubCategory.objects.filter(name__iexact='Family-Friendly Trips')
    print("Luxury Categories:", family_categories)
    destinations = Destination.objects.filter(sub_category__in=family_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/family-friendly.html', {
        'destinations': destinations,
        'sub_category': family_categories,
    })

def weekend(request):
    weekend_categories = SubCategory.objects.filter(name__iexact='Weekend Trips')
    print("Luxury Categories:", weekend_categories)
    destinations = Destination.objects.filter(sub_category__in=weekend_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/weekend-trips.html', {
        'destinations': destinations,
        'sub_category': weekend_categories,
    })

def all(request):
    destinations = Destination.objects.all()
    print("Destinations:", destinations)
    return render(request, 'shop/all.html', {
        'destinations': destinations,
    })




class DestinationViewSet(viewsets.ModelViewSet):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        queryset = Destination.objects.all()
        category = self.request.query_params.get('category')
        subcategory = self.request.query_params.get('subcategory')

        if category:
            queryset = queryset.filter(category__name__iexact=category)
        if subcategory:
            queryset = queryset.filter(subcategory__name__iexact=subcategory)

        return queryset

def search(request):
    if request.method == "POST":
        destination = request.POST.get('destination', '')
        names = Destination.objects.filter(name__iexact=destination)
        destinations = Destination.objects.filter(name=destination)
        return render(request, 'shop/search.html', {
            'destinations': destinations,
            'name': destination,
        })

def day(request):
    day_categories = SubCategory.objects.filter(name__iexact='3-Day Trips')
    print("Luxury Categories:", day_categories)
    destinations = Destination.objects.filter(sub_category__in=day_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/day.html', {
        'destinations': destinations,
        'sub_category': day_categories,
    })

def days(request):
    days_categories = SubCategory.objects.filter(name__iexact='7-day Trips')
    print("Luxury Categories:", days_categories)
    destinations = Destination.objects.filter(sub_category__in=days_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/days.html', {
        'destinations': destinations,
        'sub_category': days_categories,
    })

def festive(request):
    festive_categories = SubCategory.objects.filter(name__iexact='Festive Trips')
    print("Luxury Categories:", festive_categories)
    destinations = Destination.objects.filter(sub_category__in=festive_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/festive.html', {
        'destinations': destinations,
        'sub_category': festive_categories,
    })

def international(request):
    international_categories = Category.objects.filter(name__iexact='International')
    print("Luxury Categories:", international_categories)
    destinations = Destination.objects.filter(category__in=international_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/international.html', {
        'destinations': destinations,
        'category': international_categories,
    })

def national(request):
    national_categories = Category.objects.filter(name__iexact='India')
    print("Luxury Categories:", national_categories)
    destinations = Destination.objects.filter(category__in=national_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/national.html', {
        'destinations': destinations,
        'category': national_categories,
    })

def dream(request):
    destinations = Destination.objects.all()
    print("Destinations:", destinations)
    return render(request, 'shop/dream.html', {
        'destinations': destinations,
    })

def m(request):
    m_categories = SubCategory.objects.filter(name__iexact='Mountain Trips')
    print("Luxury Categories:", m_categories)
    destinations = Destination.objects.filter(sub_category__in=m_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/m.html', {
        'destinations': destinations,
        'sub_category': m_categories,
    })

def b(request):
    b_categories = SubCategory.objects.filter(name__iexact='Beach Trips')
    print("Luxury Categories:", b_categories)
    destinations = Destination.objects.filter(sub_category__in=b_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/b.html', {
        'destinations': destinations,
        'sub_category': b_categories,
    })

def a(request):
    a_categories = SubCategory.objects.filter(name__iexact='Adventurous Trips')
    print("Luxury Categories:", a_categories)
    destinations = Destination.objects.filter(sub_category__in=a_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/a.html', {
        'destinations': destinations,
        'sub_category': a_categories,
    })

def p(request):
    p_categories = SubCategory.objects.filter(name__iexact='Peaceful Trips')
    print("Luxury Categories:", p_categories)
    destinations = Destination.objects.filter(sub_category__in=p_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/p.html', {
        'destinations': destinations,
        'sub_category': p_categories,
    })

def h(request):
    h_categories = SubCategory.objects.filter(name__iexact='Hidden Wonders')
    print("Luxury Categories:", h_categories)
    destinations = Destination.objects.filter(sub_category__in=h_categories)
    print("Destinations:", destinations)
    return render(request, 'shop/h.html', {
        'destinations': destinations,
        'sub_category': h_categories,
    })