from django.db import models


class Logs(models.Model):
    action_type = [
        (1, "Création"),
        (2, "Modification"),
        (3, "Suppression"),
        (4, "Visite")
    ]

    user_id = models.BigIntegerField()
    username = models.CharField(max_length=200)
    action_type = models.SmallIntegerField(choices=action_type)
    visited_url = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    action_date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.id}, User ID: {self.user_id} Username: {self.username}, Action: {self.action_type}, " \
               f"Date et Heure: {self.action_date_time}," \
               f" Description: {self.description}, Url: {self.visited_url}"
