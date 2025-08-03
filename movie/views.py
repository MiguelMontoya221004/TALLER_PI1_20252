from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie


# Create your views here.
def home(request):
    #return HttpResponse('<h1> WELCOME TO HOME PAGE</h1>')
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name':'Miguel Montoya A'})
    searchTerm=request.GET.get('searchMovie')
    if searchTerm:
        movies=Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies=Movie.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm, 'movies':movies})

def about(request):
    return render(request, 'about.html' )

def search(request):
    query = request.GET.get('q')
    results = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'results': results, 'query': query})