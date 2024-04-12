import streamlit as st
st.set_page_config( page_title = "Multiple Time Frame Analyze", page_icon = "📊",layout="centered",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd
import numpy as np
import json 

import seaborn as sns
import matplotlib.pyplot as plt

ponudjeni_simboli =  [ '1INCH', 
                      'AAVE', 'ACM', 'ADA', 'AGIX', 'AKRO', 'ALGO', 'ALICE', 'ALPHA','APT','APE', 'ANKR', 'ANT', 'AKT','AMB','ATA','ACA','ADX',
                      'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AVAX', 'AXS', 'ABBC', 'AR','ASTR', 'ACH', 'API3','ASTRAFER','ALI', 'AMP','ALPINE',
                      'AGLD','AST','AUCTION',
                      'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLZ', 'BNB',  'BTC', 'BURGER', 'BTTC','BABYDOGE','BOND',
                      'BLUR', 'BTG', 'BICO','BONE','BORA', 'BNX','BRISE', 'BTRST', 'BDX', 'BAKE','BTS', 'BETA','BAR','BSW',
                      'CAKE', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CTXC', 'CVC', 'CVX','CRO','CSPR', 'CORE','COMBO',
                      'CHSB','C98','CQT','CFG','CITY', 'CLV','CYBER',
                      'DASH', 'DATA', 'DCR', 'DEGO', 'DENT', 'DGB', 'DIA', 'DOCK', 'DODO', 'DOGE', 'DOT', 'DREP', 'DUSK', 'DYDX', 'DAO', 'DAR', 'DAG', 'DFI',
                      'DERO','DEXE', 'DESO','DKA','DEFI',
                      'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 'ELF', 'EDU','ETHW','ELON','ERG', 'EWT','ENS','ERN', 'EPX',
                      'FET', 'FIL', 'FIO', 'FIRO', 'FIS', 'FLM','FLR','FLOW','FLUX', 'FTM', 'FUN', 'FXS', 'FLOKI','FIDA', 'FORTH','FRONT',
                      'GALA','GBP', 'GMX', 'GRT', 'GT', 'GNO', 'GMT', 'GLM', 'GLMR','GNS','GAL','GTC','GAS',
                      'HARD', 'HBAR', 'HIVE', 'HOOK', 'HOT', 'HT','HNT','HFT','HIGH','HIFI',
                      'ICP','ICX', 'INJ', 'IMX', 'IOST', 'IOTA', 'IOTX', 'IRIS', 'ID', 'ILV','IDEX',
                      'JOE', 'JASMY', 'JST',
                      'KAVA', 'KEY', 'KLAY', 'KMD', 'KNC', 'KSM', 'KCS' , 'KDA','KAS',
                      'LDO', 'LINA', 'LINK', 'LIT', 'LQTY', 'LRC', 'LSK', 'LTC', 'LTO', 'LUNC','LEO', 'LUNA', 'LPT','LOOKS','LYXE', 'LOCUS', 'LEVER','LAZIO',
                      'MANA', 'MASK', 'MATIC', 'MBL', 'MDT', 'MKR', 'MTL', 'MINA', 'MX', 'MAGIC', 'MOB', 'METIS','MRS','MC','MED','MULTI','MOVR','MBOX','MAV',
                      'NEAR', 'NEO', 'NEXO','NKN', 'NMR', 'NYM','NULS',
                      'OCEAN', 'OGN', 'OMG', 'ONE', 'ONG', 'ONT', 'OP', 'ORN', 'OSMO', 'OXT', 'OKB','ORDI','ORBS','OG','OAX','OM',
                      'PAXG', 'PERL', 'PERP', 'PNT', 'POND', 'PSG','PEPE', 'PHA','PENDLE', 'PROM', 'POLYX', 'PYR', 'PLA','PEOPLE','PHB','PORTO','PUNDIX', 'PENDLE',
                      'QTUM', 'QNT','QUICK', 'QI',
                      'RDNT', 'REEF', 'REN', 'RNDR', 'RIF', 'RLC', 'ROSE', 'RPL', 'RSR', 'RUNE', 'RVN', 'RON','REQ','RBN','RAD',
                      'SAND', 'SC', 'SFP','SHIB', 'SKL', 'SNX', 'SOL', 'STMX', 'STORJ', 'STPT', 'STRAX', 'STX', 'SUI','SUN', 'SUPER', 
                      'SUSHI', 'SXP', 'SSV', 'STG', 'SYS', 'SLP', 'SCRT','STEEM', 'SYN', 'SNT','SPELL','SANTOS','SEI',
                      'TFUEL', 'THETA', 'TOMO', 'TRB', 'TROY', 'TRU', 'TRX', 'TWT', 'T','TOMI','TRIBE','TEL','TRAC','TLM','TVK', 'TKO',
                      'UMA', 'UNFI', 'UNI', 'UTK', 'USTC',
                      'VET', 'VITE', 'VTHO', 'VRA','VVS','VGX','VOXEL','VIDT', 'VIB',
                      'WAN', 'WAVES', 'WIN', 'WING', 'WOO','WNXM', 'WRX', 'WTC', 'WAX', 'WAXL', 'WILD','WBT','WEMIX','WAXP', 'WLD',
                      'XEM', 'XLM', 'XMR', 'XRP', 'XTZ', 'XVS', 'XEC', 'XDC', 'XCH', 'XRD', 'XOR','XYM','XPLA',
                      'YFI', 'YFII', 'YGG',
                      'ZEC', 'ZEN', 'ZIL','ZRX',
                     ]

binance_futurese_list = ['1INCH',
                         'AAVE','ACH','ADA','AGIX','ALGO','ALICE', 'ALPHA', 'AMB', 'ANKR', 'ANT', 'APE',
                         'API3', 'APT', 'AR', 'ARB', 'ARPA', 'ASTR', 'ATA', 'ATOM', 'AUDIO','AVAX','AXS',
                         'BAKE', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLUR', 'BLZ', 'BNB', 'BNX', 'BTC',
                         'C98', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COMBO', 'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CVX',
                         'DAR', 'DASH', 'DEFI', 'DENT', 'DGB', 'DODO', 'DOGE', 'DOT', 'DUSK', 'DYDX',
                         'EDU', 'EGLD', 'ENJ', 'ENS', 'EOS', 'ETC', 'ETH',
                         'FET', 'FIL', 'FLM', 'FLOKI', 'FLOW', 'FTM', 'FXS',
                         'GALA', 'GMT', 'GMX', 'GRT', 'GTC',
                         'HBAR', 'HFT', 'HIGH', 'HOOK', 'HOT','HIFI',
                         'ICP', 'ICX', 'ID', 'IMX', 'INJ', 'IOST', 'IOTA', 'IOTX',
                         'JASMY','JOE',
                         'KAVA', 'KEY', 'KLAY', 'KNC', 'KSM',
                         'LDO', 'LEVER', 'LINA', 'LINK', 'LIT', 'LPT', 'LQTY', 'LRC', 'LTC', 'LUNA', 'LUNC',
                         'MAGIC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'MTL','MAV',
                         'NEAR', 'NEO', 'NKN',
                         'OCEAN', 'OGN', 'OMG', 'ONE', 'ONT', 'OP',
                         'PEOPLE','PEPE', 'PERP', 'PHB',
                         'QNT', 'QTUM',
                         'RAD', 'RDNT', 'REEF', 'REN', 'RLC', 'RNDR', 'ROSE', 'RSR', 'RUNE', 'RVN',
                         'SAND', 'SFP', 'SHIB', 'SKL', 'SNX', 'SOL', 'SPELL', 'SSV', 'STG', 'STMX', 
                         'STORJ', 'STX', 'SUI', 'SUSHI','SXP',
                         'T', 'THETA', 'TLM', 'TOMO', 'TRB', 'TRU', 'TRX',
                         'UMA', 'UNFI', 'UNI',
                         'VET',
                         'WAVES', 'WOO','WLD',
                         'XEM', 'XLM', 'XMR', 'XRP', 'XTZ', 'XVS',
                         'YFI',
                         'ZEC', 'ZEN', 'ZIL', 'ZRX']

top_100 =  [ 'AAVE', 'ADA', 'AGIX', 'ALGO', 'ANKR', 'APE', 'APT', 'ARB', 'ATOM', 'AUDIO', 'AVAX', 'AXS','BCH', 'BNB', 'BTC','CRO',
                       'CAKE', 'CFX', 'CHZ', 'CRV', 'CVX', 'DASH', 'DOGE', 'DOT', 'DYDX', 'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 
                       'FET', 'FIL', 'FLOW', 'FTM', 'FXS', 'GALA', 'GMX', 'GRT', 'HBAR', 'HOOK', 'HOT', 'ICP', 'ID', 'IMX', 'INJ', 'IOTA', 'KAVA', 
                       'KLAY', 'LDO','LEO', 'LINK', 'LQTY', 'LTC', 'LUNC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'NEAR', 'NEO', 'NEXO', 
                       'OCEAN', 'OP', 'OSMO', 'PEPE', 'QNT', 'RNDR', 'ROSE', 'RPL', 'RUNE', 'RVN', 'SAND', 
                       'SHIB', 'SNX', 'SOL', 'STX', 'THETA', 'TRX', 'TWT', 'UNI', 'VET', 'WOO', 'XLM', 'XMR', 'XRP', 'XTZ', 'ZEC', 'ZEN', 'ZIL']


ponudjeni_simboli.sort()

ponudjeni_intervali = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"]

ponudjeni_parovi = ["USDT", "BTC"]



def data_frame_maker(simboli, intervali, analitike, usdt_btc, kolona_sortiranja):                        
    
    #ako je izabran par sa BTC ili USDT da dodaje na simbole nastavak
    usdt_ili_btc_lista =  [i + usdt_btc for i in simboli]  
    
    #u slucaju da ne pronadje par da isece nastavak u obavestenju
    duzina_usdt_ili_btc = len(usdt_btc)
    
    kraken = []
    kraken_usdt_btc = [i + usdt_btc for i in kraken]
    
    huobi = ['CHSB','MRS','ORBS','ALI',]
    huobi_usdt_btc = [i + usdt_btc for i in huobi]
    
    gate = ['HT','GT','BTG','HNT','DAO', 'WAXL','BRISE','BTRST','XRD','ERG','XOR','WBT','BDX','WEMIX',
            'PENDLE','XPLA','RBN','DESO','DKA','MED',]
    gate_usdt_btc = [i + usdt_btc for i in gate] 
    
    mexc = ['MX','KAS','TRIBE','ASTRAFER','VVS',]
    mexc_usdt_btc = [i + usdt_btc for i in mexc] 
    
    okx = ['OKB','LEO','CRO','CSPR','XCH','ETHW','BONE','BORA','CORE','NYM','LOOKS','BABYDOGE','RON','ORDI',]
    okx_usdt_btc = [i + usdt_btc for i in okx] 
    
    kucoin = ['KCS','FLR','TON','XDC','ABBC','BLUR','WILD','ELON','METIS','AKT','VRA','DAG','DFI',
              'TOMI','XYM','LYXE','TEL','LOCUS','CQT','CFG','DERO','TRAC','EWT',]
    kucoin_usdt_btc = [i + usdt_btc for i in kucoin] 
    
    recnik = {'coin': [], 'timeframe' : []}
    
    for analitika in analitike:
        recnik[analitika] = []
        

    for coin in usdt_ili_btc_lista:
        
        for interval in intervali:
            if coin in gate_usdt_btc:
                menjacnica = 'gateio'
            elif coin in kucoin_usdt_btc:
                menjacnica = 'kucoin'
            elif coin in okx_usdt_btc:
                menjacnica = 'okx'
            elif coin in mexc_usdt_btc:
                menjacnica = 'mexc'
            elif coin in huobi_usdt_btc:
                menjacnica = 'huobi'
            elif coin in kraken_usdt_btc:
                menjacnica = 'kraken'   
                
            else:
                menjacnica = 'binance'
            

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


    dt.sort_values(by = 'timeframe', 
                   key= lambda x: x.map({"1m":1, "5m":2, "15m":3, "30m":4, "1h":5, "2h":6,
                                         "4h":7, "1d":8,"1W":9, "1M":10})
                   ,inplace = True)

    if len(dt.index) == 0:
        dt = pd.DataFrame({'coin': ["No Data"], oscilator : [0]})
    

    return dt
  
  
 




container = st.container()

tab1, tab5, tab6, tab2, tab3, tab4= container.tabs(["📋 RSI", "📋 Bollinger Bands STD", "📋 CCI", "📋 Price Change %", "📋 EMAs", "📋 SMAs"]) 



container.write("Feel free to leave a tip.")
container.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
container.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
container.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
container.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")

podesavanja_korisnika = container.file_uploader("Upload Coin List",'json') 


if podesavanja_korisnika:
  
    podesavanja_korisnika_lista = json.load(podesavanja_korisnika)

    pocetni_simboli = podesavanja_korisnika_lista
#     simboli = podesavanja_korisnika_lista
    
#     if any( x not in ponudjeni_simboli for x in simboli):
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
#        simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
     pocetni_simboli = [ 'ADA', 'AVAX', 'BNB', 'BTC', 'DOT',  'ETH', 'LINK', 'LTC',  'XRP', ]
  

ponudjeni_intervali_pocetni = [ '4h', '1d','1W']
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0






with st.sidebar.form(key ='Form1'):
    
    
    st.header('`Multiple Time Frame Analyze`')
    
    st.form_submit_button(label = "Submit")
    
    
    interval = st.multiselect('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
    izbor_liste_coina = st.selectbox('Coin  List',['Binance Futurese', 'Top MC','Custom'],1)
    

    if izbor_liste_coina == 'Binance Futurese': 
        simboli = binance_futurese_list
    elif izbor_liste_coina == 'Top MC':
        simboli = top_100
    else:
        simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    

       
    
    usdt_btc = 'USDT' #st.selectbox('USDT or BTC',ponudjeni_parovi,0)
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    
    

    
if usdt_btc :
    try:
        dt = data_frame_maker(simboli, interval, 
                              [ 'RSI','change','close','EMA20','EMA50',"EMA100","EMA200",'SMA20','SMA50',"SMA100","SMA200",'low','high','BB.upper','BB.lower','CCI20'], 
                              usdt_btc, ['timeframe'])
        
        dt.RSI = round(dt['RSI'],1)
        dt.change = round(dt['change'],1)
        dt['CCI'] = dt ['CCI20']
        dt['CCI'] = round(dt['CCI'],1)
        
        time_type = pd.CategoricalDtype(categories=["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"], ordered=True)
        dt.timeframe = dt.timeframe.astype(time_type)
        
        dt1 = dt.pivot(index='coin', columns='timeframe', values='RSI')
        
        dt2 = dt.pivot(index='coin', columns='timeframe', values='change')

        if len(interval) == 1:
            fig_high = len(dt.index ) / 10
        else:
            fig_high = len(dt.index ) / 20
            
        sns.set(font_scale=0.4)
        plt.tight_layout()
        
        fig1, ax1 = plt.subplots(figsize = (1.5,fig_high))
        sns.heatmap(dt1, cmap ='RdYlGn',vmin=20, vmax=80,  linewidths = 0.30, annot = True, cbar=False).set_title("RSI")
        ax1.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, ha='center')
        ax1.set_yticklabels(ax1.get_yticklabels(), rotation=0, ha='center')
        ax1.set_xlabel('')
        ax1.set_ylabel('')
        
        
        
        fig2, ax2 = plt.subplots(figsize = (1.5,fig_high))
        sns.heatmap(dt2, cmap ='RdYlGn',vmin=-3, vmax=3,  linewidths = 0.30, annot = True, fmt='g',cbar=False).set_title("Price Change %")
        ax2.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90, ha='center')
        ax2.set_yticklabels(ax2.get_yticklabels(), rotation=0, ha='center')
        ax2.set_xlabel('')
        ax2.set_ylabel('')
        
        dt['20'] =np.where(dt['EMA20'].isna() , np.nan, np.where((dt['EMA20']<=dt.close) , 10, -10))
        dt['50'] =np.where(dt['EMA50'].isna() , np.nan, np.where((dt['EMA50']<=dt.close) , 10, -10))
        dt['100'] =np.where(dt['EMA100'].isna() , np.nan, np.where((dt['EMA100']<=dt.close) , 10, -10))
        dt['200'] =np.where(dt['EMA200'].isna() , np.nan, np.where((dt['EMA200']<=dt.close) , 10, -10))
        
        data_frames = []
        for time_int in interval:
            dt_name = 'dt' + time_int 
            dt_name = dt[dt['timeframe'] == time_int]
            dt_name = dt_name.pivot(index='coin', columns='timeframe', values=['20','50',"100","200"])
            data_frames.append(dt_name)
        
        dt_ema = pd.concat(data_frames,axis=1)
        
        ema_sma_size = len(interval)/2
        fig3, ax3 = plt.subplots(figsize = (ema_sma_size,fig_high))
        sns.heatmap(dt_ema, cmap ='RdYlGn',vmin=-12, vmax=12,  linewidths = 0.30, annot = False, fmt='g', cbar=False).set_title("EMA 20 50 100 200 %")
        ax3.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90, ha='center')
        ax3.set_yticklabels(ax3.get_yticklabels(), rotation=0, ha='center')
        ax3.set_xlabel('')
        ax3.set_ylabel('')
        
        dt['20'] =np.where(dt['SMA20'].isna() , np.nan, np.where((dt['SMA20']<=dt.close) , round(dt.close/(dt.close-dt['SMA20']),2)*100, round(1 - dt['SMA20']/dt.close,2)*100))
        dt['50'] =np.where(dt['SMA50'].isna() , np.nan, np.where((dt['SMA50']<=dt.close) , round(dt.close/(dt.close-dt['SMA50']),2)*100, round(1 - dt['SMA50']/dt.close,2)*100))
        dt['100'] =np.where(dt['SMA100'].isna() , np.nan, np.where((dt['SMA100']<=dt.close) , round(dt.close/(dt.close-dt['SMA100']),2)*100, round(1 - dt['SMA100']/dt.close,2)*100))
        dt['200'] =np.where(dt['SMA200'].isna() , np.nan, np.where((dt['SMA200']<=dt.close) , round(dt.close/(dt.close-dt['SMA200']),2)*100, round(1 - dt['SMA200']/dt.close,2)*100))
        
        data_frames = []
        for time_int in interval:
            dt_name = 'dt' + time_int 
            dt_name = dt[dt['timeframe'] == time_int]
            dt_name = dt_name.pivot(index='coin', columns='timeframe', values=['20','50',"100","200"])
            data_frames.append(dt_name)
        
        dt_sma = pd.concat(data_frames,axis=1)
        
        
        fig4, ax4 = plt.subplots(figsize = (ema_sma_size,fig_high))
        sns.heatmap(dt_sma, cmap ='RdYlGn',vmin=-200, vmax=200,  linewidths = 0.30, annot = True, annot_kws={"fontsize":4}, fmt='g', cbar=False).set_title("SMA 20 50 100 200 %")
        ax4.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax4.set_xticklabels(ax4.get_xticklabels(), rotation=90, ha='center')
        ax4.set_yticklabels(ax4.get_yticklabels(), rotation=0, ha='center')
        ax4.set_xlabel('')
        ax4.set_ylabel('')
        
        dt['BB SMA'] = (dt['BB.upper'] + dt['BB.lower']) / 2
        
        conditions = [
        (dt['BB.upper'].isna() | dt['BB.lower'].isna() ),
        ((dt['BB.upper']<= dt.high) | (dt['BB.upper']<= dt.close)),
        ((dt['BB.lower']>= dt.low) | (dt['BB.lower']>=dt.close)),
        (dt['BB SMA'] < dt.close),
        (dt['BB SMA'] > dt.close)
#         ((dt['BB.upper']> dt.high) | (dt['BB.upper']> dt.close) | (dt['BB.lower']< dt.low) | (dt['BB.lower']<dt.close))
        ]
        
        values = [np.nan, 1,-1, 0.5, -0.75]

        dt['BB'] =np.select(conditions,values)
        
        dt['BB.SMA'] =  (dt['BB.upper'] + dt['BB.lower']) /2
        dt['BB.STD'] = (dt['BB.upper'] - dt['BB.SMA']) /2
        dt['BB.Position'] = round((dt['close'] - dt['BB.SMA']) / dt['BB.STD'],2)
        
        dt5 = dt.pivot(index='coin', columns='timeframe', values='BB.Position')
        
        fig5, ax5 = plt.subplots(figsize = (1.5,fig_high))
        sns.heatmap(dt5, cmap ='RdYlGn',vmin=-2, vmax=2,  linewidths = 0.30, annot = True, cbar=False).set_title("Bollinger Bands STD")
        ax5.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax5.set_xticklabels(ax5.get_xticklabels(), rotation=90, ha='center')
        ax5.set_yticklabels(ax5.get_yticklabels(), rotation=0, ha='center')
        ax5.set_xlabel('')
        ax5.set_ylabel('')
        
        
        dt6 = dt.pivot(index='coin', columns='timeframe', values='CCI')
        
        fig6, ax6 = plt.subplots(figsize = (1.5,fig_high))
        sns.heatmap(dt6, cmap ='RdYlGn',vmin=-150, vmax=150,  linewidths = 0.30, annot = True, fmt=".0f",cbar=False).set_title("CCI")
        ax6.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
        ax6.set_xticklabels(ax6.get_xticklabels(), rotation=90, ha='center')
        ax6.set_yticklabels(ax6.get_yticklabels(), rotation=0, ha='center')
        ax6.set_xlabel('')
        ax6.set_ylabel('')
        
        with tab1:
            tab1.pyplot(fig1,use_container_width= False)

        with tab2:
            tab2.pyplot(fig2,use_container_width= False)
            
        with tab3:
            tab3.pyplot(fig3,use_container_width= False)
            
        with tab4:
            tab4.pyplot(fig4,use_container_width= False)
            
        with tab5:
            tab5.pyplot(fig5,use_container_width= False)
            
        with tab6:
            tab6.pyplot(fig6,use_container_width= False)
            
        
    except:
        st.write('Check again your data!')
    
  
    
        
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")
