from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
import psycopg2

from .forms import UpdateForm


def init(request: HttpRequest):
    try:
        conn = psycopg2.connect(database=settings.DATABASES['default']['NAME'],
                                user=settings.DATABASES['default']['USER'],
                                password=settings.DATABASES['default']['PASSWORD'],
                                host=settings.DATABASES['default']['HOST'],
                                port=settings.DATABASES['default']['PORT'])

        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                        CREATE TABLE ex06_movies(
                            title VARCHAR(64) UNIQUE NOT NULL,
                            episode_nb INT PRIMARY KEY,
                            opening_crawl TEXT,
                            director VARCHAR(32) NOT NULL,
                            producer VARCHAR(128) NOT NULL,
                            release_date DATE NOT NULL,
                            created TIMESTAMP NOT NULL DEFAULT NOW(),
                            updated TIMESTAMP NOT NULL DEFAULT NOW()
                            );
                        CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                        RETURNS TRIGGER AS $$
                        BEGIN
                        NEW.updated = now();
                        NEW.created = OLD.created;
                        RETURN NEW;
                        END;
                        $$ language 'plpgsql';
                        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                        update_changetimestamp_column();
                        """)
        return HttpResponse('OK')
    except Exception as e:
        return HttpResponse(e)


def populate(request):
    try:
        conn = psycopg2.connect(database=settings.DATABASES['default']['NAME'],
                                user=settings.DATABASES['default']['USER'],
                                password=settings.DATABASES['default']['PASSWORD'],
                                host=settings.DATABASES['default']['HOST'],
                                port=settings.DATABASES['default']['PORT'])

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

        INSERT = """
            INSERT INTO ex06_movies (episode_nb, title, director, producer, release_date)
            VALUES (%s, %s, %s, %s, %s);
        """
        result = []
        with conn.cursor() as cur:
            for el in movies:
                try:
                    cur.execute(INSERT, [
                        el['episode_nb'],
                        el['title'],
                        el['director'],
                        el['producer'],
                        el['release_date']
                    ])
                    result.append("OK")
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    result.append(e)
        return HttpResponse("<br/>".join(str(el) for el in result))
    except Exception as e:
        return HttpResponse(e)


def display(request):
    try:
        conn = psycopg2.connect(database=settings.DATABASES['default']['NAME'],
                                user=settings.DATABASES['default']['USER'],
                                password=settings.DATABASES['default']['PASSWORD'],
                                host=settings.DATABASES['default']['HOST'],
                                port=settings.DATABASES['default']['PORT'])

        REQUEST = "SELECT * FROM ex06_movies ORDER BY episode_nb;"
        with conn:
            with conn.cursor() as cur:
                cur.execute(REQUEST)
                movies = cur.fetchall()
            if not movies:
                return HttpResponse("No data available")
        return render(request, 'ex06/display.html', {'movies': movies})
    except Exception as e:
        return HttpResponse("No data available")


def update(request):
    conn = psycopg2.connect(database=settings.DATABASES['default']['NAME'],
                            user=settings.DATABASES['default']['USER'],
                            password=settings.DATABASES['default']['PASSWORD'],
                            host=settings.DATABASES['default']['HOST'],
                            port=settings.DATABASES['default']['PORT'])

    if request.method == 'POST':
        RESPONSE = "SELECT title FROM ex06_movies ORDER BY episode_nb;"
        try:
            with conn.cursor() as cur:
                cur.execute(RESPONSE)
                movies = cur.fetchall()
            choices = ((movie[0], movie[0]) for movie in movies)
        except Exception as e:
            return HttpResponse(e)
        data = UpdateForm(choices, request.POST)
        UP_RESPONSE = "UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s;"
        if data.is_valid():
            try:
                with conn.cursor() as cur:
                    cur.execute(UP_RESPONSE, [data.cleaned_data['opening_crawl'], data.cleaned_data['title']])
                    conn.commit()
            except Exception as e:
                return HttpResponse(e)
        return redirect('update')
    else:
        RESPONSE = "SELECT * FROM ex06_movies ORDER BY episode_nb;"
        try:
            with conn.cursor() as cur:
                cur.execute(RESPONSE)
                movies = cur.fetchall()
            context = {
                'form': UpdateForm(choices=(
                    (movie[0], movie[0]) for movie in movies
                ))
            }
            return render(request, 'ex06/update.html', context)
        except Exception as e:
            return HttpResponse(e)