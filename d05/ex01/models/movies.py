from django.db import models

class Movies(models.Model):
    db_table = 'ex01_movies'
    title = models.CharField('title', max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField('episode_nb', primary_key=True)
    opening_crawl = models.TextField('opening_crawl', null=True)
    director = models.CharField('director', max_length=32, null=False)
    producer = models.CharField('producer', max_length=128, null=False)
    release_date = models.DateField('release_date', null=False)

    def __str__(self) -> str:
        return self.title
