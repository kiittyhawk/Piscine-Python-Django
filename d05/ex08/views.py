from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
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
                        CREATE TABLE ex08_planets (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(64) UNIQUE NOT NULL,
                            climate VARCHAR,
                            diameter INT,
                            orbital_period INT,
                            population BIGINT,
                            rotation_period INT,
                            surface_water REAL,
                            terrain VARCHAR(128)
                        );
                        CREATE TABLE ex08_people (
                            id SERIAL PRIMARY KEY,
                            name VARCHAR(64) UNIQUE NOT NULL,
                            birth_year VARCHAR(32),
                            gender VARCHAR(32),
                            eye_color VARCHAR(32),
                            hair_color VARCHAR(32),
                            height INT,
                            mass REAL,
                            homeworld VARCHAR(64) REFERENCES ex08_planets(name)
                        );
                        """)
        return HttpResponse('OK')
    except Exception as e:
        return HttpResponse(e)


def populate(request):
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )

    try:
        with conn.cursor() as cur:
            with open('planets.csv', 'r') as file:
                cur.copy_from(file, 'ex08_planets', sep='\t', null='NULL', columns=(
                'name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain'
            ))
        with conn.cursor() as cur:
            with open('people.csv', 'r') as file:
                cur.copy_from(file, 'ex08_people', sep='\t', null='NULL', columns=(
                'name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld'
            ))
        conn.commit()
        return HttpResponse('OK')
    except Exception as e:
        return HttpResponse(e)


def display(request):
    conn = psycopg2.connect(database=settings.DATABASES['default']['NAME'],
                            user=settings.DATABASES['default']['USER'],
                            password=settings.DATABASES['default']['PASSWORD'],
                            host=settings.DATABASES['default']['HOST'],
                            port=settings.DATABASES['default']['PORT'])

    t_people = 'ex08_people'
    t_planets = 'ex08_planets'

    REQUEST = f"""
        SELECT 
            {t_people}.name,
            {t_people}.homeworld,
            {t_planets}.climate
        FROM 
            {t_planets}
            RIGHT JOIN {t_people}
            ON 
                {t_planets}.name = {t_people}.homeworld
                WHERE
                    {t_planets}.climate LIKE '%windy%'
            ORDER BY {t_people}.name;"""
    try:
        with conn.cursor() as cur:
            cur.execute(REQUEST)
            people = cur.fetchall()
        if not people:
            raise HttpResponse()
        return render(request, 'ex08/display.html', {'people': people})
    except Exception as e:
        return HttpResponse("No data available")
