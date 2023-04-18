import streamlit as st
st.set_page_config( page_title = "Scaner", page_icon = ":shark:",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

from tradingview_ta import TA_Handler, Interval, Exchange
import time
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
        signal = analysis.summary['RECOMMENDATION']
    elif analysis.summary['RECOMMENDATION'] in ['BUY', 'STRONG_BUY']:
        signal =  analysis.summary['RECOMMENDATION']
    else:
        signal =analysis.summary['RECOMMENDATION']
            
    st.write(analysis.symbol, 
          analysis.interval,(signal, analysis.indicators["close"], ' Sell: ',str(analysis.summary['SELL']),
          'Buy: ',str(analysis.summary['BUY']),
         'Neutral: ', str(analysis.summary['NEUTRAL']))

while True:
    
    for i in lista_handler:
        
        analysis = i.get_analysis()
        
        if recnik[analysis.symbol + ' ' + analysis.interval] != analysis.summary['RECOMMENDATION']:
            recnik[analysis.symbol + ' ' + analysis.interval] = analysis.summary['RECOMMENDATION']
            st.write('\n','Time: ' + str(analysis.time)[:19],'\n')
            izvestaj(analysis)

    time.sleep(15)
 
