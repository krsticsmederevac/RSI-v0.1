import streamlit as st
st.set_page_config( page_title = "Crypto Data", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd
import json 

import matplotlib.pyplot
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, LabelSet, Span, Range1d, BoxAnnotation, HoverTool, Label
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
               title = ime_grafika, toolbar_location="above")

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
    p.y_range = Range1d(15,85,bounds=(0, 100))
    
    prosecan_rsi = dt[oscilator].mean()
    mediana_rsi = dt[oscilator].median()
    
    prosek_rsi = Label(x=len(dt)//2 - 4, y=17, text='Mean: ' + str(prosecan_rsi)[:4] +'  Median: ' + str(mediana_rsi)[:4], text_color = 'green' ,text_font_size = '12pt' )

    p.add_layout(prosek_rsi)

    hovertool_oscilator = "@" + oscilator
    p.add_tools(HoverTool(tooltips=[("Coin", "@coin"), (oscilator.upper(), hovertool_oscilator)]))

    p.add_layout(labels)
    
    return p
  
  


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

sortiranje_ponuda = ['rsi','coin']

oscilator = 'rsi'



container = st.container()

tab1, tab2 = container.tabs(["📈 Chart", "📋 Table"])




podesavanja_korisnika = st.file_uploader("Upload Coin List",'json')  

if podesavanja_korisnika:
  
    podesavanja_korisnika_lista = json.load(podesavanja_korisnika)

    pocetni_simboli = podesavanja_korisnika_lista
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = [ 'ADA',  'ATOM', 'AVAX',  'BNB', 'BTC', 'DOT', 'ETH', 'LINK', 'LTC', 'MATIC', ]
  

ponudjeni_intervali_pocetni = 5
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0






with st.sidebar.form(key ='Form1'):
    
    
    st.header('RSI `version 1`')
    
    st.form_submit_button(label = "Submite")
    
    
    interval = st.selectbox('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
        
   
    simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    
        

    kolona_sortiranja = st.selectbox('Sort by', sortiranje_ponuda,sortiranje_ponuda_pocetni)
    
    
    usdt_btc = st.multiselect('USDT and/or BTC',ponudjeni_parovi,ponudjeni_parovi[ponudjeni_parovi_pocetni])
    
    
    chart_table = st.multiselect('Chart and/or Table', ['Chart','Table'],'Chart')
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    

    
if usdt_btc and kolona_sortiranja:

    for izbor_usdt_btc in usdt_btc:
      
        dt = data_frame_maker(simboli, interval, oscilator, izbor_usdt_btc, kolona_sortiranja)
        p = grafik_oscilator_interval(dt,interval,oscilator,izbor_usdt_btc)
        dt = dt.set_index('coin')
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
