import streamlit as st
st.set_page_config( page_title = "One Coin Analyze", page_icon = "📊",layout="centered",initial_sidebar_state="auto", menu_items = {"About": "krsticsmederevac@gmail.com"})

import extra_streamlit_components as stx

from tradingview_ta import TA_Handler, Interval, Exchange

import time
import pandas as pd
import numpy as np
import json 

import seaborn as sns
import matplotlib.pyplot as plt

