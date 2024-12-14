import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import argparse
from io import BytesIO
from PIL import Image
import random
import time

BASE_URL = "https://www.novelfulll.com"

# A list of User-Agent strings to rotate so we don't get blocked
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
]

HEADERS = {
        "User-Agent": random.choice(USER_AGENTS) 
    }

def download_chapters(base_url, foldername):
    pagination = 1 # handle pagination
    chapter_links = [] # list to store all chapter links, preserving order

    while(True):
        url = f"{base_url}?page_num={pagination}"
        print(f"\t╰┈➤ Fetching {url}")

        response = requests.get(url, headers=HEADERS)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"❌ Failed to fetch {url}: {e}")
            break

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        chapter_list_div = soup.find('div', id='list-chapter')
        if chapter_list_div:
            content_links = [a['href'] for a in chapter_list_div.find_all('a', href=True) if 'content' in a['href']]
            
            if not content_links:
                print("\t\t╰┈➤ No content links found.")
                break

            print(f"\t\t╰┈➤ Found {len(content_links)} chapter(s) on page {pagination}")

            for link in content_links:
                if link not in chapter_links:
                    chapter_links.append(link)
        else:
            print("⚠️  No (more) chapters found.")
            break

        pagination = pagination + 1

    print(f"📚 Total chapters found: {len(chapter_links)}")
    print("📥 Downloading chapters...")

    for idx, content_link in enumerate(chapter_links):
        ch = str((len(chapter_links)-idx))
        download_images(f"{BASE_URL}{content_link}", ch, ch)

        delay = random.uniform(2, 5)
        print(f"⏳ Sleeping for {delay:.2f} seconds...")
        time.sleep(delay)


def download_images(url, foldername, chapter_nr = ""):
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')

    os.makedirs(foldername, exist_ok=True)

    for img_tag in img_tags:
        img_url = img_tag.get('data-src')
        if not img_url:
            continue
        
        img_name = f"{img_tags.index(img_tag) + 1:01}.png"
        original_img_extension = os.path.basename(img_url).split('.')[-1]

        try:
            img_data = requests.get(img_url, headers=HEADERS).content
            with open(os.path.join(foldername, img_name), 'wb') as img_file:
                # Convert image to PNG if it's not already in PNG format
                if original_img_extension.lower() != 'png':
                    img = Image.open(BytesIO(img_data))
                    img = img.convert('RGB')
                    img.save(os.path.join(foldername, img_name), 'PNG')
                else:
                    img_file.write(img_data)
        except Exception as e:
            print(f"❌ Failed to download {img_url}: {e}")

    print(f"✅ Chapter {chapter_nr} downloaded successfully.")

def main():
    parser = argparse.ArgumentParser(description='Download images from a chapter or all chapters of a comic.')
    
    parser.add_argument('-m', '--mode', type=str, choices=['single', 'all'], required=True,
                        help="Mode of downloading: 'single' for one chapter, 'all' for the entire comic.")
    parser.add_argument('-url', '--url', type=str, required=True, help='URL of the chapter or comic to scrape')
    parser.add_argument('-f', '--foldername', type=str, required=False, help='Name of the folder to save images')
    args = parser.parse_args()

    if not args.url.startswith("http"):
        print("❌ Invalid URL. Please make sure the URL starts with 'http'")
        sys.exit(1)

    if not args.foldername:
        default_folder = "chapter" if args.mode == "single" else "comic"
        print(f"⚠️  No folder name provided. Images will be saved in '{default_folder}' folder.")
        args.foldername = default_folder

    if args.mode == "single":
        print(f"🌐 Scraping single chapter from {args.url}...")
        download_images(args.url, args.foldername)
    elif args.mode == "all":
        print(f"🌐 Scraping all chapters from comic {args.url}...")
        download_chapters(args.url, args.foldername)

    print("🎉 All tasks finished.")


if __name__ == '__main__':
    main()