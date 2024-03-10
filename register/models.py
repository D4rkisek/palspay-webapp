from django.db import models


# User initial registration
class Member(models.Model):
    username = models.CharField(max_length=200)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    pwd = models.CharField(max_length=200)

    def __str__(self):
        return self.username
