from django.conf import settings
from django.http import HttpRequest, HttpResponse
import psycopg2


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
                        CREATE TABLE ex00_movies(
                            title VARCHAR(64) UNIQUE NOT NULL,
                            episode_nb INT PRIMARY KEY,
                            opening_crawl TEXT,
                            director VARCHAR(32) NOT NULL,
                            producer VARCHAR(128) NOT NULL,
                            release_date DATE NOT NULL
                            );
                        """)
        return HttpResponse('OK')
    except Exception as e:
        return HttpResponse(e)
