import streamlit as st
from streamlit_option_menu import option_menu

def streamlit_menu():
   selected = option_menu(
              menu_title=None,  # required
              options=["RSI", "Scaner"],  # required
              icons=["house", "book", ],  # optional
              menu_icon="cast",  # optional
              default_index=0,  # optional
              orientation="horizontal",
              styles={
                  "container": {"padding": "0!important", "background-color": "#fafafa"},
                  "icon": {"color": "orange", "font-size": "25px"},
                  "nav-link": {
                      "font-size": "25px",
                      "text-align": "left",
                      "margin": "0px",
                      "--hover-color": "#eee",
                  },
                  "nav-link-selected": {"background-color": "green"},
              },
          )
         return selected
 
 
selected = streamlit_menu()
