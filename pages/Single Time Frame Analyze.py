import streamlit as st
st.set_page_config( page_title = "Single Time Frame Analyze", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

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
                      'AAVE', 'ACM', 'ADA', 'AGIX', 'AKRO', 'ALGO', 'ALICE', 'ALPHA','APT','APE', 'ANKR', 'ANT', 'AKT',
                      'ARB', 'ARDR', 'ARPA', 'ASR', 'ATM', 'ATOM', 'AUDIO', 'AVAX', 'AXS', 'ABBC', 'AR','ASTR', 'ACH', 'API3',
                      'BADGER', 'BAL', 'BAND', 'BAT', 'BCH', 'BEL', 'BLZ', 'BNB',  'BTC', 'BURGER', 'BTTC',
                      'BLUR', 'BTG', 'BICO','BONE','BORA', 'BNX','BRISE', 'BTRST',
                      'CAKE', 'CELO', 'CELR', 'CFX', 'CHR', 'CHZ', 'CKB', 'COMP', 'COTI', 'CRV', 'CTK', 'CTSI', 'CTXC', 'CVC', 'CVX','CRO','CSPR', 'CORE','COMBO',
                      'DASH', 'DATA', 'DCR', 'DEGO', 'DENT', 'DGB', 'DIA', 'DOCK', 'DODO', 'DOGE', 'DOT', 'DREP', 'DUSK', 'DYDX', 'DAO', 'DAR', 'DAG',
                      'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 'ELF', 'EDU','ETHW','ELON','ERG',
                      'FET', 'FIL', 'FIO', 'FIRO', 'FIS', 'FLM','FLR','FLOW','FLUX', 'FTM', 'FUN', 'FXS', 'FLOKI',
                      'GALA','GBP', 'GMX', 'GRT', 'GT', 'GNO', 'GMT', 'GLM', 'GLMR',
                      'HARD', 'HBAR', 'HIVE', 'HOOK', 'HOT', 'HT','HNT',
                      'ICP','ICX', 'INJ', 'IMX', 'IOST', 'IOTA', 'IOTX', 'IRIS', 'ID', 'ILV',
                      'JOE', 'JASMY', 'JST',
                      'KAVA', 'KEY', 'KLAY', 'KMD', 'KNC', 'KSM', 'KCS' , 'KDA','KAS',
                      'LDO', 'LINA', 'LINK', 'LIT', 'LQTY', 'LRC', 'LSK', 'LTC', 'LTO', 'LUNC','LEO', 'LUNA', 'LPT','LOOKS',
                      'MANA', 'MASK', 'MATIC', 'MBL', 'MDT', 'MKR', 'MTL', 'MINA', 'MX', 'MAGIC', 'MOB', 'METIS',
                      'NEAR', 'NEO', 'NEXO','NKN', 'NMR', 'NYM',
                      'OCEAN', 'OGN', 'OMG', 'ONE', 'ONG', 'ONT', 'OP', 'ORN', 'OSMO', 'OXT', 'OKB',
                      'PAXG', 'PERL', 'PERP', 'PNT', 'POND', 'PSG','PEPE', 'PHA',
                      'QTUM', 'QNT',
                      'RDNT', 'REEF', 'REN', 'RNDR', 'RIF', 'RLC', 'ROSE', 'RPL', 'RSR', 'RUNE', 'RVN', 
                      'SAND', 'SC', 'SFP','SHIB', 'SKL', 'SNX', 'SOL', 'STMX', 'STORJ', 'STPT', 'STRAX', 'STX', 'SUI','SUN', 'SUPER', 
                      'SUSHI', 'SXP', 'SSV', 'STG', 'SYS', 'SLP', 'SCRT',
                      'TFUEL', 'THETA', 'TOMO', 'TRB', 'TROY', 'TRU', 'TRX', 'TWT', 'T',
                      'UMA', 'UNFI', 'UNI', 'UTK', 'USTC',
                      'VET', 'VITE', 'VTHO', 'VRA',
                      'WAN', 'WAVES', 'WIN', 'WING', 'WOO','WNXM', 'WRX', 'WTC', 'WAX', 'WAXL', 'WILD','WBT',
                      'XEM', 'XLM', 'XMR', 'XRP', 'XTZ', 'XVS', 'XEC', 'XDC', 'XCH', 'XRD', 'XOR',
                      'YFI', 
                      'ZEC', 'ZEN', 'ZIL',
                     ]

