from django.db.models import Avg
from rest_framework import serializers

import movies
from rating.serializers import ReviewSerializer
from .models import Movie, Tag, Like, Favorites


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tag'] = [i.name for i in instance.tag.all()]
        representation['likes_count'] = instance.likes.count()
        return representation


class LikeSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField()

    class Meta:
        model = Like
        fields = '__all__'
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        like = Like.objects.create(author=user, **validated_data)
        return like


class MovieListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Movie
        fields = ('title', 'image')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        return repr


class MovieSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    owner = serializers.ReadOnlyField(source='owner.id')
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        fields = 'all'

    @staticmethod
    def get_stats(instance):
        stars = {'5': instance.reviews.filter(rating=5).count(), '4': instance.reviews.filter(rating=4).count(),
                 '3': instance.reviews.filter(rating=3).count(), '2': instance.reviews.filter(rating=2).count(),
                 '1': instance.reviews.filter(rating=1).count()}
        return stars

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))
        rating = repr['rating']
        rating['ratings_count'] = instance.reviews.count()
        repr['stats'] = self.get_stats(instance)
        return repr

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['movie'] = instance.movie()
        return repr

