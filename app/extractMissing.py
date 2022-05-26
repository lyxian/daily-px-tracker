import pendulum
import pandas
import numpy
import sys
import os
import re

from dataReader import yfQuoteReader

INTERVAL = '1m'
DT_FORMAT = '%Y-%m-%d %H:%M'
END_TIMES = {
    'us': '04:00',
    'sg': '17:00'
}

def extractMissingStockPrice(market, stock, missingDate, interval=INTERVAL, dt_format=DT_FORMAT):
    # Validate 'missingDate'
    try:
        year, month, day = re.search(r'^(\d{4})-(\d{2})-(\d{2})$', missingDate).groups()
        pendulum.parse(f'{year}-{month}-{day}')
    except Exception as e:
        raise Exception(f'Invalid input date (year-month-date) - {e}')

    reader = yfQuoteReader(interval=interval)
    reader.params['range'] = '7d'
    data = reader.getDataPoints(stock)

    _ = ['open', 'close', 'low', 'high', 'volume']
    if 'timestamp' not in data['chart']['result'][0].keys():
        print(f'No response from {market}-{stock}')
        return 
    timestamp = data['chart']['result'][0]['timestamp']
    datetimes = [pendulum.from_timestamp(i) for i in timestamp]
    indicators = data['chart']['result'][0]['indicators']['quote'][0]

    d = {}
    for column in _:
        d[column] = indicators[column]

    df = pandas.DataFrame(d, index=datetimes).tz_convert('Asia/Singapore')
    df.index = df.index.strftime(dt_format)
    df = df[df.index.map(lambda x: x.split()[0] == missingDate)]
    FILENAME = f'data/{market}/{stock}/{df.index[0].split()[0]}'    # FAIL if empty

    # Clean Table
    floatColumns = ['open', 'close', 'low', 'high']
    df.loc[:, 'volume'] = df['volume'].apply(lambda x: 0 if numpy.isnan(x) else int(x))
    df.loc[:, floatColumns] = df.loc[:, floatColumns].fillna(method='ffill').round(3)

    # Create folder to store csv
    df = df.reset_index().rename(columns={'index':'datetime'})
    # df.to_json(f'{FILENAME}.json', orient='records', indent=4)
    df.to_csv(f'{FILENAME}.csv', index=False)
    print(f'Saved to {FILENAME}.csv\n')

    return df

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        DATETIME = sys.argv[1]
        MARKET = sys.argv[2]
        STOCKS = sys.argv[3:]
    else:
        print('Please input market as first input and stock as second input..')
        sys.exit()

    for stock in STOCKS:
        extractMissingStockPrice(MARKET, stock, DATETIME)
            