"""
URL configuration for prediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from predict.views import page_index, food_quotidien_personnel, formulaire, process_repas, form, resultat, result

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', page_index, name='index'),
    path('food-quotidien-personnel/', food_quotidien_personnel, name='food_quotidien_personnel'),
    path('formulaire/', formulaire, name='formulaire'),   
    path('resultat/', process_repas, name='process_repas'),
    path('result/', result, name='result'),
    path('predict_cat_dog/', include('predict_cat_dog.urls')),
]






