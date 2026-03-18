from django.db import models
from django.contrib.auth.models import User

class GameScore(models.Model):

    LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES
    )
    score = models.IntegerField(default=0)
    time_taken = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.score}"
