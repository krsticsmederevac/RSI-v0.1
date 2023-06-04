import streamlit as st
st.set_page_config( page_title = "Single Time Frame Analyze", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import numpy as np
import time
import pandas as pd
import json 

import matplotlib.pyplot
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, LabelSet, Span, Range1d, BoxAnnotation, HoverTool, Label, HBar
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
from bokeh.palettes import  RdYlGn


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
  
  
  

def grafik_oscilator_interval_pc(dt,interval,oscilator,usdt_btc,sort=True):
    
    if sort:
        dt = dt.sort_values(by=[oscilator])

    source = ColumnDataSource(data=dict(
        coin=dt['coin'], 
        indikator = dt[oscilator],
        names=dt['coin']))
    
    prosecan_oscilator = round(dt[oscilator].mean(),2)
    mediana_oscilator = round(dt[oscilator].median(),2)
    std_oscilator = round(dt[oscilator].std(),2)

    ime_grafika_osnovno = oscilator.upper() + ' ' + interval + ' ' + usdt_btc 
    ime_nastavak = '\nMean: ' + str(prosecan_oscilator) + '  Median: ' + str(mediana_oscilator) + '  STD: ' + str(std_oscilator)
    ime_grafika = ime_grafika_osnovno + ime_nastavak
 
    p = figure(x_range=dt['coin'], y_range=(min(dt[oscilator])*1.05,max(dt[oscilator])*1.05),#height=600,width=1200,  
               title = ime_grafika, toolbar_location=None)

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

    
    if oscilator == 'BB.Position':

        upper1 = BoxAnnotation(bottom=2, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        upper2 = BoxAnnotation(bottom=1, fill_alpha=0.1, fill_color='palegreen')
        p.add_layout(upper2)

        upper3 = BoxAnnotation(bottom=0, fill_alpha=0.1, fill_color='cornsilk')
        p.add_layout(upper3)

        lower1 = BoxAnnotation(top=-1, fill_alpha=0.1, fill_color='salmon')
        p.add_layout(lower1)

        lower2 = BoxAnnotation(top=-2, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower2)

        lower3 = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='cornsilk')
        p.add_layout(lower3)

        polovina = Span(location=0,
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)

        bb_up = Span(location=2,
                         line_color='dodgerblue', line_dash='dashed', line_width=2)
        p.add_layout(bb_up)

        bb_down = Span(location=-2,
                         line_color='dodgerblue',line_dash='dashed', line_width=2)
        p.add_layout(bb_down)
        
    
    return p
  
  

def grafik_oscilator_interval_sp(dt,interval,oscilator,usdt_btc,sort=True):
    
    if sort:
        dt = dt.sort_values(by=[oscilator])

    source = ColumnDataSource(data=dict(
        coin=dt['coin'], 
        indikator = dt[oscilator],
        names=dt['coin']))
    
    prosecan_oscilator = round(dt[oscilator].mean(),2)
    mediana_oscilator = round(dt[oscilator].median(),2)
    std_oscilator = round(dt[oscilator].std(),2)

    ime_grafika_osnovno = oscilator.upper() + ' ' + interval + ' ' + usdt_btc 
    ime_nastavak = '\nMean: ' + str(prosecan_oscilator) + '  Median: ' + str(mediana_oscilator) + '  STD: ' + str(std_oscilator)
    ime_grafika = ime_grafika_osnovno + ime_nastavak
 
    p = figure(y_range=dt['coin'],x_range =(min(dt[oscilator])*1.05,max(dt[oscilator])*1.05),#height=600,width=1200,  
               title = ime_grafika, toolbar_location=None)

    p.title.align = 'center'

    p.sizing_mode = 'scale_height'
#     "fixed", "stretch_both", "scale_width", "scale_height", "scale_both"
    
    


    palette = RdYlGn[10]
    color_mapper = linear_cmap(field_name = 'indikator', 
                               palette = palette, low = dt[oscilator].max(), 
                               high = dt[oscilator].min())

    p.scatter(y='coin', x='indikator', size=7, source=source, fill_color=color_mapper)
    
    p.xaxis.axis_label = oscilator.upper() 
    p.yaxis.axis_label = 'Coin'

    labels = LabelSet(y='coin', x='indikator', 
                      text='names',text_alpha = 0.9,text_font_size = '5pt',
                      text_align = 'left',
                      level='glyph',
                      x_offset = 6, y_offset = -3,
                      source=source)

    p.add_layout(labels)
#     p.xaxis.major_label_orientation = 1.2

    
    if oscilator == 'BB.Position':

        upper1 = BoxAnnotation(left=2, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        upper2 = BoxAnnotation(left=1, fill_alpha=0.1, fill_color='palegreen')
        p.add_layout(upper2)

        upper3 = BoxAnnotation(left=0, fill_alpha=0.1, fill_color='cornsilk')
        p.add_layout(upper3)

        lower1 = BoxAnnotation(right=-1, fill_alpha=0.1, fill_color='salmon')
        p.add_layout(lower1)

        lower2 = BoxAnnotation(right=-2, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower2)

        lower3 = BoxAnnotation(right=0, fill_alpha=0.1, fill_color='cornsilk')
        p.add_layout(lower3)

        polovina = Span(location=0,dimension='height',
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)

        bb_up = Span(location=2, dimension='height',
                         line_color='dodgerblue', line_dash='dashed', line_width=2)
        p.add_layout(bb_up)

        bb_down = Span(location=-2,dimension='height',
                         line_color='dodgerblue',line_dash='dashed', line_width=2)
        p.add_layout(bb_down)

    return p  
  
  
  

ponudjeni_simboli =  ['RLC', 'PEPE','ID','JOE', '1INCH', 'AAVE', 'ACM', 'ADA', 'AGIX', 'AKRO', 'ALGO', 'ALICE', 'ALPHA','APT','APE', 'ANKR', 'ANT',
                      'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AVAX', 'AXS', 
                      'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLZ', 'BNB',  'BTC', 
                      'BURGER', 'CAKE', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 
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

sortiranje_ponuda = ['value','coin']

# oscilator = 'rsi'



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
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = ['1INCH', 'AAVE', 'ADA', 'AGIX', 'ALGO', 'ANKR', 'APE', 'APT', 'ARB', 'ATOM', 'AUDIO', 'AVAX', 'BCH', 'BNB', 'BTC',
                       'CAKE', 'CFX', 'CHZ', 'CRV', 'CVX', 'DASH', 'DOGE', 'DOT', 'DYDX', 'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 
                       'FET', 'FIL', 'FLOW', 'FTM', 'FXS', 'GALA', 'GMX', 'GRT', 'HBAR', 'HOOK', 'HOT', 'ICP', 'ID', 'IMX', 'INJ', 'IOTA', 'KAVA', 
                       'KLAY', 'LDO', 'LINK', 'LQTY', 'LTC', 'LUNC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'NEAR', 'NEO', 'NEXO', 
                       'OCEAN', 'OP', 'OSMO', 'PEPE', 'QNT', 'RNDR', 'ROSE', 'RPL', 'RUNE', 'RVN', 'SAND', 
                       'SHIB', 'SNX', 'SOL', 'STX', 'THETA', 'TRX', 'TWT', 'UNI', 'VET', 'WOO', 'XLM', 'XMR', 'XRP', 'XTZ', 'ZEC', 'ZEN', 'ZIL']
  

ponudjeni_intervali_pocetni = 6
ponudjeni_parovi_pocetni = 0
sortiranje_ponuda_pocetni = 0






with st.sidebar.form(key ='Form1'):
    
    
    st.header('`Single TF Analyze`')
    
    st.form_submit_button(label = "Submit")
    
    
    interval = st.selectbox('Time Frame', ponudjeni_intervali,ponudjeni_intervali_pocetni)
    
        
   
    simboli = st.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)
    
        

    kolona_sortiranja = st.selectbox('Sort by', sortiranje_ponuda,sortiranje_ponuda_pocetni)
    
    
    usdt_btc = st.selectbox('USDT or BTC',ponudjeni_parovi,ponudjeni_parovi_pocetni)
    
    
#     chart_table = st.multiselect('Chart and/or Table', ['Chart','Table'],'Chart')
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    

    
if usdt_btc and kolona_sortiranja:

    for izbor_usdt_btc in usdt_btc:
      
        dt = data_frame_maker(simboli, interval, [ 'close','low','high','BB.upper','BB.lower','RSI','change'], izbor_usdt_btc, ['timeframe'])
        
        conditions = [
        (dt['BB.upper'].isna() | dt['BB.lower'].isna() ),
        ((dt['BB.upper']<= dt.high) | (dt['BB.upper']<= dt.close)),
        ((dt['BB.lower']>= dt.low) | (dt['BB.lower']>=dt.close)),
        ((dt['BB.upper']> dt.high) | (dt['BB.upper']> dt.close) | (dt['BB.lower']< dt.low) | (dt['BB.lower']<dt.close))
        ]
        
        values = [np.nan, 'UP','LOW','']

        dt['BB'] =np.select(conditions,values)
        
        dt['BB.SMA'] =  (dt['BB.upper'] + dt['BB.lower']) /2
        dt['BB.STD'] = (dt['BB.upper'] - dt['BB.SMA']) /2
        dt['BB.Position'] = round((dt['close'] - dt['BB.SMA']) / dt['BB.STD'],2)
        
        
        with tab1:
            if kolona_sortiranja == 'coin':
                sortiranje = False
            p_rsi_sp = grafik_oscilator_interval_sp(dt[['coin','RSI']],interval,'RSI',izbor_usdt_btc,sortiranje)
            tab1.bokeh_chart(p_rsi_sp)
        
        with tab2:
            p_rsi_pc = grafik_oscilator_interval_pc(dt[['coin','RSI']],interval,'RSI',izbor_usdt_btc,sortiranje)
            tab2.bokeh_chart(p_rsi_pc)
            
        
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")
