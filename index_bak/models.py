from django.db import models

# Create your models here.
class User(models.Model):
    uname = models.CharField(max_length=30)
    upwd = models.CharField(max_length=30)
    uphone = models.CharField(max_length=11)
    headimg = models.ImageField(null=True)

    def __repr__(self):
        return '<User %s>' % self.name

    def __str__(self):
        return '<User %s>' % self.name


