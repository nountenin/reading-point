from django.db import models


# Create your models here.
class Events(models.Model):
    types = [
        ('events', 'Events'),
        ('ecocitoyenne', 'Ecocitoyenne')
    ]
    title_events = models.CharField(max_length=30)
    image_events = models.ImageField(upload_to="events/images/", null=True, blank=True)
    type = models.CharField(max_length=15, choices=types)
    descriptions = models.TextField()
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{pk} {title_events}  {images_events} {type} {descriptions}".format(
            pk=self.pk,
            title_events=self.title_events,
            images_events=self.image_events,
            type=self.type,
            descriptions=self.descriptions
        )
