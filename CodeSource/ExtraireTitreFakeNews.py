# ce fichier permet d'extraire le titre de l'article a partir de l'image

import cv2
import pytesseract
import json
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import numpy as np
import os

service = Service("C:\\Program Files (x86)\\chromedriver.exe")  
driver = webdriver.Chrome(service=service)

titres = []

def save_results():
    with open("Titres.json", 'w', encoding='utf-8') as file:
        json.dump(titres, file, ensure_ascii=False, indent=4)
    print(f"Les résultats ont été sauvegardés dans Titres3.json.")

try:
    with open("Titres.json", 'r', encoding='utf-8') as file:
        titres = json.load(file)
    print(f"Le fichier Titres.json existe déjà. Reprise à partir de {len(titres)} éléments.")
except FileNotFoundError:
    print(f"Le fichier Titres.json n'existe pas. Début du traitement.")

def extract_superimposed_text(image_path):
    
    # Extraire le texte superposé d'une image donnée.
    
    # Charger l'image avec OpenCV
    driver.get(image_path)  
    time.sleep(2)  

       
    screenshot_as_bytes = driver.get_screenshot_as_png()  # Capture d'écran sous forme de flux binaire
    image_array = np.frombuffer(screenshot_as_bytes, np.uint8)

    # Lire l'image à partir du tableau avec OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Appliquer un seuillage pour isoler les zones claires
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Trouver les contours des zones blanches
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialiser le texte extrait
    extracted_text = ""

    for contour in contours:
        # Obtenir les coordonnées du rectangle englobant
        x, y, w, h = cv2.boundingRect(contour)

        # Filtrer les petites zones non pertinentes
        if w > 50 and h > 20:  # Ajuster selon vos besoins
            # Extraire la région d'intérêt (ROI)
            roi = image[y:y+h, x:x+w]

            # Appliquer l'OCR sur la région d'intérêt
            text = pytesseract.image_to_string(roi, config='--psm 6')
            extracted_text += text.strip() + "\n"

    return extracted_text

def process_images_from_json(json_path):
    
    # Lire les chemins des images à partir d'un fichier JSON et extraire le texte de chaque image.
    
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    
    for element in data[len(titres):]:  
        if isinstance(element, dict): 
            for key, value in element.items(): 
                url = value
                if url:  
                    print(f"Texte extrait de {url}:")
                    text = extract_superimposed_text(url)  
                    title = {
                        "title": text, 
                    }
                    titres.append(title)  # Ajouter le titre extrait à la liste
                    print(f"Texte extrait :\n{text}\n")
                   
                    save_results()  # Appeler la fonction pour sauvegarder les résultats
                    print("-" * 50)
                else:
                    print("Aucun lien trouvé dans cet élément.")
        else:
            print(f"L'élément n'est pas un dictionnaire : {element}")


    # Parcourir chaque chemin d'image et extraire le texte
    


json_path = "ImgsLink.json"  
process_images_from_json(json_path)


