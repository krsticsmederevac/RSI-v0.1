import streamlit as st
from tradingview_ta import TA_Handler, Interval, Exchange
import time
from colorama import Fore, Back, Style, init
init()

simboli = ["ETHUSDT", "BTCUSDT"]

intervali = ["1h", "4h", "1d" ] #"15m",

lista_handler = []
recnik = {}

for i in simboli:
    for j in intervali:
    
        handler = TA_Handler(
            symbol=i,
            exchange="binance",
            screener="crypto",
            interval=j,
            timeout=None
            )
        
        recnik[i + ' ' + j] = 'NEUTRAL'

        lista_handler.append(handler)

def izvestaj(analysis):
    
    if analysis.summary['RECOMMENDATION'] in ['SELL', 'STRONG_SELL']:
        signal = Fore.RED + analysis.summary['RECOMMENDATION'] + Style.RESET_ALL
    elif analysis.summary['RECOMMENDATION'] in ['BUY', 'STRONG_BUY']:
        signal = Fore.GREEN + analysis.summary['RECOMMENDATION'] + Style.RESET_ALL
    else:
        signal = Fore.BLUE + analysis.summary['RECOMMENDATION'] + Style.RESET_ALL
            
    print(Fore.CYAN + analysis.symbol, 
          Fore.YELLOW + analysis.interval,
          Style.RESET_ALL)

    print(signal, analysis.indicators["close"])
    print('Sell: ', Fore.RED + str(analysis.summary['SELL']),Style.RESET_ALL,
          'Buy: ',Fore.GREEN + str(analysis.summary['BUY']),Style.RESET_ALL,
         'Neutral: ', Fore.BLUE +  str(analysis.summary['NEUTRAL']),Style.RESET_ALL)

while True:
    
    for i in lista_handler:
        
        analysis = i.get_analysis()
        
        if recnik[analysis.symbol + ' ' + analysis.interval] != analysis.summary['RECOMMENDATION']:
            recnik[analysis.symbol + ' ' + analysis.interval] = analysis.summary['RECOMMENDATION']
            print('\n',Fore.BLUE + 'Time: ' + str(analysis.time)[:19],Style.RESET_ALL,'\n')
            izvestaj(analysis)

    time.sleep(10)
 
