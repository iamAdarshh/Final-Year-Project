from django.contrib import admin
from .models import Feedback, ReviewMovie, ReviewSeries

# Register your models here.
admin.site.site_header = "RHub Admin Dashboard"

class ReviewMovieAdmin(admin.ModelAdmin):
    list_display = ('movieid','review', 'date')

class ReviewSeriesAdmin(admin.ModelAdmin):
    list_display = ('seriesid','review', 'date')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')

admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(ReviewMovie, ReviewMovieAdmin)
admin.site.register(ReviewSeries, ReviewSeriesAdmin)
