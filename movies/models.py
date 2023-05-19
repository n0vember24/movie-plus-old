from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.db.models import (
    Model, CharField, SlugField, TextField, ForeignKey, SET_NULL, SmallIntegerField,
    DateTimeField, TextChoices, ImageField, CASCADE, FileField, ManyToManyField, TimeField, IntegerChoices, DateField
)
from django.utils.text import slugify

from users.models import User


class Genre(Model):
    title = CharField(max_length=50)
    slug = SlugField(unique=True, max_length=100)
    description = TextField(max_length=300)


class Country(Model):
    name = CharField(max_length=100)
    alpha = SlugField(unique=True, max_length=3)

    class Meta:
        verbose_name_plural = 'Countries'


class Movie(Model):
    allowed_video_extensions = ['mp4', 'mkv', 'avi', 'mov', 'webm']

    class AgeLimitChoices(IntegerChoices):
        FOR_ALL = 0
        FOR_TEENS = 12
        FOR_ADULTS = 18

    class LanguageChoice(TextChoices):
        UZ = 'uz', 'Uzbek'
        RU = 'ru', 'Russian'
        EN = 'en', 'English'

    class MovieTypeChoices(TextChoices):
        FREE = 'free', 'Free'
        SUBSCRIPTION = 'subs', 'Subscription'
        PAID = 'paid', 'Paid'

    title = CharField(max_length=100)
    slug = SlugField(unique=True, max_length=100)
    trailer = FileField(upload_to='video/trailers/', validators=[FileExtensionValidator(allowed_video_extensions)])
    movie = FileField(upload_to='video/movies/', validators=[FileExtensionValidator(allowed_video_extensions)])
    genres = ManyToManyField('movies.Genre')
    countries = ManyToManyField('movies.Country')
    duration = TimeField()
    age_limit = SmallIntegerField()
    year = DateField()
    language = CharField(max_length=10, choices=LanguageChoice.choices, default=LanguageChoice.UZ)
    type = CharField(max_length=10, choices=MovieTypeChoices.choices, default=MovieTypeChoices.FREE)
    persons = ManyToManyField('movies.Person')


class Review(Model):
    movie = ForeignKey('movies.Movie', CASCADE)
    author = ForeignKey(User, SET_NULL, null=True)
    text = CharField(max_length=250, null=True, blank=True)
    rate = SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    pub_date = DateTimeField(auto_now_add=True)


class Person(Model):
    class JobTypes(TextChoices):
        DIRECTOR = 'director', 'Director'
        ACTOR = 'actor', 'Actor'
        PRODUCER = 'producer', 'Producer'
        OPERATOR = 'operator', 'Operator'
        SCREENWRITER = 'screenwriter', 'Screen Writer'

    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)
    job = CharField(max_length=20, choices=JobTypes.choices, default=JobTypes.ACTOR)
    photo = ImageField(upload_to='images/persons/')
    slug = SlugField(unique=True, max_length=200)
    biography = CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.slug = f'{slugify(self.first_name)}-{slugify(self.last_name)}'
        self.save(*args, **kwargs)
