import pendulum
import pandas
import numpy
import sys
import os

from dataReader import yfQuoteReader

INTERVAL = '1m'
DT_FORMAT = '%Y-%m-%d %H:%M'
END_TIMES = {
    'us': '04:00',
    'sg': '17:00'
}

def extractStockPrice(market, stock, saveCSV, interval=INTERVAL, dt_format=DT_FORMAT):
    data = yfQuoteReader(interval=interval).getDataPoints(stock)

    _ = ['open', 'close', 'low', 'high', 'volume']
    timestamp = data['chart']['result'][0]['timestamp']
    datetimes = [pendulum.from_timestamp(i) for i in timestamp]
    indicators = data['chart']['result'][0]['indicators']['quote'][0]

    d = {}
    for column in _:
        d[column] = indicators[column]

    df = pandas.DataFrame(d, index=datetimes).tz_convert('Asia/Singapore')
    df.index = df.index.strftime(dt_format)
    FILENAME = f'data/{market}/{stock}/{df.index[0].split()[0]}'

    # Clean Table
    floatColumns = ['open', 'close', 'low', 'high']
    df.loc[:, 'volume'] = df['volume'].apply(lambda x: 0 if numpy.isnan(x) else int(x))
    df.loc[:, floatColumns] = df.loc[:, floatColumns].fillna(method='ffill').round(3)

    # Create folder to store csv
    if saveCSV:
        if stock not in os.listdir(f'data/{market}'):
            os.mkdir(f'data/{market}/{stock}')
            df = df.reset_index().rename(columns={'index':'datetime'})
            # df.to_json(f'{FILENAME}.json', orient='records', indent=4)
            df.to_csv(f'{FILENAME}.csv', index=False)
    return df

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        MARKET = sys.argv[1]
        STOCKS = sys.argv[2:]
    else:
        print('Please input market as first input and stock as second input..')
        sys.exit()

    for stock in STOCKS:
        extractStockPrice(MARKET, stock, True)
            