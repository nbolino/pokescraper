from src.engines import *
import os

try:
    if os.environ.get('ENV') in ['dev', 'local']:
        from dotenv import load_dotenv
        load_dotenv()
except Exception as err:
    print(err)
    print('Error loading environment variables')
    exit(0)


def main():
    engine = CardShopLive()
    engine.runScrape()
    engine.saveScrapeResults()

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, TypeError, NameError) as err:
        print(err)
        print('Failed to execute main')
        exit(0)