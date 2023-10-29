from django.contrib import admin
from homepage.models import Feedback

# Register your models here.
@admin.register(Feedback)
class feedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback']