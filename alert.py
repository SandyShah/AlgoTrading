
max_profit = 3500
max_loss = -1500

exception_list = ['NIFTY22AUG17000PE', 'BHARTIARTL22JUL670PE']

from kiteconnect import KiteConnect
import datetime
import time
import pytz
import requests
import time

# Kite Login Details
access_token='dfjngjgngtkgjvbngkgjmvnnhdnd' # Access token for Zerodha Kite
kite = KiteConnect(api_key="gnghgngnhgpgg")
kite.set_access_token(access_token)

print(kite.holdings())
print(kite.margins()['equity']['available']['live_balance'])
    
#Get last traded proce of a equity/option
def get_ltp(symbol='ABC', exchange='NFO:'):
    temp = exchange+symbol
    return kite.quote(temp)[temp]['last_price']

# Function to calculate PNL of euity/option at a time
def position_pnl(position=1):
    
    PNL = 0
    quantity = position['quantity']
    tradingsymbol = position['tradingsymbol']
    
    if tradingsymbol in exception_list:
        return 0

    exchange=position['exchange']+':'
    ltp = get_ltp(symbol=tradingsymbol, exchange=exchange) 
    
    if quantity==0:
        # print(position['pnl'])
        return position['pnl']   
    
    if quantity>0:
        trading_price = position['buy_price']
        # PNL = (ltp-trading_price)*quantity
    elif quantity<0:
        trading_price = position['sell_price']
    
    PNL = (ltp-trading_price)*quantity

    return PNL



# Sends Continuous PNL to below ChatBot
def telegram_bot_sendtext(bot_message):   
    bot_token = '1234567890:HDGFBG566959HHDhckIPY1eGj3gWeZ8'
    bot_chatID = '99887755'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
    
# Send Alert to below ChatBot only when threshold value is crossed
def telegram_bot_sendtext_imp(bot_message):
    
    bot_token = '1122334455:9898FGFHFG767GFGFtpDHycXXVO1Z_v0'
    bot_chatID = '9988775544'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

    
f = 1

while f==1:
    
    time.sleep(5)
    nowTime = datetime.datetime.now(pytz.timezone('Asia/Calcutta')).time()
    print(nowTime)    
        
    my_positions = kite.positions()['net']
    sum_pnl = 0
    
    for position in my_positions:
        pnl = position_pnl(position)
        sum_pnl = sum_pnl+pnl
      
    print('Sum_PNL = '+str(round(sum_pnl)))
    
    if (sum_pnl>max_profit):
        telegram_bot_sendtext_imp('Profit Reached '+ str(sum_pnl))
             
    if (sum_pnl<max_loss):
        telegram_bot_sendtext_imp('Losses Reached '+ str(sum_pnl))
    
    telegram_bot_sendtext('Profit - '+ str(sum_pnl))
        
    print('--------------')