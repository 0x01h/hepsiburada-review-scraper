[![Made with Python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# Hepsiburada Review Scraper [![HB Review Scraper](https://img.shields.io/badge/version-1.0.0%20beta-red.svg)](https://github.com/n1rv4n4/hepsiburada-review-scraper/) [![GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
[Hepsiburada](https://www.hepsiburada.com) review/comment and rating scraper. Turkish text dataset creator for data science and NLP projects. Nearly 30M reviews with category and product links can be crawled and used for text classification, sentiment analysis, text mining, FastText models etc. Supported by multithreading, written in Python.

## Prerequisites
`$ pip3 install -r requirements.txt`

## Installation
```
$ git clone https://github.com/0x01h/hepsiburada-review-scraper.git
$ cd hepsiburada-review-scraper
$ python3 hepsiburada.py
```

## Usage
Program provides an human-friendly interactive shell for users.

### Features
- Shutdown computer after finishing: Optional choice for deep and long scrapings.
- Threads: Try to give a proper number. *Recommended value is 64.*
- Timeout: Giving a large number could result in long waiting times, small numbers could lead connection failures. *Recommended time range is 15-30 seconds.*
- Pagination Depth: Maximum number of paginated review pages for each product.

You can track your progress via *progress bars.* `categories.txt`, `products.txt`, `hepsiburada.txt` will be saving to your current directory.

[![Say thanks.](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://www.linkedin.com/in/orçunözdemir/)

**For educational purposes only.**
