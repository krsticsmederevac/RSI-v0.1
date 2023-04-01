import streamlit as st
st.set_page_config( page_title = "RSI Field", page_icon = ":shark:",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})



from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd

from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Text, LabelSet
from bokeh.plotting import figure
from bokeh.models import BoxAnnotation
from bokeh.models import HoverTool
from bokeh.transform import linear_cmap
from bokeh.transform import factor_cmap
from bokeh.palettes import  RdYlGn

from bokeh.io import export_png





pocetni_simboli = ["BTC","ETH", 'BNB','LINK', 'ATOM','LTC', 'XRP', 'ADA', 'MATIC', 'DOGE', 'SOL', 'DOT','AVAX']

ponudjeni_simboli =  ["BTC","ETH", 'BNB', 'XRP', 'ADA', 'MATIC', 'DOGE', 'SOL', 'DOT',
           'LTC', 'SHIB', 'AVAX', 'LINK', 'ATOM', 'XMR', 'ETC', 'HOT',
           'UNI', 'XLM', 'FIL', 'APT', 'HBAR', 'LDO', 'NEAR', 
'VET', 'ALGO', 'ARB', 'QNT', 'APE','GRT', 'FTM', 'CFX', 'EGLD', 
              'THETA', 'AAVE', 
           'OP', 'MASK', 'DYDX', 'GMX', 'FET', 'JOE','HOOK' , 'COTI' ]

ponudjeni_intervali = ["1m", "5m", "30m", "1h", "2h", "4h", "1d","1W", "1M"]

st.sidebar.header('RSI `version 1`')

with st.spinner('Loading'):
    st.sidebar.subheader('Select TF')
    intervali = st.sidebar.selectbox('Time Frame', ponudjeni_intervali)

st.sidebar.subheader('Select Coin')
simboli = st.sidebar.multiselect('Coins',ponudjeni_simboli, pocetni_simboli)





                         
                         
usdt_lista =  [i + "USDT" for i in simboli]                         
lista_handler = []
recnik = {'coin': [], 'rsi' : []}

for i in usdt_lista:
    
    
    handler = TA_Handler(
        symbol=i,
        exchange="binance",
        screener="crypto",
        interval=intervali,
        timeout=None
        )
    
    try:
        analysis = handler.get_analysis()
        
    except: 
        print(i[:-4] + " nije pronadjen na menjacnici!")
    
    
    try:
        
        recnik['rsi'].append(round(analysis.indicators["RSI"],2))
        recnik['coin'].append(i[:-4])
    except:
            print(i[:-4] + " nema toliku istoriju!")    
    else:continue
    

    lista_handler.append(handler)
    
# print(recnik)

dt = pd.DataFrame(recnik) 
    
dt.sort_values(by=['rsi'], inplace=True)






source = ColumnDataSource(data=dict(
    coin=dt['coin'], 
    rsi=dt['rsi'],
    names=dt['coin']))


group = dt['coin']

p = figure(x_range=group, y_range=(0,101),#height=600,width=1200,  
           title="RSI")


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
color_mapper = linear_cmap(field_name = 'rsi', 
                           palette = palette, low = dt['rsi'].max(), 
                           high = dt['rsi'].min())

p.scatter(x='coin', y='rsi', size=8, source=source, fill_color=color_mapper)
p.xaxis.axis_label = 'Coin'
p.yaxis.axis_label = 'RSI' 

labels = LabelSet(x='coin', y='rsi', 
                  text='names',text_alpha = 0.9,text_font_size = '6pt',
                  text_align = 'right',
                  level='glyph',
                  x_offset = 10, y_offset = 10,
                  source=source)
p.xaxis.major_label_orientation = 1.2


p.add_tools(HoverTool(tooltips=[("Coin", "@coin"), ("rsi", "@rsi")]))

p.add_layout(labels)


st.bokeh_chart(p)

