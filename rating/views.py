from rest_framework import mixins, permissions
from rest_framework.generics import GenericAPIView, CreateAPIView
from movies.permissions import IsAuthor
from . import serializers

from rating.models import Review


class UpdateDestroyAPIView(mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ReviewCreateApiView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewUpdateSerializer
    permission_classes = (permissions.IsAuthenticated, IsAuthor)




