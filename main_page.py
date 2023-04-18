import streamlit as st
from streamlit_option_menu import option_menu

def streamlit_menu():
   selected = option_menu(
              menu_title=None,  # required
              options=["RSI Field", "Scaner"],  # required
              icons=["house", "book", ],  # optional
              menu_icon="cast",  # optional
              default_index=0,  # optional
              orientation="horizontal"
          )
   return selected
 
 
selected = streamlit_menu()
