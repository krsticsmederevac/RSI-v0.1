import streamlit as st
st.set_page_config( page_title = "Crypto Data", page_icon = "📊",layout="wide",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx


url1 = "https://www.tradingview.com/script/48BzLTIt-CryptoData-Coin-BTC-Quick-Chart-ic/"
url2 = 'https://www.tradingview.com/script/T1z24zxb-CryptoData-Oscillators-ic/'
url3 = 'https://www.tradingview.com/script/fGl81yI5-CryptoData-ic/'
url4 = 'https://www.tradingview.com/script/0Kur5zUX-CryptoData-Pack2-ic/'
st.write("Check out my TradingView indicators")
st.write("CryptoData Coin/BTC Quick Chart [+ic] [link](%s)" % url1)
st.write("CryptoData Oscillators [+ic] [link](%s)" % url2)
st.write("CryptoData [+ic] [link](%s)" % url3)
st.write("CryptoData Pack2 [+ic] [link](%s)" % url4)
st.write('\n')
st.write("Feel free to leave a tip.")
st.write("Eth: 0xb77fcef5c13e1a54bdfff9a7e5268743e81325c4")
st.write("Tron: TVT4GcBP29NoiuHTttfa4QJA837rv9XZ7v")
st.write("Ltc: LRb7sR5T3L3qqG8Tbvsp8GyvsTfydSmbU8")
st.write("Btc: 1GDi8CRH6QUFw6UiPVyt7ZtD9BjmsRNAWJ")
