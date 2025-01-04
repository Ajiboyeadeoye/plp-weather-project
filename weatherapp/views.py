from django.shortcuts import render
from django.contrib import messages
import requests
import datetime
from dotenv import load_dotenv
import os

# Create your views here.
def home(request):

    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=ed3c75217434d85fd3365bb732b92b84'
    PARAMS = {'units': 'metric'}
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    SEARCH_ENGINE_ID = os.getenv('SEARCH_ENGINE_ID')
   

    Query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={Query}&start={start}&searchType={searchType}&imgSize=xlarge&num=1"
    data = requests.get(city_url).json()
    count = 0
    search_items = data.get("items")
    image_url = search_items[0].get("link")

    try:
        data = requests.get(url, PARAMS).json()

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']

        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {'description': description, 'icon': icon, 'temp': temp, 'day': day, 'city': city, 'exception_occured':False, 'image_url': image_url})

    except:
        exception_occured = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {'description': 'clear sky', 'icon': '01d', 'temp': 25, 'day': day, 'city': 'indore', exception_occured :True},)
    