ponudjeni_simboli.sort()

ponudjeni_intervali = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "1d","1W", "1M"]

ponudjeni_parovi = ["USDT", "BTC"]

sortiranje_ponuda = ['value','coin']




def data_frame_maker(simboli, intervali, analitike, usdt_btc, kolona_sortiranja):                        
    
    #ako je izabran par sa BTC ili USDT da dodaje na simbole nastavak
    usdt_ili_btc_lista =  [i + usdt_btc for i in simboli]  
    
    #u slucaju da ne pronadje par da isece nastavak u obavestenju
    duzina_usdt_ili_btc = len(usdt_btc)

    gate = ['HT','GT','BTG','HNT','DAO', 'WAXL','BRISE','BTRST','XRD','ERG','XOR','WBT',]
    gate_usdt_btc = [i + usdt_btc for i in gate] 
    
    mexc = ['MX','KAS',]
    mexc_usdt_btc = [i + usdt_btc for i in mexc] 
    
    okx = ['OKB','LEO','CRO','CSPR','XCH','ETHW','BONE','BORA','CORE','NYM','LOOKS',]
    okx_usdt_btc = [i + usdt_btc for i in okx] 
    
    kucoin = ['KCS','FLR','TON','XDC','ABBC','BLUR','WILD','ELON','METIS','AKT','VRA','DAG',]
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

