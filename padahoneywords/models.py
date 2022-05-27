from django.db import models

# Create your models here.
from django.db import models

class Sweetwords(models.Model):
    #all the salted ,hashed passwords real and honewywords
    salt = models.CharField(
        max_length=128,
        help_text="The salt that we will use in the users account",
        )
    sweetwords = models.CharField(
        max_length=65536,
        help_text="all the sweetwords including the real and alla the fake",
        )

    class Meta:
        verbose_name_plural = 'sweetwords'

    def __str__(self):
        return self.salt
