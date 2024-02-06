from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
from collections import defaultdict

class Scraper(ABC):
    def __init__(self):
        self.results = defaultdict(list)
    
    @property
    @abstractmethod
    def config(self):
        pass

    def runScrape(self):
        for url in self.config['urls']:
            try:
                soup = self.requestSite(url)
            except:
                print('fail')
            self.scrapeData(soup)

    def requestSite(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    
    def printResults(self):
        print(self.results)

    @abstractmethod
    def scrapeData(self, soup):
        pass

class CardShopLive(Scraper):
    @property
    def config(self):
        return {
        'urls': ['https://cardshoplive.com/collections/pokemon?page=1'],
        'collectionMap': {
            'paradox rift': 'PAR',
            'obsidian flames': 'OBF',
            '151': 'MEW',
            'paldean fates': 'PAF',
            'temporal forces': 'TEF',
            'scarlet & violet': 'SVI', # must be after all SVI expansions
            'celebrations': 'CEL',
            'fusion strike': 'FST',
            'brilliant stars': 'BRS',
            'astral radiance': 'ASR'
        },
        'packCount': {
            'elite trainer box': 8,
            '10 packs': 10, # don't want 10 pack bundles, too hard to handle multi
            '3 pack': 3,
            'booster bundle': 36,
            'sleeved booster pack': 1,
            'checklane blister': 1,
            'ultra premium': 16,
        }
    }

    def scrapeData(self, soup):
        productCards = soup.find_all('div', class_='productCard__card')
        for productCard in productCards:
            title = productCard.find(class_='productCard__title').text.strip().lower()
            collectionKey = None
            for collection, key in self.config['collectionMap'].items():
                if collection in title:
                    collectionKey = key
                    break
            packCount = None
            for packType, count in self.config['packCount'].items():
                if packType in title:
                    packCount = count
                    break
            # remove dollar sign and USD
            price = float(productCard.find(class_='productCard__price').text.strip().split(' ')[0][1:])
            inStock = not productCard.find(class_='productCard__button productCard__button--outOfStock')
            print(title, collectionKey, packCount, price, inStock)
            if collectionKey and packCount:
                self.results[collectionKey].append((title, packCount, count, price, inStock))