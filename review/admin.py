from django.contrib import admin
from review.models import Review

# Register your models here.
@admin.register(Review)
class reviewAdmin(admin.ModelAdmin):
   list_display=['book_title',
                'reviewer_name',
                'review_score',
                'review_summary',
                'review_text', 
                'review_date',]
