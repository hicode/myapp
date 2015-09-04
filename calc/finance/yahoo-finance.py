# pip install yahoo-finance

from yahoo_finance import Share
yahoo = Share('YHOO')
print yahoo.get_open()
print yahoo.get_price()
print yahoo.get_trade_datetime()

### Refresh data from market
yahoo.refresh()
print yahoo.get_price()
print yahoo.get_trade_datetime()

### Historical data
print yahoo.get_historical('2014-04-25', '2015-04-29')

### More readable output :)
from pprint import pprint
pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))


### Summary information for our example
from pprint import pprint
pprint(yahoo.get_info())

yahoo = Share('baba')
yahoo = Share('1211.hk')
yahoo = Share('21103.hk')
yahoo = Share('002594.sz')
yahoo = Share('160125.sz')
yahoo = Share('150128.sz')
yahoo = Share('150218.sz')

yahoo = Share('600000.ss')
yahoo = Share('510900.ss')


'''
### Avalible methods
get_price()
get_change()
get_volume()
get_prev_close()
get_open()
get_avg_daily_volume()
get_stock_exchange()
get_market_cap()
get_book_value()
get_ebitda()
get_dividend_share()
get_dividend_yield()
get_earnings_share()
get_days_high()
get_days_low()
get_year_high()
get_year_low()
get_50day_moving_avg()
get_200day_moving_avg()
get_price_earnings_ratio()
get_price_earnings_growth_ratio()
get_price_sales()
get_price_book()
get_short_ratio()
get_trade_datetime()
get_historical(start_date, end_date)
get_info()
refresh()
'''

#### Get currency data
##Example: EUR/PLN (EURPLN=X)
from yahoo_finance import Currency
eur_pln = Currency('EURPLN')
print eur_pln.get_bid()
print eur_pln.get_ask()
print eur_pln.get_rate()
print eur_pln.get_trade_datetime()

#Refresh data from market
eur_pln.refresh()
print eur_pln.get_rate()
print eur_pln.get_trade_datetime()

'''
Avalible methods
get_bid()
get_ask()
get_rate()
get_trade_datetime()
refresh()
'''
