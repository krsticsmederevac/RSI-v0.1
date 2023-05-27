import streamlit as st
st.set_page_config( page_title = "Scanner", page_icon = "📊",layout="centered",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd
import numpy as np
import json 

import seaborn as sns
import matplotlib.pyplot as plt


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
    
#     dt['Change'] = round(dt['change'],2).astype(str) + '%'
#     dt.RSI = round(dt[['RSI']],1)
#     dt.change = round(dt[['change']],2)
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




container = st.container()

tab1, tab2, tab3, tab4 = container.tabs(["📋 RSI","📋 Price Change %","📋 EMAs","📋 SMAs" ]) 



container.write("Feel free to leave a tip.")
container.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
container.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
container.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
container.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")

podesavanja_korisnika = container.file_uploader("Upload Coin List",'json') 


if podesavanja_korisnika:
  
    podesavanja_korisnika_lista = json.load(podesavanja_korisnika)

    pocetni_simboli = podesavanja_korisnika_lista
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = [ '1INCH', 'AAVE', 'ADA', 'AGIX', 'ALGO', 'ANKR', 'APE', 'APT', 'ARB', 'ATOM', 'AUDIO', 'AVAX', 'BCH', 'BNB', 'BTC',
                       'CAKE', 'CFX', 'CHZ', 'COCOS', 'CRV', 'CVX', 'DASH', 'DOGE', 'DOT', 'DYDX', 'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 
                       'FET', 'FIL', 'FLOW', 'FTM', 'FXS', 'GALA', 'GMX', 'GRT', 'HBAR', 'HOOK', 'HOT', 'ICP', 'ID', 'IMX', 'INJ', 'IOTA', 'KAVA', 
                       'KLAY', 'LDO', 'LINK', 'LQTY', 'LTC', 'LUNC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'NEAR', 'NEO', 'NEXO', 
                       'OCEAN', 'OP', 'OSMO', 'PEPE', 'QNT', 'RNDR', 'ROSE', 'RPL', 'RUNE', 'RVN', 'SAND', 
                       'SHIB', 'SNX', 'SOL', 'STX', 'THETA', 'TRX', 'TWT', 'UNI', 'VET', 'WOO', 'XLM', 'XMR', 'XRP', 'XTZ', 'ZEC', 'ZEN', 'ZIL']
  

ponudjeni_intervali_pocetni = ['15m','1h', '4h', '1d','1W']
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0






with st.sidebar.form(key ='Form1'):
    
    
    st.header('Scanner `version 1`')
    
    st.form_submit_button(label = "Submite")
    
    
    interval = st.multiselect('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
   
    simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    
    
    usdt_btc = st.selectbox('USDT or BTC',ponudjeni_parovi,0)
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    
    

    
if usdt_btc :
    try:
        dt = data_frame_maker(simboli, interval, 
                              [ 'RSI','change','close','EMA10','EMA20',"EMA100","EMA200",'SMA10','SMA20',"SMA100","SMA200"], 
                              usdt_btc, ['timeframe'])
        
        dt.RSI = round(dt['RSI'],1)
        dt.change = round(dt['change'],1)
        
        time_type = pd.CategoricalDtype(categories=["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"], ordered=True)
        dt.timeframe = dt.timeframe.astype(time_type)
        
        dt1 = dt.pivot(index='coin', columns='timeframe', values='RSI')
        
        dt2 = dt.pivot(index='coin', columns='timeframe', values='change')

        
        fig_high = len(dt.index ) / 5
        sns.set(font_scale=0.4)
        
        fig1, ax1 = plt.subplots(figsize = (1.5,fig_high))
        sns.heatmap(dt1, cmap ='RdYlGn',vmin=0, vmax=100,  linewidths = 0.30, annot = True, cbar=False).set_title("RSI")
        ax1.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax1.set_xlabel('')
        ax1.set_ylabel('')
        
        fig2, ax2 = plt.subplots(figsize = (1.5,fig_high))
        sns.heatmap(dt2, cmap ='RdYlGn',vmin=-3, vmax=3,  linewidths = 0.30, annot = True, cbar=False).set_title("Price Change %")
        ax2.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax2.set_xlabel('')
        ax2.set_ylabel('')
        
        dt['10'] =np.where((dt['EMA10']<=dt.close), 10, -10)
        dt['20'] =np.where((dt['EMA20']<=dt.close), 20, -20)
        dt['100'] =np.where((dt['EMA100']<=dt.close), 100, -100)
        dt['200'] =np.where((dt['EMA200']<=dt.close), 200, -200)
        
        data_frames = []
        for time_int in interval:
            dt_name = 'dt' + time_int 
            dt_name = dt[dt['timeframe'] == time_int]
            dt_name = dt_name.pivot(index='coin', columns='timeframe', values=['10','20',"100","200"])
            data_frames.append(dt_name)
        
        dt_ema = pd.concat(data_frames,axis=1)
        
        ema_sma_size = len(interval)/2
        fig3, ax3 = plt.subplots(figsize = (ema_sma_size,fig_high))
        sns.heatmap(dt_ema, cmap ='RdYlGn',vmin=-1, vmax=1,  linewidths = 0.30, annot = False, cbar=False).set_title("EMA 10 20 100 200")
        ax3.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax3.set_xticklabels(ax4.get_xticklabels(), rotation=90, ha='center')
        ax3.set_xlabel('')
        ax3.set_ylabel('')
        
        dt['10'] =np.where((dt['SMA10']<=dt.close), 10, -10)
        dt['20'] =np.where((dt['SMA20']<=dt.close), 20, -20)
        dt['100'] =np.where((dt['SMA100']<=dt.close), 100, -100)
        dt['200'] =np.where((dt['SMA200']<=dt.close), 200, -200)
        
        data_frames = []
        for time_int in interval:
            dt_name = 'dt' + time_int 
            dt_name = dt[dt['timeframe'] == time_int]
            dt_name = dt_name.pivot(index='coin', columns='timeframe', values=['10','20',"100","200"])
            data_frames.append(dt_name)
        
        dt_sma = pd.concat(data_frames,axis=1)
        
        ema_sma_size = len(interval)/2
        fig4, ax4 = plt.subplots(figsize = (ema_sma_size,fig_high))
        sns.heatmap(dt_sma, cmap ='RdYlGn',vmin=-1, vmax=1,  linewidths = 0.30, annot = False, cbar=False).set_title("SMA 10 20 100 200")
        ax4.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax4.set_xticklabels(ax4.get_xticklabels(), rotation=90, ha='center')
        ax4.set_xlabel('')
        ax4.set_ylabel('')

        with tab1:
            tab1.pyplot(fig1,use_container_width= False)

        with tab2:
            tab2.pyplot(fig2,use_container_width= False)
            
        with tab3:
            tab3.pyplot(fig3,use_container_width= False)
            
        with tab4:
            tab4.pyplot(fig4,use_container_width= False)
    except:
        st.write('Check again your data!')
    
  
    
        
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")
