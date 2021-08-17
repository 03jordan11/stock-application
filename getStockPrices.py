import finnhub
import json
from datetime import datetime, timedelta

def readJson(fn):
    with open(fn) as jsonFile:
        data = json.load(jsonFile)
    return data

def writeJson(fn, data):
    with open(fn, 'w') as out:
        json.dump(data, out)

def getSettings():
    print('hi')
    settings = readJson("settings.json")
    folder = settings['DEV_FOLDER'] if settings['ENV'] == "Dev" else settings['PROD_FOLDER']
    print(f"""api key is {settings['API_KEY']}\n
    time difference is {settings['TIME_DIFFERENCE']}\n
    folder name is {folder}
    """)
    return settings['API_KEY'], settings['TIME_DIFFERENCE'], folder


API_KEY, TIME_DIFFERENCE, FOLDER_PATH = getSettings()

fhub = finnhub.Client(api_key=API_KEY)

#Getting list of all tickers
tickers = readJson(f'{FOLDER_PATH}/tickers.json')
winningTickers = tickers['winners']
losingTickers = tickers['losers']

#Grabbing all winners and losers
winners = readJson(f'{FOLDER_PATH}/winners.json')
losers = readJson(f'{FOLDER_PATH}/losers.json')

for winningTicker in winningTickers:
    if winningTicker in winners:
        winners[winningTicker]['prices'].append(
            {
                "date": (datetime.now()+timedelta(hours=TIME_DIFFERENCE)).strftime("%m-%d-%Y:%H%M%S"),
                "price": fhub.quote(winningTicker)['c']
            }
        )

for losingTicker in losingTickers:
    if losingTicker in losers:
        losers[losingTicker]['prices'].append(
            {
                "date": (datetime.now()+timedelta(hours=TIME_DIFFERENCE)).strftime("%m-%d-%Y:%H%M%S"),
                "price": fhub.quote(losingTicker)['c']
            }
        )

writeJson(f"{FOLDER_PATH}/winners.json", winners)
writeJson(f"{FOLDER_PATH}/losers.json", losers)
