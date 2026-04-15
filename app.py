import streamlit as st
from binance.client import Client
from binance.exceptions import BinanceClientException

st.title("💰 حسابك الحقيقي")

try:
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    client = Client(api_key, api_secret)
    
    asset = client.get_asset_balance(asset='USDT')
    
    # Validate the response before accessing
    if asset and 'free' in asset:
        balance = float(asset['free'])
        st.success(f"الرصيد: {balance:.2f} USDT")
    else:
        st.warning("لم يتم العثور على رصيد USDT")
        
except BinanceClientException as e:
    st.error(f"خطأ في المفاتيح أو الاتصال: {e}")
except KeyError:
    st.error("تأكد من المفاتيح في Secrets")
except Exception as e:
    st.error(f"خطأ غير متوقع: {str(e)}")
