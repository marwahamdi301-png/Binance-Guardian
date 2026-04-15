import streamlit as st
from binance.client import Client

st.set_page_config(page_title="Binance Tracker", page_icon="💰")
st.title("💰 محفظتي: سبوت + تمويل")

try:
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # 1. جلب أرصدة السبوت
    spot_assets = client.get_account()['balances']
    
    # 2. جلب أرصدة التمويل (Funding)
    funding_assets = client.get_funding_asset()

    st.write("### 📊 النتائج التي عثرنا عليها:")
    
    found = False

    # فحص أرصدة السبوت
    for asset in spot_assets:
        free = float(asset['free'])
        if free > 0.00000001:
            st.success(f"**{asset['asset']}** (في السبوت): {free:,.8f}")
            found = True

    # فحص أرصدة التمويل
    for asset in funding_assets:
        free = float(asset['free'])
        if free > 0.00000001:
            st.info(f"**{asset['asset']}** (في التمويل): {free:,.8f}")
            found = True
            
    if not found:
        st.warning("⚠️ لم يتم العثور على مبالغ في السبوت أو التمويل. تأكد من مكان عملاتك في تطبيق بينانس.")

except Exception as e:
    st.error(f"⚠️ خطأ: {e}")
    st.info("تأكد من تفعيل صلاحيات القراءة في الـ API.")