#     dt.sort_values(by=kolona_sortiranja, inplace=True)
    dt.sort_values(by = 'timeframe', 
                   key= lambda x: x.map({"1m":1, "5m":2, "15m":3, "30m":4, "1h":5, "2h":6,
                                         "4h":7, "1d":8,"1W":9, "1M":10})
                   ,inplace = True)

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
    
    prosecan_oscilator = round(dt[oscilator].mean(),2)
    mediana_oscilator = round(dt[oscilator].median(),2)
    std_oscilator = round(dt[oscilator].std(),2)
    min_oscilator = round(dt[oscilator].min(),2)
    max_oscilator = round(dt[oscilator].max(),2)
    
    if oscilator == 'change':
        ime_za_naslov = 'Price Change %'
    elif oscilator == 'BB.Position':
         ime_za_naslov = 'Bollinger Bands STD'
    elif oscilator == 'RSI':
         ime_za_naslov = 'RSI'
    elif oscilator == 'CCI20':
         ime_za_naslov = 'CCI'
    elif (oscilator[:3] == 'EMA') or (oscilator[:3] == 'SMA') :
         ime_za_naslov = oscilator[:-2] + ' Distance %'
          
    
    now = datetime.now() + timedelta(hours=2)
    datum_vreme = now.strftime("%H:%M %d/%m/%y") 
    ime_grafika_osnovno = ime_za_naslov + ' ' + interval + ' ' + usdt_btc + '     ' + datum_vreme
    ime_nastavak = '\nMean: ' + str(prosecan_oscilator) + '  Median: ' + str(mediana_oscilator) + '  STD: ' + str(std_oscilator) + ' Min: ' + str(min_oscilator) + ' Max: ' + str(max_oscilator)
    ime_grafika = ime_grafika_osnovno + ime_nastavak
    

    if oscilator == 'BB.Position':
        x2 =  max(max(dt[oscilator]) + 0.5, 2.5)
        x1 = min(min(dt[oscilator]) - 0.5, -2.5)
    
    if oscilator == 'RSI':
        x2 =  max(max(dt[oscilator]) + 5,85)
        x1 = min(min(dt[oscilator])-5, 15)
        
    if oscilator == 'change':
        if (max(dt[oscilator]) >= 0 and  min(dt[oscilator]) < 0) :
            distanca = max (abs((max(dt[oscilator]) + min(dt[oscilator]))) * 0.3 , 2)
        else:
            distanca = max(abs((max(dt[oscilator]) - min(dt[oscilator]))) *0.3 , 2)
        
        
        x2 = max(max(dt[oscilator]) + distanca, 1)
        x1 = min(min(dt[oscilator]) - distanca, -1)
        
    if (oscilator[:3] == 'EMA') or (oscilator[:3] == 'SMA') :
        if (max(dt[oscilator]) >= 0 and  min(dt[oscilator]) < 0) :
            distanca = max(abs((max(dt[oscilator]) + min(dt[oscilator]))) * 0.3 , 2)
        else:
            distanca = max(abs((max(dt[oscilator]) - min(dt[oscilator]))) *0.3 , 2)

        x2 = max(max(dt[oscilator]) + distanca, 1)
        x1 = min(min(dt[oscilator]) - distanca, -1)
 
  
    if oscilator == 'CCI20' :
        if (max(dt[oscilator]) >= 0 and  min(dt[oscilator]) < 0) :
            distanca = max(abs((max(dt[oscilator]) + min(dt[oscilator]))) * 0.3 , 2)
        else:
            distanca = max(abs((max(dt[oscilator]) - min(dt[oscilator]))) *0.3 , 2)
        
        x2 = max(max(dt[oscilator]) + distanca, 150)
        x1 = min(min(dt[oscilator]) - distanca, -150)
    

    p = figure(x_range=dt['coin'],y_range =(x1,x2),#height=600,width=1200,  
               title = ime_grafika, toolbar_location='above')

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
    
    
    
    try:
        btc_location = Span(location= dt[dt.coin == usdt_btc][oscilator].values[0],
                             line_color='darkviolet',line_dash='dashed', line_width=1.5)
        p.add_layout(btc_location)
    except:
        print()
    
    
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


        
    if oscilator == 'change':

        upper1 = BoxAnnotation(bottom=0, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)



        lower2 = BoxAnnotation(top=0, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower2)

        polovina = Span(location=0,
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
    
    if (oscilator[:3] == 'EMA') or (oscilator[:3] == 'SMA') :
        
        upper1 = BoxAnnotation(bottom=0, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        lower2 = BoxAnnotation(top=0, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower2)

        polovina = Span(location=0,
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
    
    
    if oscilator == 'CCI20':

        upper1 = BoxAnnotation(bottom=100, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        upper2 = BoxAnnotation(bottom=0, fill_alpha=0.15, fill_color='palegreen')
        p.add_layout(upper2)


        lower2 = BoxAnnotation(top=0, fill_alpha=0.1, fill_color='salmon')
        p.add_layout(lower2)

        lower3 = BoxAnnotation(top=-100, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower3)
        

        polovina = Span(location=0,
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
        
        rsi70 = Span(location=100,
                         line_color='olive',line_dash='dashed', line_width=2)
        p.add_layout(rsi70)
        
        rsi30 = Span(location=-100,
                         line_color='salmon',line_dash='dashed', line_width=2)
        p.add_layout(rsi30)
   
    return p
  
#############################################################################################################################################################

def grafik_oscilator_interval_sp(dt,interval,oscilator,usdt_btc,sort=True):
    
    if sort:
        dt = dt.sort_values(by=[oscilator])

    source = ColumnDataSource(data=dict(
        coin=dt['coin'], 
        indikator = dt[oscilator],
        names=dt['coin']))
    
    prosecan_oscilator = round(dt[oscilator].mean(),2)
    mediana_oscilator = round(dt[oscilator].median(),2)
#     std_oscilator = round(dt[oscilator].std(),2)

    if oscilator == 'change':
        ime_za_naslov = 'Price Change %'
    elif oscilator == 'BB.Position':
         ime_za_naslov = 'Bollinger Bands STD'
    elif oscilator == 'RSI':
         ime_za_naslov = 'RSI'
    elif oscilator == 'CCI20':
         ime_za_naslov = 'CCI'
    elif (oscilator[:3] == 'EMA') or (oscilator[:3] == 'SMA') :
         ime_za_naslov = oscilator[:-2] + ' Distance %'
            
    now = datetime.now() + timedelta(hours=2)
    datum_vreme = now.strftime("%H:%M %d/%m/%y") 
    ime_grafika_osnovno = ime_za_naslov + ' ' + interval + ' ' + usdt_btc + '     ' + datum_vreme
    
    ime_nastavak = '\nMean: ' + str(prosecan_oscilator) + '  Median: ' + str(mediana_oscilator) #+ '  STD: ' + str(std_oscilator)
    ime_grafika = ime_grafika_osnovno + ime_nastavak
    

        
    if oscilator == 'BB.Position':
        x2 =  max(max(dt[oscilator]) + 0.5, 2.5)
        x1 = min(min(dt[oscilator]) - 0.5, -2.5)
    
    if oscilator == 'RSI':
        x2 =  max(max(dt[oscilator]) + 5,85)
        x1 = min(min(dt[oscilator]) - 5, 15)
        
    if oscilator == 'change':
        if (max(dt[oscilator]) >= 0 and  min(dt[oscilator]) < 0) :
            distanca = max (abs((max(dt[oscilator]) + min(dt[oscilator]))) * 0.3 , 2)
        else:
            distanca = max(abs((max(dt[oscilator]) - min(dt[oscilator]))) *0.3 , 2)
        
        
        x2 = max(max(dt[oscilator]) + distanca, 1)
        x1 = min(min(dt[oscilator]) - distanca, -1)
        
    if (oscilator[:3] == 'EMA') or (oscilator[:3] == 'SMA') :
        if (max(dt[oscilator]) >= 0 and  min(dt[oscilator]) < 0) :
            distanca = max(abs((max(dt[oscilator]) + min(dt[oscilator]))) * 0.3 , 2)
        else:
            distanca = max(abs((max(dt[oscilator]) - min(dt[oscilator]))) *0.3 , 2)
        
        
        x2 = max(max(dt[oscilator]) + distanca, 1)
        x1 = min(min(dt[oscilator]) - distanca, -1)
        
    if oscilator == 'CCI20' :
        if (max(dt[oscilator]) >= 0 and  min(dt[oscilator]) < 0) :
            distanca = max(abs((max(dt[oscilator]) + min(dt[oscilator]))) * 0.3 , 2)
        else:
            distanca = max(abs((max(dt[oscilator]) - min(dt[oscilator]))) *0.3 , 2)
        
        x2 = max(max(dt[oscilator]) + distanca, 150)
        x1 = min(min(dt[oscilator]) - distanca, -150)

 
    p = figure(y_range=dt['coin'],x_range =(x1,x2),#width=350,height=600,  
               title = ime_grafika, toolbar_location='above',tools ='save')

    p.title.align = 'center'

    p.sizing_mode = 'stretch_width'
#     "fixed", "stretch_both", "scale_width", "scale_height", "scale_both"
    
    p.yaxis.major_label_text_font_size = '6px'
    p.toolbar.active_drag = None
    p.toolbar.active_scroll = None
    p.toolbar.active_tap = None

    palette = RdYlGn[10]
    color_mapper = linear_cmap(field_name = 'indikator', 
                               palette = palette, low = dt[oscilator].max(), 
                               high = dt[oscilator].min())

    p.scatter(y='coin', x='indikator', size=7, source=source, fill_color=color_mapper)
    
#     p.xaxis.axis_label = oscilator.upper() 
#     p.yaxis.axis_label = 'Coin'

    labels = LabelSet(y='coin', x='indikator', 
                      text='names',text_alpha = 0.9,text_font_size = '4pt',
                      text_align = 'left',
                      level='glyph',
                      x_offset = 6, y_offset = -4,
                      source=source)

    p.add_layout(labels)
    
    
    
    try:
        btc_location = Span(location= dt[dt.coin == usdt_btc][oscilator].values[0],dimension='height',
                             line_color='darkviolet',line_dash='dashed', line_width=1.5)
        p.add_layout(btc_location)
    except:
        print()
        
        
    
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

        
    if oscilator == 'change':

        upper1 = BoxAnnotation(left=0, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)



        lower2 = BoxAnnotation(right=0, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower2)

        polovina = Span(location=0,dimension='height',
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
        
    if (oscilator[:3] == 'EMA') or (oscilator[:3] == 'SMA') :
        
        upper1 = BoxAnnotation(left=0, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        lower2 = BoxAnnotation(right=0, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower2)

        polovina = Span(location=0,dimension='height',
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
        
        
    
    if oscilator == 'CCI20':

        upper1 = BoxAnnotation(left=100, fill_alpha=0.2, fill_color='olive')
        p.add_layout(upper1)

        upper2 = BoxAnnotation(left=0, fill_alpha=0.15, fill_color='palegreen')
        p.add_layout(upper2)


        lower2 = BoxAnnotation(right=0, fill_alpha=0.1, fill_color='salmon')
        p.add_layout(lower2)

        lower3 = BoxAnnotation(right=-100, fill_alpha=0.2, fill_color='red')
        p.add_layout(lower3)
        

        polovina = Span(location=0,dimension='height',
                         line_color='orange',line_dash='dashed', line_width=2)
        p.add_layout(polovina)
        
        rsi70 = Span(location=100,dimension='height',
                         line_color='olive',line_dash='dashed', line_width=2)
        p.add_layout(rsi70)
        
        rsi30 = Span(location=-100,dimension='height',
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
    
    if any( x not in ponudjeni_simboli for x in pocetni_simboli):
       pocetni_simboli = ['BTC']
       st.write('Bad input file, please try again.') 
      
    
else:
    pocetni_simboli = [ 'AAVE', 'ADA', 'AGIX', 'ALGO', 'ANKR', 'APE', 'APT', 'ARB', 'ATOM', 'AUDIO', 'AVAX', 'AXS','BCH', 'BNB', 'BTC','CRO',
                       'CAKE', 'CFX', 'CHZ', 'CRV', 'CVX', 'DASH', 'DOGE', 'DOT', 'DYDX', 'EGLD', 'ENJ', 'EOS', 'ETC', 'ETH', 
                       'FET', 'FIL', 'FLOW', 'FTM', 'FXS', 'GALA', 'GMX', 'GRT', 'HBAR', 'HOOK', 'HOT', 'ICP', 'ID', 'IMX', 'INJ', 'IOTA', 'KAVA', 
                       'KLAY', 'LDO','LEO', 'LINK', 'LQTY', 'LTC', 'LUNC', 'MANA', 'MASK', 'MATIC', 'MINA', 'MKR', 'NEAR', 'NEO', 'NEXO', 
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
    
    
    usdt_btc = st.selectbox('Coin Line',ponudjeni_simboli,ponudjeni_simboli.index('BTC'))
    

    podesavanja = simboli

    json_podesavanja = json.dumps(podesavanja)
    
    
#############################################################################################################################################################################
    
if usdt_btc and kolona_sortiranja:

    

    try: 
        dt = data_frame_maker(simboli, [interval], [ 'close','low','high','BB.upper','BB.lower','RSI','change',"EMA200",'EMA50',"EMA100",'SMA50',"SMA100",'SMA200','CCI20'], 'USDT', ['timeframe'])
    
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
        dt['BB.Position'] = (dt['close'] - dt['BB.SMA']) / dt['BB.STD']


        dt['EMA200 %'] = -(dt['EMA200'] - dt['close'])/dt['close'] * 100
        dt['EMA100 %'] = -(dt['EMA100'] - dt['close'])/dt['close'] * 100
        dt['EMA50 %'] = -(dt['EMA50'] - dt['close'])/dt['close'] * 100

        dt['SMA200 %'] = -(dt['SMA200'] - dt['close'])/dt['close'] * 100
        dt['SMA100 %'] = -(dt['SMA100'] - dt['close'])/dt['close'] * 100
        dt['SMA50 %'] = -(dt['SMA50'] - dt['close'])/dt['close'] * 100
    
    
        
        
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
        try:
            p_bb_sp = grafik_oscilator_interval_sp(dt[['coin','BB.Position']],interval,'BB.Position',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_bb_sp)
        except: 
            print()  
        try:
            p_ch_sp = grafik_oscilator_interval_sp(dt[['coin','change']],interval,'change',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_ch_sp)
        except: 
            print()  
        try:
            p_cci_sp = grafik_oscilator_interval_sp(dt[['coin','CCI20']],interval,'CCI20',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_cci_sp)
        except: 
            print()
            

        try:
            p_ema200_sp = grafik_oscilator_interval_sp(dt[['coin','EMA200 %']],interval,'EMA200 %',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_ema200_sp)
        except: 
            print()    
        try:
            p_ema100_sp = grafik_oscilator_interval_sp(dt[['coin','EMA100 %']],interval,'EMA100 %',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_ema100_sp)
        except: 
            print()    
        try:
            p_ema50_sp = grafik_oscilator_interval_sp(dt[['coin','EMA50 %']],interval,'EMA50 %',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_ema50_sp)
        except: 
            print()
        try:
            p_sma200_sp = grafik_oscilator_interval_sp(dt[['coin','SMA200 %']],interval,'SMA200 %',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_sma200_sp)
        except: 
            print()
        try:
            p_sma100_sp = grafik_oscilator_interval_sp(dt[['coin','SMA100 %']],interval,'SMA100 %',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_sma100_sp)
        except: 
            print()
        try:
            p_sma50_sp = grafik_oscilator_interval_sp(dt[['coin','SMA50 %']],interval,'SMA50 %',usdt_btc,sortiranje_po_value)
            tab1.bokeh_chart(p_sma50_sp)
        except: 
            print()

    with tab2:
        try:
            p_rsi_pc = grafik_oscilator_interval_pc(dt[['coin','RSI']],interval,'RSI',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_rsi_pc)
        except: 
            print()    
        try:
            p_bb_pc = grafik_oscilator_interval_pc(dt[['coin','BB.Position']],interval,'BB.Position',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_bb_pc)
        except: 
            print()
        try:
            p_ch_pc = grafik_oscilator_interval_pc(dt[['coin','change']],interval,'change',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_ch_pc)
        except: 
            print()
            
        try:
            p_cci_pc = grafik_oscilator_interval_pc(dt[['coin','CCI20']],interval,'CCI20',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_cci_pc)
        except: 
            print()
            
        try:
            p_ema200_pc = grafik_oscilator_interval_pc(dt[['coin','EMA200 %']],interval,'EMA200 %',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_ema200_pc)
        except: 
            print()
        try:
            p_ema100_pc = grafik_oscilator_interval_pc(dt[['coin','EMA100 %']],interval,'EMA100 %',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_ema100_pc)
        except: 
            print()
        try:
            p_ema50_pc = grafik_oscilator_interval_pc(dt[['coin','EMA50 %']],interval,'EMA50 %',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_ema50_pc)
        except: 
            print()
        try:   
            p_sma200_pc = grafik_oscilator_interval_pc(dt[['coin','SMA200 %']],interval,'SMA200 %',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_sma200_pc)
        except: 
            print()
        try:
            p_sma100_pc = grafik_oscilator_interval_pc(dt[['coin','SMA100 %']],interval,'SMA100 %',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_sma100_pc)
        except: 
            print()
        try:
            p_sma50_pc = grafik_oscilator_interval_pc(dt[['coin','SMA50 %']],interval,'SMA50 %',usdt_btc,sortiranje_po_value)
            tab2.bokeh_chart(p_sma50_pc)
        except: 
            print()
            
container.download_button("Download Coin List",json_podesavanja,"my_coin_list.json","application/json")
