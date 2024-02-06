from engines import *

def lambda_handler(event, context):
    engine = CardShopLive()
    engine.runScrape()
    engine.printResults()

lambda_handler({},{})