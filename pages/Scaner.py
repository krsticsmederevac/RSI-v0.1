import streamlit as st
st.set_page_config( page_title = "RSI Field", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd
import json 

# import matplotlib.pyplot
# from bokeh.io import curdoc, show
# from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, LabelSet, Span, Range1d, BoxAnnotation, HoverTool, Label
# from bokeh.plotting import figure
# from bokeh.transform import linear_cmap
# from bokeh.palettes import  RdYlGn


def data_frame_maker(simboli, intervali, analitike, usdt_btc, kolona_sortiranja, menjacnica = 'binance'):                        
    
    #ako je izabran par sa BTC ili USDT da dodaje na simbole nastavak
    usdt_ili_btc_lista =  [i + usdt_btc for i in simboli]  
    
    #u slucaju da ne pronadje par da isece nastavak u obavestenju
    duzina_usdt_ili_btc = len(usdt_btc)



    recnik = {'coin': [], 'timeframe' : []}
    
    for analitika in analitike:
        recnik[analitika] = []
        

    for coin in usdt_ili_btc_lista:
        for interval in intervali:
            

            handler = TA_Handler(
                symbol = coin,
                exchange = menjacnica,
                screener = "crypto",
                interval = interval,
                timeout=None
                )

            try:
                analysis = handler.get_analysis()
            except: 
                print(coin[:-duzina_usdt_ili_btc] + " can't find on exchenge.")

            
            recnik['coin'].append(coin[:-duzina_usdt_ili_btc])
            recnik['timeframe'].append(interval)
            try:
                for analitika in analitike:
                    recnik[analitika].append(analysis.indicators[analitika])
            except:
                for analitika in analitike:
                    recnik[analitika].append(None)    
                print(coin[:-duzina_usdt_ili_btc] + "  can't find older data.")    
            else:continue
   



    dt = pd.DataFrame(recnik) 

#     dt.sort_values(by=kolona_sortiranja, inplace=True)
    dt.sort_values(by = 'timeframe', 
                   key= lambda x: x.map({"1m":1, "5m":2, "15m":3, "30m":4, "1h":5, "2h":6,
                                         "4h":7, "1d":8,"1W":9, "1M":10})
                   ,inplace = True)

    if len(dt.index) == 0:
        dt = pd.DataFrame({'coin': ["No Data"], oscilator : [0]})

    return dt
  
  
  



ponudjeni_simboli =  ['RLC', 'PEPE','ID','JOE', '1INCH', 'AAVE', 'ACM', 'ADA', 'AGIX', 'AKRO', 'ALGO', 'ALICE', 'ALPHA','APT','APE', 'ANKR', 'ANT',
                      'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AVAX', 'AXS', 
                      'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLZ', 'BNB',  'BTC', 
                      'BURGER', 'CAKE', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COCOS', 
                      'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CTXC', 'CVC', 'CVX', 'DASH', 'DATA', 'DCR', 'DEGO',
                      'DENT', 'DGB', 'DIA', 'DOCK', 'DODO', 'DOGE', 'DOT', 'DREP', 'DUSK', 'DYDX', 'EGLD',
                      'ENJ', 'EOS', 'ETC', 'ETH', 'FET', 'FIL', 'FIO', 'FIRO', 'FIS', 'FLM','FLOW', 'FTM', 
                      'FUN', 'FXS', 'GALA','GBP', 'GMX', 'GRT', 'HARD', 'HBAR', 'HIVE', 'HOOK', 'HOT','ICP',
                      'ICX', 'INJ', 'IMX', 'IOST', 'IOTA', 'IOTX', 'IRIS', 'KAVA', 'KEY', 'KLAY', 'KMD', 'KNC', 'KSM',
                      'LDO', 'LINA', 'LINK', 'LIT', 'LQTY', 'LRC', 'LSK', 'LTC', 'LTO', 'LUNC', 'MANA', 'MASK',
                      'MATIC', 'MBL', 'MDT', 'MKR', 'MTL', 'MINA', 'NEAR', 'NEO', 'NEXO',
                      'NKN', 'NMR', 'OCEAN', 'OGN', 'OMG', 'ONE', 'ONG', 'ONT', 'OP', 'ORN', 'OSMO', 'OXT', 
                      'PAXG', 'PERL', 'PERP', 'PNT', 'POND', 'PSG', 'QTUM', 'RDNT', 'REEF', 
                      'REN', 'RNDR', 'RIF', 'RLC', 'ROSE', 'RPL', 'RSR', 'RUNE', 'RVN', 'QNT', 'SAND', 'SC', 'SFP','SHIB', 'SKL', 
                      'SNX', 'SOL', 'STMX', 'STORJ', 'STPT', 'STRAX', 'STX', 'SUN', 'SUPER', 
                      'SUSHI', 'SXP', 'TFUEL', 'THETA', 'TOMO', 'TRB', 'TROY', 'TRU', 'TRX', 'TWT', 
                      'UMA', 'UNFI', 'UNI', 'UTK', 'VET', 'VITE', 'VTHO', 'WAN', 'WAVES', 'WIN', 'WING', 'WOO',
                      'WNXM', 'WRX', 'WTC', 'XEM', 'XLM', 'XMR', 'XRP', 'XTZ', 'XVS', 'XEC', 'YFI', 'ZEC', 'ZEN', 'ZIL']

ponudjeni_simboli.sort()

ponudjeni_intervali = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"]

ponudjeni_parovi = ["USDT", "BTC"]

# sortiranje_ponuda = ['rsi','coin']

# oscilator = 'rsi'



container = st.container()

tab1, tab2 = container.tabs(["📈 RSI and %", "📋 EMA and MA"])




podesavanja_korisnika = st.file_uploader("Upload Coin List",'json')  

if podesavanja_korisnika:
  
    podesavanja_korisnika_lista = json.load(podesavanja_korisnika)

    pocetni_simboli = podesavanja_korisnika_lista
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = ['1INCH', 'AAVE', 'ADA', 'AGIX', 'ALGO', 'ANKR', 'APE', 'APT', 'ARB', 'ATOM', 'AUDIO', 'AVAX', 'BCH', 'BNB', 'BTC',
                       'CAKE', 'CFX', 'CHZ', 'COCOS', 'CRV', 'CVX', 'DASH', 'DOGE', 'DOT', 'DYDX', 'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 
                       'FET', 'FIL', 'FLOW', 'FTM', 'FXS', 'GALA', 'GMX', 'GRT', 'HBAR', 'HOOK', 'HOT', 'ICP', 'ID', 'IMX', 'INJ', 'IOTA', 'KAVA', 
                       'KLAY', 'LDO', 'LINK', 'LQTY', 'LTC', 'LUNC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'NEAR', 'NEO', 'NEXO', 
                       'OCEAN', 'OP', 'OSMO', 'PEPE', 'QNT', 'RNDR', 'ROSE', 'RPL', 'RUNE', 'RVN', 'SAND', 
                       'SHIB', 'SNX', 'SOL', 'STX', 'THETA', 'TRX', 'TWT', 'UNI', 'VET', 'WOO', 'XLM', 'XMR', 'XRP', 'XTZ', 'ZEC', 'ZEN', 'ZIL']
  

ponudjeni_intervali_pocetni = ['1h', '4h', '1d']
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0






with st.sidebar.form(key ='Form1'):
    
    
    st.header('CryptoData `version 1`')
    
    st.form_submit_button(label = "Submite")
    
    
    interval = st.multiselect('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
        
   
    simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    
        

#     kolona_sortiranja = st.selectbox('Sort by', sortiranje_ponuda,sortiranje_ponuda_pocetni)
    
    
    usdt_btc = st.select('USDT or BTC',ponudjeni_parovi,ponudjeni_parovi[ponudjeni_parovi_pocetni])
    
    
#     chart_table = st.multiselect('Chart and/or Table', ['Chart','Table'],'Chart')
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    

    
if usdt_btc :

    dt = data_frame_maker(simboli, interval, oscilator, izbor_usdt_btc, kolona_sortiranja)
    
#     dt = dt.set_index('coin')
    stil = dt.style.background_gradient(axis=0, cmap = 'RdYlGn')
    if 'Chart' in chart_table:
        with tab1:
            tab1.bokeh_chart(p)
    if 'Table' in chart_table:
        with tab2:
            tab2.dataframe(stil,use_container_width= True)
        
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")

st.write("Feel free to leave a tip.")
st.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
st.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
st.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
st.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")
