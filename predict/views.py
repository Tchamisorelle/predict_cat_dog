from django.shortcuts import render, redirect
from .models import food_quotidien, RepasForm

from datetime import timedelta





def make_prediction(jour_semaine):
    # Sélectionner tous les aliments de la base de données correspondant au jour de la semaine
    aliments = food_quotidien.objects.filter(jour__icontains=jour_semaine)

    # Vérifier si la liste des aliments est vide
    if not aliments:
        return None  # Aucun aliment disponible pour ce jour de la semaine

    # Créer un dictionnaire pour stocker les probabilités et les valeurs des champs associés à chaque aliment
    probabilites = {}
    champs_valeurs = {}

    # Calculer la probabilité en fonction du nombre d'apparitions de chaque aliment et stocker les valeurs des champs
    for aliment in aliments:
        apparitions = food_quotidien.objects.filter(aliment=aliment.aliment).count()
        probabilite = apparitions
        probabilites[aliment.aliment] = probabilite

        champs_valeur = {
            'liquide': aliment.liquide,
            'fruit': aliment.fruit,
            'maladie': aliment.maladie
        }
        champs_valeurs[aliment.aliment] = champs_valeur

    # Trouver les 4 aliments avec les probabilités les plus élevées
    aliments_predire = sorted(probabilites, key=probabilites.get, reverse=True)[:4]

    # Vérifier si les aliments trouvés ont été consommés à la date précédente
    aliments_probabilites = []
    for aliment_predire in aliments_predire:
        aliment = food_quotidien.objects.filter(aliment=aliment_predire).first()
        if aliment:
            date_precedente = aliment.date - timedelta(days=1)
            aliment_precedent = food_quotidien.objects.filter(aliment=aliment.aliment, date=date_precedente).first()
            if not aliment_precedent:
                aliment_probabilite = {
                    'aliment': aliment.aliment,
                    'liquide': aliment.liquide,
                    'fruit': aliment.fruit,
                    'maladie': aliment.maladie,
                    'probabilite': probabilites[aliment.aliment]
                }
                aliments_probabilites.append(aliment_probabilite)

    return aliments_probabilites


def jour_suivant(jour_semaine):
    jours_semaine = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    index_jour = jours_semaine.index(jour_semaine.lower())
    index_suivant = (index_jour + 1) % len(jours_semaine)
    return jours_semaine[index_suivant]


def page_index(request):
    if request.method == 'POST':
        jour_semaine = request.POST.get('jour_semaine')
        aliments_predire = make_prediction(jour_semaine)

        if aliments_predire:
            return render(request, 'index.html', {'aliments_predire': aliments_predire})
        else:
            message = "Aucun aliment à prédire n'a été trouvé pour ce jour de la semaine."
            return render(request, 'index.html', {'message': message})

    return render(request, 'index.html')



from .models import predict_collect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def food_quotidien_personnel(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        aliment = request.POST.get('aliment')
        boisson = request.POST.get('boisson')
        fruit = request.POST.get('fruit')
        email = request.POST.get('email')
        maladie = request.POST.get('maladie')

        try:
            validate_email(email)
        except ValidationError:
            # Gérer l'erreur si l'adresse e-mail n'est pas valide
            return render(request, 'tableau_de_bord.html', {'error_message': 'Adresse e-mail invalide'})


        # Créez une instance du modèle Collect et enregistrez les valeurs dans la base de données
        Collect = predict_collect.objects.create(nom=nom, aliment=aliment, boisson=boisson, fruit=fruit, email=email, maladie=maladie)
        Collect.save()

        return redirect('food_quotidien_personnel')  # Redirigez l'utilisateur vers la page d'index après l'enregistrement

    return render(request, 'food_quotidien_personnel.html')

def formulaire(request):
    return render(request, 'food_quotidien_personnel.html')


def process_repas(request):
    if request.method == 'POST':
        form = RepasForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            repas = form.cleaned_data['repas']  
            repas_precedents = []
            liste_repas = list(predict_collect.objects.filter(email=email, aliment = repas))
            # Recherchez les repas correspondants dans la base de données
            for repa in liste_repas:
                repas_precedents.extend(list(predict_collect.objects.filter(email=email, date__lt = repa.date).order_by('-date'))[:1])

            # Vérifiez s'il y a un repas avec un champ maladie non vide

            danger = None
            for repas_precedent in repas_precedents:
                if repas_precedent.maladie:
                    danger = repas_precedent
                    break
            
            context = {
                'repas_precedents': repas_precedents,
                'danger': danger
            }
            
            return render(request, 'result.html', context)
    else:
        form = RepasForm()

    return render(request, 'food_quotidien_personnel.html', {'form': form})

def form(request):
    return render(request, 'form.html')

def resultat(request):
    return render(request, 'result.html')

def result(request):
    return render(request, 'result.html')

