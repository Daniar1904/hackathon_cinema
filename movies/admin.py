from django.contrib import admin
from .models import Movie, Tag, Favorites


admin.site.register(Movie)
admin.site.register(Tag)
admin.site.register(Favorites)
