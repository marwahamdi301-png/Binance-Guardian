import streamlit as st
from binance.client import Client

st.title("💰 حسابك الحقيقي")

try:
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    client = Client(api_key, api_secret)
    asset = client.get_asset_balance(asset='USDT')
    st.success(f"الرصيد: {asset['free']} USDT")
except Exception as e:
    st.error("تأكد من المفاتيح في Secrets")
