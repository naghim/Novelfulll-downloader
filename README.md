# NovelFulll Downloader

This project is a web scraper/downloader for NovelFulll, a website that hosts a large collection of novels. This Python script allows you to download images from chapters or an entire comic hosted on [https://www.novelfulll.com](https://www.novelfulll.com). The script can operate in two modes: downloading a single chapter or scraping all chapters from a webcomic.

If you want to download a single chapter, provide a direct link to the chapter. If you want to download all content, then provide a link to the webcomic's page. The script automatically handles pagination to find all chapters. See the [Usage](#usage) section for more information.

The tool converts downloaded images to `PNG` format, ensuring consistent quality. It can be changed to your preferred image format as needed.

## Requirements

- Python 3.x
- Requests library
- BeautifulSoup library
- Pillow

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4 pillow
```

Or install them using the [`requirements.txt`](requirements.txt) by typing the following command in a terminal window: `pip install -r requirements.txt`

## Usage

After cloning the repository, run the script with command-line arguments to specify the download mode, target URL, and output folder.

### Command-line arguments

| Argument        | Description                                                                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-m, --mode`    | Mode of operation: `single` (for one chapter) or `all` (for the entire comic).                                                                       |
| `-url, --url`   | The URL of the chapter or comic to scrape. Must start with `http`.                                                                                   |
| `--f, --folder` | (Optional) The name of the folder to save images. Defaults to `chapter` in case of downloading a single chapter, otherwise the index of the chapter. |

Examples:

#### Download a single chapter

```bash
python downloader.py -m single -url https://www.novelfulll.com/comic/chapter -f my_chapter
```

#### Download all chapters from a comic

```bash
python downloader.py -m all -url https://www.novelfulll.com/comic
```

## Disclaimer

This scraper is for educational purposes only. Please respect the terms of service of NovelFulll and do not use this scraper for any illegal activities.

## Notes

This script relies heavily on the website's structure. If the structure changes, the script will need updates to remain functional. Should you encounter any issues, please report them by opening an issue [here](https://github.com/naghim/Novelfulll-downloader/issues), and I’ll address them promptly.

### Todos

- [ ] Implement parallel downloading.
- [ ] Implement downloading chapter ranges (i.e. 4-11)

---

---

> This script is a part of the **AS-Utils** project — a collection of tools and scripts designed for similar issues. Explore more scripts like this in the [AS-Utils repository](https://github.com/naghim/as-utils). 🚀
