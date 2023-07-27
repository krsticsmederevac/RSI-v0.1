import streamlit as st
st.set_page_config( page_title = "Single Coin Multiple TF", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import numpy as np
import pandas as pd
import json 

from datetime import datetime, timedelta

import matplotlib.pyplot
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, LabelSet, Span, Range1d, BoxAnnotation, HoverTool, Label, HBar
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.palettes import  RdYlGn


ponudjeni_simboli =  [ '1INCH', 
                      'AAVE', 'ACM', 'ADA', 'AGIX', 'AKRO', 'ALGO', 'ALICE', 'ALPHA','APT','APE', 'ANKR', 'ANT', 'AKT','AMB','ATA','ACA','ADX',
                      'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AVAX', 'AXS', 'ABBC', 'AR','ASTR', 'ACH', 'API3','ASTRAFER','ALI', 'AMP','ALPINE',
                      'AGLD','AST','AUCTION',
                      'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLZ', 'BNB',  'BTC', 'BURGER', 'BTTC','BABYDOGE','BOND',
                      'BLUR', 'BTG', 'BICO','BONE','BORA', 'BNX','BRISE', 'BTRST', 'BDX', 'BAKE','BTS', 'BETA','BAR','BSW',
                      'CAKE', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CTXC', 'CVC', 'CVX','CRO','CSPR', 'CORE','COMBO',
                      'CHSB','C98','CQT','CFG','CITY', 'CLV',
                      'DASH', 'DATA', 'DCR', 'DEGO', 'DENT', 'DGB', 'DIA', 'DOCK', 'DODO', 'DOGE', 'DOT', 'DREP', 'DUSK', 'DYDX', 'DAO', 'DAR', 'DAG', 'DFI',
                      'DERO','DEXE', 'DESO','DKA','DEFI',
                      'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 'ELF', 'EDU','ETHW','ELON','ERG', 'EWT','ENS','ERN', 'EPX',
                      'FET', 'FIL', 'FIO', 'FIRO', 'FIS', 'FLM','FLR','FLOW','FLUX', 'FTM', 'FUN', 'FXS', 'FLOKI','FIDA', 'FORTH','FRONT',
                      'GALA','GBP', 'GMX', 'GRT', 'GT', 'GNO', 'GMT', 'GLM', 'GLMR','GNS','GAL','GTC','GAS',
                      'HARD', 'HBAR', 'HIVE', 'HOOK', 'HOT', 'HT','HNT','HFT','HIGH',
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
                      'SUSHI', 'SXP', 'SSV', 'STG', 'SYS', 'SLP', 'SCRT','STEEM', 'SYN', 'SNT','SPELL','SANTOS',
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
                         'HBAR', 'HFT', 'HIGH', 'HOOK', 'HOT',
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

tab1= container.tabs(["📋Coin"]) 



container.write("Feel free to leave a tip.")
container.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
container.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
container.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
container.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")


pocetni_simboli = [ 'BTC' ]
  

ponudjeni_intervali_pocetni = ['1h', '4h', '1d','1W']
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0


with st.sidebar.form(key ='Form3'):
    
    
    st.header('`Single Coin Multiple TF`')
    
    st.form_submit_button(label = "Submit")
    
    
    interval = st.multiselect('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
    simboli = st.selectbox('Coins',ponudjeni_simboli, 42)
    

       
    
    usdt_btc = 'USDT' #st.selectbox('USDT or BTC',ponudjeni_parovi,0)
    

    podesavanja = simboli

