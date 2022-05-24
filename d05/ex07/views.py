from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import UpdateForm
from .models import Movies


def populate(request):

    movies = [
        {
            'episode_nb': '1',
            'title': 'The Phantom Menace',
            'director': 'George Lucas',
            'producer': 'Rick McCallum',
            'release_date': '1999-05-19'
        },
        {
            'episode_nb': '2',
            'title': 'Attack of the Clones',
            'director': 'George Lucas',
            'producer': 'Rick McCallum',
            'release_date': '2002-05-16'
        },
        {
            'episode_nb': '3',
            'title': 'Revenge of the Sith',
            'director': 'George Lucas',
            'producer': 'Rick McCallum',
            'release_date': '2005-05-19'
        },
        {
            'episode_nb': '4',
            'title': ' A New Hope',
            'director': 'George Lucas',
            'producer': 'Gary Kurtz, Rick McCallum',
            'release_date': '1977-05-25'
        },
        {
            'episode_nb': '5',
            'title': 'The Empire Strikes Back',
            'director': 'Irvin Kershner',
            'producer': 'Gary Kurtz, Rick McCallum',
            'release_date': '1980-05-17'
        },
        {
            'episode_nb': '6',
            'title': 'Return of the Jedi',
            'director': 'Richard Marquand',
            'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum',
            'release_date': '1983-05-25'
        },
        {
            'episode_nb': '7',
            'title': 'The Force Awakens',
            'director': 'J. J. Abrams',
            'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk',
            'release_date': '2015-12-11'
        },
    ]

    result = []
    for movie in movies:
        try:
            Movies.objects.create(
                episode_nb=movie['episode_nb'],
                title=movie['title'],
                director=movie['director'],
                producer=movie['producer'],
                release_date=movie['release_date']
            )
            result.append('OK')
        except Exception as e:
            result.append(e)
    return HttpResponse("<br/>".join(str(el) for el in result))


def display(request):
    try:
        movies = Movies.objects.order_by('episode_nb')
        if not movies:
            return HttpResponse("No data available")
        return render(request, 'ex07/display.html', {'movies':movies})
    except Exception as e:
        return HttpResponse("No data available")


def update(request):
    if request.method == 'POST':
        try:
            movies = Movies.objects.order_by('episode_nb')
            if not movies:
                raise Movies.DoesNotExist
        except Movies.DoesNotExist as e:
            return HttpResponse(e)
        choices = ((movie.title, movie.title) for movie in movies)
        data = UpdateForm(choices, request.POST)
        if data.is_valid():
            try:
                movie = Movies.objects.get(title=data.cleaned_data['title'])
                movie.opening_crawl = data.cleaned_data['opening_crawl']
                movie.save()
            except Exception as e:
                print(e)
        return redirect(request.path)
    else:
        try:
            movies = Movies.objects.order_by('episode_nb')
            if not movies:
                return HttpResponse("No data available")
        except Movies.DoesNotExist as e:
            return HttpResponse("No data available")
        choices = ((movie.title, movie.title) for movie in movies)
        context = {'form': UpdateForm(choices)}
        return render(request, 'ex07/update.html', context)
        