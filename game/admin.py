from django.contrib import admin
from .models import GameScore


@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "score",
        "time_taken",
        "level",
        "created_at",
    )

    list_filter = (
        "level",
        "created_at",
    )

    search_fields = (
        "user__username",
    )

    ordering = ("-created_at",)
