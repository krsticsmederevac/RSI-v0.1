import streamlit as st
st.set_page_config( page_title = "RSI Field", page_icon = "📊",layout="centered",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

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
  
  
  



ponudjeni_simboli =  ['1INCH', 'AAVE', 'ACM', 'ADA', 'AGIX', 'AKRO', 'ALGO', 'ALICE', 'ALPHA', 'ANKR', 
                      'ANT', 'APE', 'APT', 'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AVAX', 
                      'AXS', 'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLZ', 'BNB', 'BTC', 'BURGER', 'CAKE',
                      'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COCOS', 'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CTXC', 
                      'CVC', 'CVX', 'DASH', 'DATA', 'DCR', 'DEGO', 'DENT', 'DGB', 'DIA', 'DOCK', 'DODO', 'DOGE', 'DOT', 
                      'DREP', 'DUSK', 'DYDX', 'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 'FET', 'FIL', 'FIO', 'FIRO', 'FIS', 
                      'FLM', 'FLOW', 'FTM', 'FUN', 'FXS', 'GALA', 'GBP', 'GMX', 'GRT', 'HARD', 'HBAR', 'HIVE', 'HOOK',
                      'HOT', 'ICP', 'ICX', 'ID', 'IMX', 'INJ', 'IOST', 'IOTA', 'IOTX', 'IRIS', 'JOE', 'KAVA', 'KEY', 
                      'KLAY', 'KMD', 'KNC', 'KSM', 'LDO', 'LINA', 'LINK', 'LIT', 'LQTY', 'LRC', 'LSK', 'LTC', 'LTO', 
                      'LUNC', 'MANA', 'MASK', 'MATIC', 'MBL', 'MDT', 'MINA', 'MKR', 'MTL', 'NEAR', 'NEO', 'NEXO', 'NKN', 
                      'NMR', 'OCEAN', 'OGN', 'OMG', 'ONE', 'ONG', 'ONT', 'OP', 'ORN', 'OSMO', 'OXT', 'PAXG', 'PEPE', 'PERL', 
                      'PERP', 'PNT', 'POND', 'PSG', 'QNT', 'QTUM', 'RDNT', 'REEF', 'REN', 'RIF', 'RLC', 'RLC', 'RNDR', 'ROSE',
                      'RPL', 'RSR', 'RUNE', 'RVN', 'SAND', 'SC', 'SFP', 'SHIB', 'SKL', 'SNX', 'SOL', 'STMX', 'STORJ', 'STPT',
                      'STRAX', 'STX', 'SUN', 'SUPER', 'SUSHI', 'SXP', 'TFUEL', 'THETA', 'TOMO', 'TRB', 'TROY', 'TRU', 'TRX', 
                      'TWT', 'UMA', 'UNFI', 'UNI', 'UTK','VET', 'VITE', 'VTHO', 'WAN', 'WAVES', 'WIN', 'WING', 'WNXM', 'WOO', 
                      'WRX', 'WTC', 'XEC', 'XEM', 'XLM', 'XMR', 'XRP', 'XTZ', 'XVS', 'YFI', 'ZEC', 'ZEN', 'ZIL']

ponudjeni_simboli.sort()

ponudjeni_intervali = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"]

ponudjeni_parovi = ["USDT", "BTC"]

# sortiranje_ponuda = ['rsi','coin']

# oscilator = 'rsi'



container = st.container()

tab1, tab2 = container.tabs(["📋 RSI and Price Change %", "📋 EMA and MA"])




podesavanja_korisnika = st.file_uploader("Upload Coin List",'json')  

if podesavanja_korisnika:
  
    podesavanja_korisnika_lista = json.load(podesavanja_korisnika)

    pocetni_simboli = podesavanja_korisnika_lista
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = [ 'ADA', 'ARB', 'ATOM', 'AVAX',  'BNB', 'BTC',
                      'DOT', 'ETH', 'FTM', 'LDO', 'LINK', 'LTC', 'PEPE',
                       'RNDR', 'ROSE',  'WOO']
  

ponudjeni_intervali_pocetni = ['1h', '4h', '1d']
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0






with st.sidebar.form(key ='Form1'):
    
    
    st.header('CryptoData `version 1`')
    
    st.form_submit_button(label = "Submite")
    
    
    interval = st.multiselect('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
        
   
    simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    
        

#     kolona_sortiranja = st.selectbox('Sort by', sortiranje_ponuda,sortiranje_ponuda_pocetni)
    
    
    usdt_btc = st.selectbox('USDT or BTC',ponudjeni_parovi,0)
    
    
#     chart_table = st.multiselect('Chart and/or Table', ['Chart','Table'],'Chart')
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    

    
if usdt_btc :

    dt = data_frame_maker(simboli, interval, [ "change",'RSI','close','EMA10','EMA20',"EMA100","EMA200",'SMA10','SMA20',"SMA100","SMA200"], usdt_btc, ['timeframe'])
    
    
    time_type = pd.CategoricalDtype(categories=["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"], ordered=True)
    dt.timeframe = dt.timeframe.astype(time_type)
    
    dt.set_index(['coin','timeframe'], inplace = True)
    dt.sort_index(level=0, inplace = True)
    
    dt.change = round(dt['change'],2).astype(str) + '%'
    dt.RSI = round(dt['RSI'],1)
    
    
    stil = dt.style.background_gradient(cmap = 'RdYlGn',subset = ['change'] )
    
    with tab1:
        tab1.dataframe(stil,use_container_width= True)
    with tab2:
        tab2.dataframe(stil,use_container_width= True)
        
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")

st.write("Feel free to leave a tip.")
st.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
st.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
st.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
st.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")
