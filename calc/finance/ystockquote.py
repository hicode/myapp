# pip install ystockquote

'''
# to run unit tests:
$ python -m unittest discover
'''

http://finance.yahoo.com/d/quotes.csv?s=160125.sz&f=l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7
http://finance.yahoo.com/d/quotes.csv?s=510900.ss&f=l1c1va2xj1b4j4dyekjm3m4rr5p5p6s7
OK: http://ichart.yahoo.com/table.csv?s=600000.SS&a=08&b=25&c=2010&d=08&e=8&f=2014&g=d

y=ystockquote.get_price('002594.sz')

### Example Usage
import ystockquote
print(ystockquote.get_price('GOOGL'))
print(ystockquote.get_price('000001.sz'))
print(ystockquote.get_price('21103.hk'))

print(ystockquote.get_price('600000.SS'))
http://ichart.yahoo.com/table.csv?s=600000.SS&a=08&b=25&c=2010&d=09&e=8&f=2010&g=d 
http://finance.yahoo.com/d/quotes.csv?s=XOM+BBDb.TO+JNJ+MSFT&f=snd1l1yr 
http://finance.yahoo.com/d/quotes.csv?s=000010.sz&f=snd1l1yr
http://finance.yahoo.com/d/quotes.csv?s=600000.ss&f=snd1l1yr

print(ystockquote.get_price_book('GOOGL'))
print(ystockquote.get_bid_realtime('GOOGL'))

import ystockquote
from pprint import pprint
pprint(ystockquote.get_historical_prices('GOOGL', '2013-01-03', '2013-01-08'))
{'2013-01-03': {'Adj Close': '723.67',
                'Close': '723.67',
                'High': '731.93',
                'Low': '720.72',
                'Open': '724.93',
                'Volume': '2318200'},
 '2013-01-04': {'Adj Close': '737.97',
                'Close': '737.97',
                'High': '741.47',
                'Low': '727.68',
                'Open': '729.34',
                'Volume': '2763500'},
 '2013-01-07': {'Adj Close': '734.75',
                'Close': '734.75',
                'High': '739.38',
                'Low': '730.58',
                'Open': '735.45',
                'Volume': '1655700'},
 '2013-01-08': {'Adj Close': '733.30',
                'Close': '733.30',
                'High': '736.30',
                'Low': '724.43',
                'Open': '735.54',
                'Volume': '1676100'}}
