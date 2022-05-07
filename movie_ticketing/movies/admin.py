from django.contrib import admin

from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "created_at", "updated_at"]
    search_fields = ["title"]
