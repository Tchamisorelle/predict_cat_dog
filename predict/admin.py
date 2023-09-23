from django.contrib import admin

# Register your models here.
from .models import food_quotidien, predict_collect

class FoodQuotidienAdmin(admin.ModelAdmin):
    list_display = ['date', 'jour', 'aliment', 'liquide', 'fruit', 'maladie', 'id']

class CollectAdmin(admin.ModelAdmin):
    list_display = ['nom', 'aliment', 'boisson', 'fruit', 'email', 'date', 'id', 'maladie']

admin.site.register(food_quotidien, FoodQuotidienAdmin)
admin.site.register(predict_collect, CollectAdmin)
class ChoiceInline(admin.TabularInline):
    list_display = ['nom', 'aliment', 'boisson', 'fruit', 'email', 'date', 'id', 'maladie']

