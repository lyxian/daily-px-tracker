import pendulum
import pandas
import numpy
import sys

from dataReader import yfQuoteReader

if len(sys.argv) == 2:
    STOCK = sys.argv[1]
else:
    print('Please input STOCK as first input..')
    sys.exit()

# STOCK = 'C2PU.SI'
# STOCK = 'AMC'
# FILENAME = f'{STOCK}-1d.json'
INTERVAL = '1m'
DT_FORMAT = '%Y-%m-%d %H:%M'

# _ = yfQuoteReader(interval=INTERVAL).saveDataPoints(STOCK)
# with open(FILENAME, 'r') as file:
#     data = json.load(file)
data = yfQuoteReader(interval=INTERVAL).getDataPoints(STOCK)

_ = ['open', 'close', 'low', 'high', 'volume']
timestamp = data['chart']['result'][0]['timestamp']
datetimes = [pendulum.from_timestamp(i) for i in timestamp]
indicators = data['chart']['result'][0]['indicators']['quote'][0]

d = {}
for column in _:
    d[column] = indicators[column]

df = pandas.DataFrame(d, index=datetimes).tz_convert('Asia/Singapore')
df.index = df.index.strftime(DT_FORMAT)
FILENAME = f'data/{STOCK}_1d_{df.index[0].split()[0]}'

# Clean Table
floatColumns = ['open', 'close', 'low', 'high']
df.loc[:, 'volume'] = df['volume'].apply(lambda x: 0 if numpy.isnan(x) else int(x))
df.loc[:, floatColumns] = df.loc[:, floatColumns].fillna(method='ffill').round(3)

print(df)
if 1:
    df = df.reset_index().rename(columns={'index':'datetime'})
    df.to_json(f'{FILENAME}.json', orient='records', indent=4)
    df.to_csv(f'{FILENAME}.csv', index=False)

# from datetime import datetime
# datetimes = [datetime.fromtimestamp(i) for i in timestamp]
# df = pandas.DataFrame(d, index=datetimes).tz_localize('Asia/Singapore')