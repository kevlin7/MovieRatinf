from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from tmdbv3api import TMDb
from tmdbv3api import Movie

from django.http import HttpResponse
from django.core import serializers


from .models import  PopularMovie
from .forms import SignUpForm #ChallanForm,
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login

tmdb = TMDb()
#The API Key to get the Movies data 
tmdb.api_key = "2e93434991976d7b7a48dba6459bd15f"




#API = "2e93434991976d7b7a48dba6459bd15f"

#Url = "https://api.themoviedb.org/3/movie/550?api_key=2e93434991976d7b7a48dba6459bd15f"

#API_Read_Access_Token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyZTkzNDM0OTkxOTc2ZDdiN2E0OGRiYTY0NTliZDE1ZiIsInN1YiI6IjYyNjRlYjJkMjAyZTExMDhhYzdhYzdkNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z5af45h0bvdFo3R594oXyeX53tm_U43Jf3RIGsHVTfg"

#The Dashboard page with Django Login Decorator
@login_required()
def index(request):
    #Saves the popular movies to the Database during first load and when Database is empty
    if PopularMovie.objects.count() == 0: 
        movie = Movie()
        popular = movie.popular()
        for p in popular:
            temp_record = PopularMovie()
            temp_record.movie_id = p.id
            temp_record.title = p.title
            temp_record.rating = p.vote_average
            temp_record.save()        
    return render(request, 'index.html',{"access_token":tmdb.api_key})

#Function to Register new User
def register_user(request):
    if request.method =='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            auth_login(request,user)
            messages.success(request, ('Youre now registered'))
            return redirect('login')
    else: 
        form = SignUpForm() 
    
    context = {'form': form}
    return render(request, 'registration/register.html', context)    

#Function for logging off from the system
def logout_user(request):
    logout(request)
    messages.success(request,('Youre now logged out'))
    return redirect('login')    

#Function to display the List of Movies
@login_required()
def movie_list(request):
    return render(request, 'movielist.html')


#Function to Authenticate the token
@login_required()
def token_authentication(request):
    return render(request, 'tokenauthenticator.html')    

#Function to render the Movies data from the Database
@login_required()
def render_table(request):
    db_data = PopularMovie.objects.raw('SELECT * FROM popular_movie ORDER BY id desc')
    serialized_objects = serializers.serialize('json', db_data)
    return HttpResponse(serialized_objects, content_type='application/json; charset=utf-8')    
          
