from django.shortcuts import render
from keras.models import load_model
import cv2
import numpy as np
import pandas as pd


def image_reco(image):
    max_size = (255, 255)  # Taille maximale souhaitée pour l'image redimensionnée

    # Redimensionner l'image en conservant l'aspect ratio
    resized_image = cv2.resize(image, max_size)
    
    # Convertir l'image en niveaux de gris
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    
    # Normaliser les valeurs des pixels (mise à l'échelle entre 0 et 1)
    normalized_image = gray_image / 255.0
    
    return normalized_image

def perform_image_recognition(image):
    model1 = load_model(r"C:\Users\sorel\OneDrive\Bureau\TP_CNN\CNN\cnn_biblo\cnn_biblo\model.h5")
    input_image = image_reco(image)
    input_imag = np.expand_dims(input_image, axis=-1)
    input_imag = np.expand_dims(input_imag, axis=0)
    prediction = model1.predict(input_imag)

    # seuil = 80
    # ss = 50

    # Convertir la prédiction en étiquette
    predicted_label = np.round(prediction[0][0]*100)


    return predicted_label

def accueilir(request):

    return render(request, 'accueil.html')

# def page_accueil(request):
#     if request.method == 'POST':
#         image_file = request.FILES['image_file']
#         image_array = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
#         result = perform_image_recognition(image_array)
#         return result  # Retourner le résultat de la prédiction

def reponse(request):
    if request.method == 'POST':
        image_file = request.FILES['image_file']
        image_array = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        result = perform_image_recognition(image_array)
        seuil = 80
        ss = 50
        # Convertir la prédiction en étiquette
        if result <= ss:
            resu =  "L'image est un chat à {}%"
            resul = result
            result = resu.format(resul)
        elif (ss < result <= seuil) :
            resu = "L'image est un chien à {}%"
            resul = result
            result = resu.format(resul)
        elif (result > seuil):
            resu = "L\'image n\'est ni un chien ni un chat à {}%"
            resul = result
            result = resu.format(resul) 
        return render(request, 'reponse.html', {'result': result})  # Renvoyer le résultat dans la page reponse.html
    else:
        return render(request, 'reponse.html')  # Si la méthode de requête n'est pas POST, simplement renvoyer la page reponse.html

def accueil_graine(request):
    if request.method == 'POST':
        # Récupérer le fichier uploadé à partir de la requête
        uploaded_file = request.FILES['image_file']

        # Charger le fichier Excel avec plusieurs données
        data_file = pd.ExcelFile(uploaded_file)

        model1 = load_model(r"C:\Users\sorel\OneDrive\Bureau\Bureau\modele_graine.h5")

        # Liste pour stocker les résultats des différentes données
        results = []

        # Parcourir chaque feuille du fichier Excel
        for sheet_name in data_file.sheet_names:
            # Charger les données à partir de la feuille courante
            data = data_file.parse(sheet_name, header=0)

            # Supprimer les colonnes indésirables
            col_sup = ['sample', 'sample_genotype']
            data = data.drop(columns=col_sup)

            # Effectuer les prédictions sur les données courantes
            predictions = model1.predict(data)
            predicted_labels = np.argmax(predictions, axis=1)

            # Obtenir les pourcentages correspondants aux probabilités
            probabilities = np.max(predictions, axis=1)
            percentages = probabilities * 100

            # Construire les résultats pour chaque donnée
            for i, (label, percentage) in enumerate(zip(predicted_labels, percentages)):
                if label == 0:
                    result_string = f"Core_Rouge ({percentage:.2f}%)"
                elif label == 1:
                    result_string = f"AB-QTL_Mbalmayo_Vert ({percentage:.2f}%)"
                elif label == 2:
                    result_string = f"AB-QTL_Bafia_Noir ({percentage:.2f}%)"
                elif label == 3:
                    result_string = f"AB-QTL_Nioro_Bleu ({percentage:.2f}%)"
                else:
                    result_string = "Classe Inconnue"

                    # Ajouter le résultat à la liste des résultats avec l'indice de la donnée
                results.append(f"Donnée {i+1} - {result_string}")


        # Passer les résultats au contexte pour l'affichage
        context = {'results': results}
        return render(request, 'accueil_graine.html', context)

    return render(request, 'accueil_graine.html')

