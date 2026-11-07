import feedparser
import json
import hashlib
import os

# Liste de dizaines de flux RSS de presse (gros et petits médias)
FEEDS = {
    "Mediapart": "https://www.mediapart.fr/articles/feed",
    "Blast": "https://www.blast-info.fr/rss",
    "Le Figaro": "https://www.lefigaro.fr/rss/figaro_actualites.xml",
    "Le Monde": "https://www.lemonde.fr/rss/une.xml",
    "Libération": "https://www.liberation.fr/arc/outboundfeeds/rss/",
    "Reporterre": "https://reporterre.net/spip.php?page=backend",
    "Les Echos": "https://www.lesechos.fr/rss/rss_une.xml",
    "La Croix": "https://www.la-croix.com/RSS/UNIVERS_WLC.xml",
    "BFMTV": "https://www.bfmtv.com/rss/info/flux-rss/flux-toutes-les-actualites/",
    "Futura Sciences": "https://www.futura-sciences.com/rss/actualites.xml"
}

articles = []

for source, url in FEEDS.items():
    print(f"Récupération de : {source}...")
    feed = feedparser.parse(url)
    
    for entry in feed.entries[:15]:  # Prend les 15 derniers articles par média
        title = entry.get("title", "Sans titre")
        link = entry.get("link", "")
        date = entry.get("published", entry.get("updated", ""))
        summary = entry.get("summary", entry.get("description", ""))
        
        # Identifiant unique basé sur le lien
        article_id = hashlib.md5(link.encode()).hexdigest()
        
        articles.append({
            "id": article_id,
            "source": source,
            "title": title,
            "link": link,
            "date": date,
            "summary": summary,
            "content": summary  # Dans un RSS, le résumé/contenu textuel est fourni
        })

# Sauvegarde dans le fichier articles.json
with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Terminé ! {len(articles)} articles sauvegardés.")
