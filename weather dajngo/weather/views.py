from django.shortcuts import render,redirect
import requests
from test_1.settings import API_KEY_W
from django.views.generic.base import View
from .models import City
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.

class Start(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'start.html')

    def post(self, request, *args, **kwargs):

        city = request.POST['city']
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
        city_weather = requests.get(url.format(city,API_KEY_W)).json()
        print(city_weather)
        if(city_weather.get('cod') and city_weather.get('cod') == 200):
            data = City()
            data.name = city_weather.get('name')
            data.code = city_weather.get('id')
            data.coord_lat = city_weather.get('coord').get('lat')
            data.coord_lon =  city_weather.get('coord').get('lon')

            data.temp = city_weather.get('main').get('temp')
            data.humidity = city_weather.get('main').get('humidity')
            data.pressure = city_weather.get('main').get('pressure')
            data.temp_max = city_weather.get('main').get('temp_max')
            data.temp_min = city_weather.get('main').get('temp_min')

            data.wind_deg = city_weather.get('wind').get('speed')
            data.wind_speed = city_weather.get('wind').get('deg')
            data.save()
            return redirect('data/?code={}'.format(data.id))

        return render(request, 'start.html',{'err':'city not found'})



class Data_C(View):

    def get(self, request, *args, **kwargs):
        ex = {}
        data = City.objects.all().order_by('-id')
        # filters 
        if (request.GET.get('city')):
            ex['select_city'] = request.GET.get('city') # select city for paginator
            data = data.filter(name=request.GET.get('city'))
        if (request.GET.get('date_form')):
            data = data.filter(date__gte=request.GET.get('date_form'))
        if(request.GET.get('date_to')):
            data = data.filter(date__lte=request.GET.get('date_to'))
        if (request.GET.get('code')):
            ex['this_data'] = int(request.GET.get('code')) # select user query 

        ex['city'] = City.objects.raw('select id, name from weather_city group by name') #all citry to db for list 
        page = Paginator(data,6)
        if (request.GET.get('page')):
            pg = request.GET.get('page')
            ex['data'] = page.get_page(pg)
        else:
            ex['data'] = page.get_page(1)

        return render(request, 'data.html',ex)

    def post(self, request, *args, **kwargs):
        pass