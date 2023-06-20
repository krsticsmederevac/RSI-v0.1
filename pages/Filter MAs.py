import streamlit as st
st.set_page_config( page_title = "Filter MAs", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

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
                      'AGLD','AST',
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
                      'MANA', 'MASK', 'MATIC', 'MBL', 'MDT', 'MKR', 'MTL', 'MINA', 'MX', 'MAGIC', 'MOB', 'METIS','MRS','MC','MED','MULTI','MOVR','MBOX',
                      'NEAR', 'NEO', 'NEXO','NKN', 'NMR', 'NYM','NULS',
                      'OCEAN', 'OGN', 'OMG', 'ONE', 'ONG', 'ONT', 'OP', 'ORN', 'OSMO', 'OXT', 'OKB','ORDI','ORBS','OG','OAX','OM',
                      'PAXG', 'PERL', 'PERP', 'PNT', 'POND', 'PSG','PEPE', 'PHA','PENDLE', 'PROM', 'POLYX', 'PYR', 'PLA','PEOPLE','PHB','PORTO','PUNDIX',
                      'QTUM', 'QNT','QUICK', 'QI',
                      'RDNT', 'REEF', 'REN', 'RNDR', 'RIF', 'RLC', 'ROSE', 'RPL', 'RSR', 'RUNE', 'RVN', 'RON','REQ','RBN','RAD',
                      'SAND', 'SC', 'SFP','SHIB', 'SKL', 'SNX', 'SOL', 'STMX', 'STORJ', 'STPT', 'STRAX', 'STX', 'SUI','SUN', 'SUPER', 
                      'SUSHI', 'SXP', 'SSV', 'STG', 'SYS', 'SLP', 'SCRT','STEEM', 'SYN', 'SNT','SPELL','SANTOS',
                      'TFUEL', 'THETA', 'TOMO', 'TRB', 'TROY', 'TRU', 'TRX', 'TWT', 'T','TOMI','TRIBE','TEL','TRAC','TLM','TVK', 'TKO',
                      'UMA', 'UNFI', 'UNI', 'UTK', 'USTC',
                      'VET', 'VITE', 'VTHO', 'VRA','VVS','VGX','VOXEL','VIDT', 'VIB',
                      'WAN', 'WAVES', 'WIN', 'WING', 'WOO','WNXM', 'WRX', 'WTC', 'WAX', 'WAXL', 'WILD','WBT','WEMIX','WAXP',
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
                         'MAGIC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'MTL',
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
                         'WAVES', 'WOO',
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

sortiranje_ponuda = ['value','coin']




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

    dt.sort_values(by='coin', inplace=True)
#     dt.sort_values(by = 'timeframe', 
#                    key= lambda x: x.map({"1m":1, "5m":2, "15m":3, "30m":4, "1h":5, "2h":6,
#                                          "4h":7, "1d":8,"1W":9, "1M":10})
#                    ,inplace = True)

    if len(dt.index) == 0:
        dt = pd.DataFrame({'coin': ["No Data"], oscilator : [0]})

    return dt
  
  
############################################################################################################################################

def grafik_oscilator_interval_pc(dt,interval,oscilator,usdt_btc,sort=True):
    
    if sort:
        dt = dt.sort_values(by=[oscilator])

    source = ColumnDataSource(data=dict(
        coin=dt['coin'], 
        indikator = dt[oscilator],
        names=dt['coin']))
    

    

    if oscilator == 'RSI':
         ime_za_naslov = 'RSI'

          

    
    now = datetime.now() + timedelta(hours=2)
    datum_vreme = now.strftime("%H:%M %d/%m/%y") 
    ime_grafika_osnovno = ime_za_naslov + ' ' + interval +  '     ' + datum_vreme

    if rsi_inverse:
        ime_grafika_dodatak = '\nRSI <= ' + str(rsi_min) + ' or RSI >= '+ str(rsi_max)
    else:
        ime_grafika_dodatak = '\n'+ str(rsi_min) + ' <= RSI <=' + str(rsi_max)
    ime_grafika = ime_grafika_osnovno + ime_grafika_dodatak
    
    
    if oscilator == 'RSI':
        x2 =  max(max(dt[oscilator]) + 5,85)
        x1 = min(min(dt[oscilator])-5, 15)
        
  
    
    
        
    p = figure(x_range=dt['coin'],y_range =(x1,x2),width=1200, #height=600,width=1200,  
               title = ime_grafika, toolbar_location='above')
    
    if len(dt.index) > 125:
        p.xaxis.major_label_text_font_size = "5pt"
        
    p.title.align = 'center'

    p.sizing_mode = 'stretch_both'
    
    
    


    palette = RdYlGn[10]
    color_mapper = linear_cmap(field_name = 'indikator', 
                               palette = palette, low = dt[oscilator].max(), 
                               high = dt[oscilator].min())

    p.scatter(x='coin', y='indikator', size=7, source=source, fill_color=color_mapper)
    
    p.xaxis.axis_label = 'Coin'
    p.yaxis.axis_label = oscilator.upper() 

    labels = LabelSet(x='coin', y='indikator', 
                      text='names',text_alpha = 0.9,text_font_size = '5pt',
                      text_align = 'center',
                      level='glyph',
                      x_offset = 0, y_offset = 6,
                      source=source)

    p.add_layout(labels)
    p.xaxis.major_label_orientation = 1.2
    

        
    if oscilator == 'RSI':

        upper1 = BoxAnnotation(bottom=80, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        upper2 = BoxAnnotation(bottom=70, fill_alpha=0.1, fill_color='palegreen')
        p.add_layout(upper2)


        lower2 = BoxAnnotation(top=30, fill_alpha=0.1, fill_color='salmon')
        p.add_layout(lower2)

        lower3 = BoxAnnotation(top=20, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower3)
        

        polovina = Span(location=50,
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
      
        rsi70 = Span(location=70,
                         line_color='olive',line_dash='dashed', line_width=2)
        p.add_layout(rsi70)
        
        rsi30 = Span(location=30,
                         line_color='salmon',line_dash='dashed', line_width=2)
        p.add_layout(rsi30)


   
    return p
  
#############################################################################################################################################################

def grafik_oscilator_interval_sp(dt,interval,oscilator,usdt_btc,sort=True):
    
    if sort:
        dt = dt.sort_values(by=[oscilator])
    else:
        dt = dt.sort_values(by=['coin'], ascending = False)
        
    source = ColumnDataSource(data=dict(
        coin=dt['coin'], 
        indikator = dt[oscilator],
        names=dt['coin']))
    



    if oscilator == 'RSI':
         ime_za_naslov = 'RSI'
  
        
        
            
    now = datetime.now() + timedelta(hours=2)
    datum_vreme = now.strftime("%H:%M %d/%m/%y") 
    ime_grafika_osnovno = ime_za_naslov + ' ' + interval  + '     ' + datum_vreme
    
    if rsi_inverse:
        ime_grafika_dodatak = '\nRSI <= ' + str(rsi_min) + ' or RSI >= '+ str(rsi_max)
    else:
        ime_grafika_dodatak = '\n'+ str(rsi_min) + ' <= RSI <=' + str(rsi_max)
    ime_grafika = ime_grafika_osnovno + ime_grafika_dodatak
  
    

    
    if oscilator == 'RSI':
        x2 =  max(max(dt[oscilator]) + 5,85)
        x1 = min(min(dt[oscilator]) - 5, 15)
        


 
    p = figure(y_range=dt['coin'],x_range =(x1,x2),height=900,#width=350,  
               title = ime_grafika, toolbar_location='above',tools ='save')

    p.title.align = 'center'

    p.sizing_mode = "stretch_width"
#     "fixed", "stretch_both", "scale_width", "scale_height", "scale_both","stretch_width","stretch_height"
    
    p.yaxis.major_label_text_font_size = '6px'
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None

    palette = RdYlGn[10]
    color_mapper = linear_cmap(field_name = 'indikator', 
                               palette = palette, low = dt[oscilator].max(), 
                               high = dt[oscilator].min())

    p.scatter(y='coin', x='indikator', size=7, source=source, fill_color=color_mapper)
    

    labels = LabelSet(y='coin', x='indikator', 
                      text='names',text_alpha = 0.9,text_font_size = '4pt',
                      text_align = 'left',
                      level='glyph',
                      x_offset = 6, y_offset = -4,
                      source=source)

    p.add_layout(labels)
    
    
    

   
        
    if oscilator == 'RSI':

        upper1 = BoxAnnotation(left=80, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        upper2 = BoxAnnotation(left=70, fill_alpha=0.15, fill_color='palegreen')
        p.add_layout(upper2)


        lower2 = BoxAnnotation(right=30, fill_alpha=0.1, fill_color='salmon')
        p.add_layout(lower2)

        lower3 = BoxAnnotation(right=20, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower3)
        

        polovina = Span(location=50,dimension='height',
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
        
        rsi70 = Span(location=70,dimension='height',
                         line_color='olive',line_dash='dashed', line_width=2)
        p.add_layout(rsi70)
        
        rsi30 = Span(location=30,dimension='height',
                         line_color='salmon',line_dash='dashed', line_width=2)
        p.add_layout(rsi30)

        

    
    return p  

  
  
#############################################################################################################################################################  

container = st.container()


tab1, tab2 = container.tabs(["📈 Smartphone format", "📋 PC format"])

container.write("Feel free to leave a tip.")
container.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
container.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
container.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
container.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")


podesavanja_korisnika = st.file_uploader("Upload Coin List",'json')  

if podesavanja_korisnika:
  
    podesavanja_korisnika_lista = json.load(podesavanja_korisnika)

    pocetni_simboli = podesavanja_korisnika_lista
#     simboli = podesavanja_korisnika_lista
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
#     if any( x not in ponudjeni_simboli for x in simboli):
       pocetni_simboli = ['BTC']
#        simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = [ 'ADA', 'AVAX', 'BNB', 'BTC', 'DOT',  'ETH', 'LINK', 'LTC',  'XRP', ]
  

ponudjeni_intervali_pocetni = 6
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0




with st.sidebar.form(key ='Form1'):
    
    
    st.header('`Single TF Analyze`')
    
    st.form_submit_button(label = "Submit")
    
    rsi_range = st.slider('RSI Value Between', min_value=0, max_value=100, value=(40,60), step=1)
    rsi_inverse = st.checkbox('Inverse Range',value = True)
  
    interval = st.selectbox('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
   
    izbor_liste_coina = st.selectbox('Coin List',['Binance Futurese', 'Top MC','Custom'],0)
    
    
    if izbor_liste_coina == 'Binance Futurese': 
        simboli = binance_futurese_list
    elif izbor_liste_coina == 'Top MC':
        simboli = top_100
    else:
        simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)


    

    kolona_sortiranja = st.selectbox('Sort by', sortiranje_ponuda,sortiranje_ponuda_pocetni)
    
    if 'BTC' in simboli:
        pocetni_coin_za_liniju = simboli.index('BTC')
    else:
         pocetni_coin_za_liniju = 0
        
    # usdt_btc = st.selectbox('Coin Line',simboli,pocetni_coin_za_liniju)
    usdt_btc = 'BTC'

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    
#############################################################################################################################################################################
    
if kolona_sortiranja:

    

    try: 
        dt = data_frame_maker(simboli, [interval], [ 'RSI'], 'USDT', ['timeframe'])

        rsi_min = min(rsi_range)
        rsi_max = max(rsi_range)
        
        if rsi_inverse:
            dt = dt[(dt.RSI <= rsi_min) | (dt.RSI >= rsi_max)]
        else:
            dt = dt[(dt.RSI >= rsi_min) & (dt.RSI <= rsi_max)]
          
        
        if kolona_sortiranja == 'coin':
            sortiranje_po_value = False
        else:
            sortiranje_po_value = True
    except: 
        st.write('No Data')    
      
    with tab1:
            
        try:
            p_rsi_sp = grafik_oscilator_interval_sp(dt[['coin','RSI']],interval,'RSI',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_rsi_sp)
        except: 
            print()  
       

    with tab2:
        try:
            p_rsi_pc = grafik_oscilator_interval_pc(dt[['coin','RSI']],interval,'RSI',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_rsi_pc)
        except: 
            print()    
       
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")
