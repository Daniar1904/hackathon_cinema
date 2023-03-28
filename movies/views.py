from rest_framework import generics, response

import movies
from rating.serializers import ReviewActionSerializer
from rest_framework import generics, permissions
from .models import Movie, Like
from .serializers import MovieSerializer, LikeSerializer, FavoriteSerializer
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


class FavoriteCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        serializer.save(owner=self.request.user)



@action(['GET', 'POST'], detail=True)
def reviews(self, request, pk):
    product = self.get_object()
    if request.method == 'GET':
        reviews = movies.reviews.all()
        serializer = ReviewActionSerializer(reviews, many=True).data
        return response.Response(serializer, status=200)
    else:
        if movies.reviews.filter(owner=request.user).exists():
            return response.Response('You already reviewed this product!', status=400)
        data = request.data
        serializer = ReviewActionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user, product=product)
        return response.Response(serializer.data, status=201)


@action(['DELETE'], detail=True)
def review_delete(self, request, pk):
    movie = self.get_object()
    user = request.user
    if not movie.reviews.filter(owner=user).exists():
        return response.Response('You did not reviewed this product!', status=400)
    review = movie.reviews.get(owner=user)
    review.delete()
    return response.Response('Successfully deleted', status=204)

   

    


        
