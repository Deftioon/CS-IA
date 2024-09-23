import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import src.auth as auth

auth.authenticate('config.yaml')