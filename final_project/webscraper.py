import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import pandas as pd

BASE_URL = "https://www.azlyrics.com"

# List of User-Agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/537.36",
]

# Session object to persist cookies and headers
session = requests.Session()

def get_soup(url):
    """Fetch a URL with randomized headers and delay."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an error for HTTP errors
        time.sleep(random.uniform(1, 3))  # Random delay between requests
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


# Step 1: Get artist index links
soup = get_soup(BASE_URL)
if not soup:
    print("Failed to retrieve base page.")
    exit()

artist_links = [
    link.get('href') for link in soup.find_all('a', class_='btn btn-menu') if link.get('href')
]

# Step 2: Get artist pages
unique_artist_links = set()
for link in artist_links:
    url = "https:" + link if link.startswith("//") else BASE_URL + link
    soup = get_soup(url)
    if not soup:
        continue

    division_soup = soup.find_all('div', class_='col-sm-6 text-center artist-col')
    artist_links = [a.get('href') for div in division_soup for a in div.find_all('a')]
    unique_artist_links.update(artist_links)




# Step 3: Get song links from artist pages
song_final_links = []
for link in unique_artist_links:
    url = "https:" + link if link.startswith("//") else BASE_URL + link
    soup = get_soup(url)
    if not soup:
        continue

    song_links = [
        a.get('href') for a in soup.find_all('a', href=True) if 'lyrics' in a.get('href')
    ]
    song_final_links.extend(song_links)

# Normalize song URLs
song_final_links = [
    BASE_URL + link if not link.startswith("http") else link for link in song_final_links
]

# Step 4: Scrape lyrics from song pages
final_download = []
for link in song_final_links:
    soup = get_soup(link)
    if not soup:
        continue

    lyrics_div = soup.find('div', class_=False, id=False)  # Lyrics are often in an unclassed div
    if lyrics_div:
        lyrics = lyrics_div.get_text(strip=True, separator="\n")
        final_download.append(lyrics)
df = pd.DataFrame(final_download)
df.to_csv("lyrics.csv", index=False, encoding="utf-8")
        

