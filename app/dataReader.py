import pendulum
import requests
import pandas
import json
import re

class yfDataReader():
    def __init__(self):
        self.url = 'https://sg.finance.yahoo.com/quote/{}/history'
        self.params = {
            'filter': 'history',
            'interval': '1d',
            'frequency': '1d'
        }
        self.headers = {
            "Connection": "keep-alive",
            "Expires": str(-1),
            "Upgrade-Insecure-Requests": str(1),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def getTickerPriceDf(self, ticker, startDate=pendulum.datetime(2020,1,1,tz='Asia/Singapore'), endDate=pendulum.today()):
        if not isinstance(startDate, pendulum.DateTime) or not isinstance(endDate, pendulum.DateTime):
            raise Exception('Start/End date has bad data type, please use DateTime objects')
        else:
            startDate = int(startDate.timestamp())
            endDate = int(endDate.timestamp())

        tickerUrl = self.url.format(ticker)
        tickerParams = {
            'period1': startDate,
            'period2': endDate,
            **self.params
        }

        print(f'Getting response from {tickerUrl}')
        response = requests.get(url=tickerUrl, params=tickerParams, headers=self.headers)
        data = json.loads(re.search(r'root\.App\.main = (.*?);\n}\(this\)\);', response.text).group(1))["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]
        prices = [i for i in data['prices'] if 'type' not in i.keys()]
        # with open('x.json', 'w') as file:
        #     file.write(json.dumps(data, indent=4))

        df = pandas.DataFrame(prices).sort_values(by=['date'], ascending=True)
        df.loc[:, 'date'] = df['date'].apply(lambda x: pendulum.from_timestamp(x).to_date_string())
        df = df.set_index("date")

        return df

    def getTickerPriceDfs(self, tickers, startDate, endDate):
        dfs = [self.getTickerPriceDf(ticker, startDate, endDate) for ticker in tickers]

        return pandas.concat(dfs, keys=tickers, names=['ticker','date'])

import pendulum
import requests
import json

class yfQuoteReader():
    def __init__(self, interval='60m'):
        self.url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}'
        self.params = {
            'interval': interval,
            'range': '1d',
            'corsDomain': 'finance.yahoo.com',
            '.tsrc': 'finance'
        }
        self.headers = {
            "Connection": "keep-alive",
            "Expires": str(-1),
            "Upgrade-Insecure-Requests": str(1),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def getDataPoints(self, ticker):

        tickerUrl = self.url.format(ticker)
        tickerParams = {
            # 'period1': startDate,
            # 'period2': endDate,
            **self.params
        }

        print(f'Getting response from {tickerUrl}')
        response = requests.get(url=tickerUrl, params=tickerParams, headers=self.headers)

        return response.json()

    def saveDataPoints(self, ticker):

        tickerUrl = self.url.format(ticker)
        tickerParams = {
            # 'period1': startDate,
            # 'period2': endDate,
            **self.params
        }

        print(f'Getting response from {tickerUrl}')
        response = requests.get(url=tickerUrl, params=tickerParams, headers=self.headers)

        with open(f'{ticker}-{tickerParams["range"]}.json', 'w') as file:
            file.write(json.dumps(response.json(), indent=4))

        return

# class yfQuotes
# https://query1.finance.yahoo.com/v8/finance/chart/9CI.SI?region=US&lang=en-US&includePrePost=false&interval=15m&useYfid=true&range=5d&corsDomain=finance.yahoo.com&.tsrc=finance
# https://query1.finance.yahoo.com/v8/finance/chart/9CI.SI?symbol=9CI.SI&period1=1645448599&period2=1645621399&useYfid=true&interval=1m&includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&region=US&crumb=TUI2vN6taxv&corsDomain=finance.yahoo.com
# https://query1.finance.yahoo.com/v7/finance/quote?symbols=9CI.SI

if __name__ == '__main__':
    _ = yfQuoteReader().getDataPoints('C2PU.SI')