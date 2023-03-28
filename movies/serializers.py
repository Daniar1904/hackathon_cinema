from rest_framework import serializers
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


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['movie'] = instance.movie()
        return repr
