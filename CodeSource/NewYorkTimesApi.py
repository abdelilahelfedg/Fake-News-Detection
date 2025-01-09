import requests
import json
import os
import time

api_key = "es1AgEzFlonKS0Qn05UjbRBq0kAfG8ha"
base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"

query = "australia"
articles = []

if os.path.exists("TrueNews.json"):
    with open("TrueNews.json", "r", encoding="utf-8") as file:
        articles = json.load(file)
# Définir le nombre maximum de pages à récupérer (chaque page = 10 articles)
max_pages = 90

for page in range(80,max_pages):
    params = {
        "q": query,
        "page": page,
        "api-key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Ajouter les articles à la liste
        docs = data.get("response", {}).get("docs", [])
            
        for doc in docs:
            article = {
                "title": doc.get("headline", {}).get("main"),
                "url": doc.get("web_url"),
                "snippet": doc.get("snippet"),
                "lead_paragraph": doc.get("lead_paragraph"),
                "pub_date": doc.get("pub_date"),
            }
            articles.append(article)
    else:
        print(f"Erreur avec la page {page}: {response.status_code}")
    
    time.sleep(1)


with open("TrueNews.json", "w", encoding="utf-8") as file:
    json.dump(articles, file, indent=4, ensure_ascii=False)
    

print(f"Nombre d'articles récupérés : {len(articles)}")
