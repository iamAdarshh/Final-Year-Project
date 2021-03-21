from django.db import models
from django.contrib.auth.models import User

# Create your models here.

'''
    This is Feedback model.
    It will store name, email, contact and message from the user.
    It return name of user to admin.
'''
class Feedback(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    contact = models.CharField(max_length=10)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

'''
    This is ReviewMovie model.
    It will store reviews from user.
    It will store moveid, userid, userreview, date, sentiment and probability.
'''
class ReviewMovie(models.Model):
    movieid = models.IntegerField(null=False)
    userid = models.CharField(max_length=100, null=True)
    review = models.CharField(max_length = 500, null=True)
    date = models.DateTimeField(auto_now_add=True)
    sentiment = models.IntegerField(null=True)
    probability = models.FloatField(null=True)

    def __str__(self):
        return self.review

'''
    This is ReviewSeries model.
    It will store reviews from user.
    It will store seriesid, userid, userreview, date, sentiment and probability.
'''
class ReviewSeries(models.Model):
    seriesid = models.IntegerField(null=False)
    userid = models.CharField(max_length=100, null=True)
    review = models.CharField(max_length = 500, null=True)
    date = models.DateTimeField(auto_now_add=True)
    sentiment = models.IntegerField(null=True)
    probability = models.FloatField(null=True)

    def __str__(self):
        return self.review