from django.shortcuts import render
from django.http import HttpResponse
from .models import Movie
from django.db.models import Count

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib, base64

# Página principal
def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

# Página "About"
def about(request):
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


# Página de búsqueda (si la usas)
def search(request):
    query = request.GET.get('q')
    results = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, 'search_results.html', {'results': results, 'query': query})

# Página de estadísticas
# Página de estadísticas
def statistics_view(request):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import io, base64

    # ============================
    # Gráfica 1: Películas por año
    # ============================
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {str(year): Movie.objects.filter(year=year).count() for year in years if year}

    # Crear gráfica
    plt.figure(figsize=(8,5))
    plt.bar(movie_counts_by_year.keys(), movie_counts_by_year.values(),
            width=0.5, color='skyblue', edgecolor='black')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)

    buffer1 = io.BytesIO()
    plt.savefig(buffer1, format='png')
    buffer1.seek(0)
    graphic_year = base64.b64encode(buffer1.getvalue()).decode('utf-8')
    buffer1.close()
    plt.close()

    # ============================
    # Gráfica 2: Películas por género
    # ============================
    movies = Movie.objects.all()
    genre_counts = {}

    for movie in movies:
        if movie.genre:
            first_genre = movie.genre.split(",")[0].strip()
            genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    plt.figure(figsize=(8,5))
    plt.bar(genre_counts.keys(), genre_counts.values(),
            color='orange', edgecolor='black')
    plt.title('Movies per Genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.xticks(rotation=45)

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png')
    buffer2.seek(0)
    graphic_genre = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    buffer2.close()
    plt.close()

    # Renderizamos ambas gráficas en el mismo template
    return render(request, 'statistics.html', {
        'graphic_year': graphic_year,
        'graphic_genre': graphic_genre
    })

