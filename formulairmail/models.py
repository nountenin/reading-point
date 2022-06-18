from django.db import models


# Create your models here.
# Email
class Email(models.Model):
    email_exp = models.CharField(max_length=500)
    object = models.CharField(max_length=500)
    message = models.TextField()
    created_by = models.IntegerField(default=1)
    modified_by = models.IntegerField(default=1)
    modified_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return "{email} {message}".format(
            email=self.email,
            message=self.message
        )


class Newsletter(models.Model):
    emails = models.EmailField(max_length=100,unique=True)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.pk} {self.emails}'
