import streamlit as st
st.set_page_config( page_title = "Crypto Data", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from streamlit_extras.app_logo import add_logo

add_logo('images/logo_black.jpg')


url1 = "https://www.tradingview.com/script/48BzLTIt-CryptoData-Coin-BTC-Quick-Chart-ic/"
url2 = 'https://www.tradingview.com/script/T1z24zxb-CryptoData-Oscillators-ic/'
url3 = 'https://www.tradingview.com/script/fGl81yI5-CryptoData-ic/'
url4 = 'https://www.tradingview.com/script/0Kur5zUX-CryptoData-Pack2-ic/'
url5 = 'https://www.tradingview.com/script/oR7our9T-CryptoData-Bollinger-Keltner-ic/'
url6 = 'https://www.tradingview.com/script/EsVAnvc5-CryptoData-Spot-vs-Futurese-ic/'
url7 = 'https://www.tradingview.com/script/ng0APBVp-CryptoData-RSI-ic/'
url8 = 'https://www.tradingview.com/script/mobbjHHQ-CryptoData-Bollinger-Keltner-RSI-ic/'
url9 = 'https://www.tradingview.com/script/1yvrKxza-CryptoData-Bands-Lines-ic/'
url10 = 'https://www.tradingview.com/script/Tw8DmRpM-CryptoData-Trend-ATH-ATL-ic/'
url11 = 'https://www.tradingview.com/script/C706lqlR-CryptoData-Coin-Volume-Spot-ic/'
url12 = 'https://www.tradingview.com/script/zPyDN1gK-CryptoData-EZ-Bands-Levels-ic/'

st.write("Check out my TradingView indicators")

st.write("[CryptoData Coin/BTC Quick Chart [+ic]](%s)" % url1)
st.write("[CryptoData EZ Bands & Levels [+ic]](%s)" % url12)
st.write("[CryptoData Spot vs Futurese [+ic]](%s)" % url6)
st.write("[CryptoData Trend & ATH/ATL [+ic]](%s)" % url10)
st.write("[CryptoData Coin Volume Spot [+ic]](%s)" % url11)

st.write("[CryptoData Bands & Lines [+ic]](%s)" % url9)
st.write("[CryptoData Bollinger, Keltner & RSI [+ic]](%s)" % url8)
st.write("[CryptoData RSI [+ic]](%s)" % url7)
st.write("[CryptoData Bollinger & Keltner [+ic]](%s)" % url5)


st.write("[CryptoData [+ic]](%s)" % url3)
st.write("[CryptoData Oscillators [+ic]](%s)" % url2)
st.write("[CryptoData Pack2 [+ic]](%s)" % url4)

st.write('\n')
st.write("Feel free to leave a tip.")
st.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
st.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
st.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
st.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")
