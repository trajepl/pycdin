from django.db import models


class Auth(models.Model):
    id = models.IntegerField(max_length = 100)
    password = models.CharField(max_length = 50)

    def __str__(self):
        return str(self.id + self.password)


class Remote(models.Model):
    def __str__(self):
        return self.host
