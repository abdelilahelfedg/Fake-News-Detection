# Ce fichier permet d'extraire les liens vers les pages contenant les fake news et pour chaque page contenant une article le script extraire et stocke le lien vers l'image


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time

# Chemin vers votre WebDriver (ajustez en fonction de votre système)
webdriver_path = "C:\\Program Files (x86)\\chromedriver.exe"  


input_file = 'fakeNews.json'
output_file = 'ImgsLink.json'

# Charger les liens depuis un fichier JSON
with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

base_url = "https://factcheck.afp.com/"


# Initialiser le WebDriver
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service)

# Liste pour stocker les résultats
results = []

def save_results():
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    print(f"Les résultats ont été sauvegardés dans {output_file}.")

try:
    with open(output_file, 'r', encoding='utf-8') as file:
        results = json.load(file)
    print(f"Le fichier {output_file} existe déjà. Reprise à partir de {len(results)} éléments.")
except FileNotFoundError:
    print(f"Le fichier {output_file} n'existe pas. Début du traitement.")

for element in data[len(results):]:
    try:
        link = element.get('url')
        print(f"Traitement du lien : {link}")
        # Accéder à la page
        driver.get(link)
        time.sleep(2)  

        # Extraire la première balise <img> et son attribut src
        img_tag = driver.find_element(By.CLASS_NAME, "img-fluid")
        src = img_tag.get_attribute("src")

        if src:
            full_src = base_url + src if not src.startswith("http") else src
            results.append({link: full_src})
            print(f"Lien de l'image : {full_src}")
            print(len(results))
        else:
            results.append({link: None})
            print("Aucune balise <img> trouvée.")
        save_results()
    except Exception as e:
        print(f"Erreur pour le lien {link}: {e}")
        results.append({link: None})



print(f"Extraction terminée. Les résultats ont été enregistrés dans {output_file}.")


driver.quit()
