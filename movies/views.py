from rest_framework.viewsets import ModelViewSet

from movies.models import Movie
from movies.permissions import IsAdminOrReadOnly
from movies.serializers import MovieSerializer


class MovieView(ModelViewSet):
	queryset = Movie.objects.all()
	serializer_class = MovieSerializer
	permission_classes = IsAdminOrReadOnly,
