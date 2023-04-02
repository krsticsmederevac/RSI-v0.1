import streamlit as st
st.set_page_config( page_title = "RSI Field", page_icon = ":shark:",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, LabelSet, Span, Range1d, BoxAnnotation, HoverTool
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.palettes import  RdYlGn


def data_frame_maker(simboli, interval, oscilator, usdt_btc, kolona_sortiranja, menjacnica = 'binance'):                        
                         
    usdt_ili_btc_lista =  [i + usdt_btc for i in simboli]  
    
    duzina_usdt_ili_btc = len(usdt_btc)

    lista_handler = []

    recnik = {'coin': [], oscilator : []}

    for coin in usdt_ili_btc_lista:

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

        try:
            recnik[oscilator].append(round(analysis.indicators[oscilator.upper()],2))
            recnik['coin'].append(coin[:-duzina_usdt_ili_btc])
        except:
                print(coin[:-duzina_usdt_ili_btc] + "  can't find older data.")    
        else:continue


        lista_handler.append(handler)

    dt = pd.DataFrame(recnik) 

    dt.sort_values(by=[kolona_sortiranja], inplace=True)

    if len(dt.index) == 0:
        dt = pd.DataFrame({'coin': ["No Data"], oscilator : [0]})

    return dt
  
  
  
  
def grafik_oscilator_interval(dt,interval,oscilator,usdt_btc):

    source = ColumnDataSource(data=dict(
        coin=dt['coin'], 
        rsi=dt[oscilator],
        names=dt['coin']))


    group = dt['coin']

    ime_grafika = oscilator.upper() + ' ' + interval + " " + usdt_btc

    p = figure(x_range=group, y_range=(0,101),#height=600,width=1200,  
               title = ime_grafika)

    p.title.align = 'center'

    p.sizing_mode='stretch_both'

    upper = BoxAnnotation(bottom=80, fill_alpha=0.1, fill_color='green')
    p.add_layout(upper)

    upper = BoxAnnotation(bottom=60, fill_alpha=0.1, fill_color='olive')
    p.add_layout(upper)

    lower = BoxAnnotation(top=40, fill_alpha=0.1, fill_color='red')
    p.add_layout(lower)

    lower = BoxAnnotation(top=20, fill_alpha=0.1, fill_color='firebrick')
    p.add_layout(lower)


    palette = RdYlGn[10]
    color_mapper = linear_cmap(field_name = oscilator, 
                               palette = palette, low = dt[oscilator].max(), 
                               high = dt[oscilator].min())

    p.scatter(x='coin', y=oscilator, size=8, source=source, fill_color=color_mapper)
    p.xaxis.axis_label = 'Coin'
    p.yaxis.axis_label = oscilator.upper() 

    labels = LabelSet(x='coin', y=oscilator, 
                      text='names',text_alpha = 0.9,text_font_size = '6pt',
                      text_align = 'right',
                      level='glyph',
                      x_offset = 10, y_offset = 10,
                      source=source)
    p.xaxis.major_label_orientation = 1.2


    polovina = Span(location=50,
                     line_color='orange',line_dash='dashed', line_width=1)
    p.add_layout(polovina)
    p.y_range = Range1d(0,100,bounds=(0, 100))

    hovertool_oscilator = "@" + oscilator
    p.add_tools(HoverTool(tooltips=[("Coin", "@coin"), (oscilator.upper(), hovertool_oscilator)]))

    p.add_layout(labels)
    
    return p
  
  
  
  
  
pocetni_simboli = ['ADA', 'ATOM', 'BNB', 'BTC', 'DOGE', 'DOT', 'ETH', 'LINK', 'LTC', 'MATIC', 'XRP']

ponudjeni_simboli =  ['1INCH', 'AAVE', 'ACM', 'ADA', 'AKRO', 'ALGO', 'ALICE', 'ALPHA', 'ANKR', 'ANT',
                      'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AUTO', 'AVAX', 'AXS', 
                      'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEAM', 'BEL', 'BLZ', 'BNB', 'BTC', 'BTT',
                      'BURGER', 'BZRX', 'CAKE', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COCOS', 
                      'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CTXC', 'CVC', 'DASH', 'DATA', 'DCR', 'DEGO',
                      'DENT', 'DGB', 'DIA', 'DNT', 'DOCK', 'DODO', 'DOGE', 'DOT', 'DREP', 'DUSK', 'DYDXEGLD',
                      'ENJ', 'EOS', 'EPS', 'ETC', 'ETH', 'FET', 'FIL', 'FIO', 'FIRO', 'FIS', 'FLM', 'FTM', 
                      'FTT', 'FUN', 'GBP', 'GMX', 'GRT', 'GTO', 'HARD', 'HBAR', 'HIVE', 'HNT', 'HOOK', 'HOT',
                      'ICX', 'INJ', 'IOST', 'IOTA', 'IOTX', 'IRIS', 'KAVA', 'KEY', 'KMD', 'KNC', 'KSM',
                      'LDO', 'LINA', 'LINK', 'LIT', 'LQTY', 'LRC', 'LSK', 'LTC', 'LTO', 'LUNA', 'MANA', 
                      'MATIC', 'MBL', 'MDT', 'MFT', 'MITH', 'MKR', 'MTL', 'NANO', 'NBS', 'NEAR', 'NEO', 
                      'NKN', 'NMR', 'NPXS', 'OCEAN', 'OGN', 'OMG', 'ONE', 'ONG', 'ONT', 'OP', 'ORN', 'OXT', 
                      'PAX', 'PAXG', 'PERL', 'PERP', 'PNT', 'POND', 'PSG', 'QTUM', 'RAMP', 'RDNT', 'REEF', 
                      'REN', 'REP', 'RIF', 'RLC', 'ROSE', 'RSR', 'RUNE', 'RVN', 'SAND', 'SC', 'SFP', 'SKL', 
                      'SNX', 'SOL', 'SRM', 'STMX', 'STORJ', 'STPT', 'STRAX', 'STX', 'SUN', 'SUPER', 'SUSD', 
                      'SUSHI', 'SXP', 'TCT', 'TFUEL', 'THETA', 'TOMO', 'TRB', 'TROY', 'TRU', 'TRX', 'TWT', 
                      'UMA', 'UNFI', 'UNI', 'UTK', 'VET', 'VITE', 'VTHO', 'WAN', 'WAVES', 'WIN', 'WING', 
                      'WNXM', 'WRX', 'WTC', 'XEM', 'XLM', 'XMR', 'XRP', 'XTZ', 'XVS', 'YFI', 'ZEN', 'ZIL', 'ZRXYFII']

ponudjeni_simboli.sort()



ponudjeni_intervali = ["1m", "5m", "30m", "1h", "2h", "4h", "1d","1W", "1M"]

ponudjeni_parovi = ["USDT", "BTC"]

sortiranje_ponuda = ['rsi','coin']

oscilator = 'rsi'

with st.sidebar.form(key ='Form1'):
    
    st.header('RSI `version 1`')
    
    st.form_submit_button(label = "Submite")
    
    
    interval = st.selectbox('Time Frame', ponudjeni_intervali)
    
    simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    
    kolona_sortiranja = st.selectbox('Sort by', sortiranje_ponuda)
    
    usdt_btc = st.multiselect('USDT and//or BTC',ponudjeni_parovi, 'USDT')
    
if usdt_btc and kolona_sortiranja:

    for izbor_usdt_btc in usdt_btc:
        dt = data_frame_maker(simboli, interval, oscilator, izbor_usdt_btc, kolona_sortiranja)
        p = grafik_oscilator_interval(dt,interval,oscilator,izbor_usdt_btc)
        
        st.bokeh_chart(p)

st.write("Feel free to leave a tip.")
st.write("Eth: 0xe183bf9861b995107df580e1f9fa2a5e56e9ea40")
st.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
