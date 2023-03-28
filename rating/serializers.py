from rest_framework import serializers
from rating.models import Review


class ReviewActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        movie = attrs['movie']
        user = request.user
        if user.reviews.filter(movie=movie).exists():
            raise serializers.ValidationError('You already reviewed this film')
        return attrs


class ReviewUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    movie = serializers.ReadOnlyField(source='movie.title')

    class Meta:
        model = Review
        fields = '__all__'
