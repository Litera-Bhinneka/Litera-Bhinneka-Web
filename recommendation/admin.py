from django.contrib import admin
from .models import Recommendation
from .models import OutsideRecommendation

# Register your models here.
@admin.register(Recommendation)
class recommendationAdmin(admin.ModelAdmin):
   list_display=['book_title',
                'another_book_title',
                'recommender_name',
                'recommendation_scale',
                'description',
                'recommendation_date',]
   
admin.site.register(OutsideRecommendation)