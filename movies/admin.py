from django.contrib import admin

from .models import Genre, Country, Movie, Review, Person

admin.site.register((Genre, Country, Movie, Review, Person))
