import pendulum
import pandas
import numpy
import sys
import os

from dataReader import yfQuoteReader

if len(sys.argv) >= 3:
    MARKET = sys.argv[1]
    STOCKS = sys.argv[2:]
else:
    print('Please input market as first input and stock as second input..')
    sys.exit()

for stock in STOCKS:
    INTERVAL = '1m'
    DT_FORMAT = '%Y-%m-%d %H:%M'

    data = yfQuoteReader(interval=INTERVAL).getDataPoints(stock)

    _ = ['open', 'close', 'low', 'high', 'volume']
    timestamp = data['chart']['result'][0]['timestamp']
    datetimes = [pendulum.from_timestamp(i) for i in timestamp]
    indicators = data['chart']['result'][0]['indicators']['quote'][0]

    d = {}
    for column in _:
        d[column] = indicators[column]

    df = pandas.DataFrame(d, index=datetimes).tz_convert('Asia/Singapore')
    df.index = df.index.strftime(DT_FORMAT)
    FILENAME = f'data/{MARKET}/{stock}/{df.index[0].split()[0]}'

    # Clean Table
    floatColumns = ['open', 'close', 'low', 'high']
    df.loc[:, 'volume'] = df['volume'].apply(lambda x: 0 if numpy.isnan(x) else int(x))
    df.loc[:, floatColumns] = df.loc[:, floatColumns].fillna(method='ffill').round(3)

    # Create folder to store csv
    if 1:
        if stock not in os.listdir('data'):
            os.mkdir(f'data/{MARKET}/{stock}')
        # print(df)
        df = df.reset_index().rename(columns={'index':'datetime'})
        # df.to_json(f'{FILENAME}.json', orient='records', indent=4)
        df.to_csv(f'{FILENAME}.csv', index=False)
        