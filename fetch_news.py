import feedparser
import json
import hashlib

# Liste élargie de flux RSS de gros et petits médias
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
    "Futura Sciences": "https://www.futura-sciences.com/rss/actualites.xml",
    "Franceinfo": "https://www.franceinfo.fr/titre/rss"
}

articles = []

for source, url in FEEDS.items():
    print(f"Récupération de : {source}...")
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:  # Prend les 20 derniers articles de chaque média
            title = entry.get("title", "Sans titre")
            link = entry.get("link", "")
            date = entry.get("published", entry.get("updated", "Date inconnue"))
            summary = entry.get("summary", entry.get("description", ""))
            
            # ID unique basé sur le lien pour éviter les doublons
            article_id = hashlib.md5(link.encode()).hexdigest()
            
            articles.append({
                "id": article_id,
                "source": source,
                "title": title,
                "link": link,
                "date": date,
                "summary": summary
            })
    except Exception as e:
        print(f"Erreur pour {source}: {e}")

# Enregistre le résultat dans le fichier articles.json
with open("articles.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print(f"Terminé ! {len(articles)} articles récupérés au total.")
