from django.db import models
from django import forms

# Create your models here.
class food_quotidien(models.Model):
    date = models.DateField()
    jour = models.CharField(max_length=15)
    aliment = models.CharField(max_length=50)
    liquide = models.CharField(max_length=20, null=True, blank=True)
    fruit = models.CharField(max_length=20, null=True, blank=True)
    maladie = models.CharField(max_length=30, null=True, blank=True)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.date} - {self.aliment}"
    class Meta:
        db_table = 'food_quotidien' #indiquer que la table existe dns la bd
    

class predict_collect(models.Model):
    nom = models.CharField(max_length=30)
    aliment = models.CharField(max_length=50)
    boisson = models.CharField(max_length=30, null=True, blank=True)
    fruit = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=50)
    date = models.DateTimeField(auto_now=True)
    id = models.AutoField(primary_key=True)
    maladie = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nom
    class Meta:
        db_table = 'predict_collect'

class RepasForm(forms.Form):
    email = forms.EmailField()
    repas = forms.CharField(max_length=100)

