from rest_framework import generics
from .models import Movie, Like
from .serializers import MovieSerializer, LikeSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

class MovieListView(generics.ListAPIView):
    """вывод списка фильмов"""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = MovieSerializer(queryset, many=True)
        return Response(serializer.data)


class MovieDetailView(generics.RetrieveAPIView):
    """вывод фильма"""

    def get(self, request, pk=None):
        queryset = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(queryset)
        return Response(serializer.data)
