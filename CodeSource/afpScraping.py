from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os

# Chemin vers ChromeDriver
PATH = "C:\\Program Files (x86)\\chromedriver.exe"
service = Service(PATH)
driver = webdriver.Chrome(service=service)

# URL de la page à scraper
url = "https://factcheck.afp.com/list/regions/Middle-East?page=18"
driver.get(url)

# Attendre le chargement des articles 
wait = WebDriverWait(driver, 10)

# Itérer sur chaque article
index = 0
old_length = 0
j = 19
articles_data = []
if os.path.exists("fakeNews.json"):
    with open("fakeNews.json", "r", encoding="utf-8") as file:
        articles_data = json.load(file)
while True:
    try:
        
        articles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article/a")))
        
        article = articles[index]
        article_url = article.get_attribute("href")  # Récupérer l'URL
        driver.get(article_url)

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

        title = driver.find_element(By.TAG_NAME, "h1").text
        print(f"\nArticle {index + 1} - Titre : {title}")

        try:
            publi_date = driver.find_element(By.CSS_SELECTOR, "li[data-type='created']").text
        except Exception:
            publi_date = "Date non trouvée"
        print(f"Date de publication : {publi_date}")

        try:
            div = driver.find_element(By.XPATH, "//div[@class='wrapper-body']/div")
            paragraphs = div.find_elements(By.TAG_NAME, "p")
            for i in range(min(3, len(paragraphs))):  # Maximum 3 paragraphes ou moins
                print(f"Paragraphe {i + 1} : {paragraphs[i].text}")
            content = [paragraphs[i].text for i in range(min(3, len(paragraphs)))]
        except Exception:
            print("Aucun contenu trouvé pour cet article.")
            content = ["Aucun contenu trouvé pour cet article."]

        articles_data.append({
            "title": title,
            "url": article_url,
            "publication_date": publi_date,
            "content": content,
            "region": "North-America"
        })

        driver.get(url)
        index += 1 
        print(index)
        print(j)
        if index == len(articles):

            url = f"https://factcheck.afp.com/list/regions/Middle-East?page={j}"
            driver.get(url)
            j += 1
            index = 0 
            
    except Exception as e:
        print(f"Erreur lors du traitement de l'article {index + 1} : {e}")
        break

with open("fakeNews.json", "w", encoding="utf-8") as file:
    json.dump(articles_data, file, ensure_ascii=False, indent=4)

print("Données enregistrées dans 'fakeNews.json'.")
print(len(articles_data))

driver.quit()
