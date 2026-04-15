import streamlit as st
from binance.client import Client

# 1. إعدادات الصفحة
st.set_page_config(page_title="Binance Pro Bot", page_icon="⚡")
st.title("⚡ بوت بينانس الشامل والمُتداول")

try:
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # --- القسم الأول: رصد شامل للمحافظ ---
    st.header("🔍 الرصد الشامل للأرصدة")
    
    # محفظة السبوت
    spot = client.get_account()['balances']
    # محفظة التمويل
    funding = client.get_funding_asset()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 Spot")
        for a in spot:
            if float(a['free']) > 0.00001:
                st.write(f"**{a['asset']}**: {a['free']}")
    
    with col2:
        st.subheader("💳 Funding")
        for a in funding:
            if float(a['free']) > 0.00001:
                st.write(f"**{a['asset']}**: {a['free']}")

    # --- القسم الثاني: لوحة التداول ---
    st.divider()
    st.header("🛒 تنفيذ صفقات سريعة")
    
    symbol = st.text_input("اسم الزوج (مثال: BTCUSDT)", "BTCUSDT").upper()
    side = st.selectbox("نوع العملية", ["BUY", "SELL"])
    quantity = st.number_input("الكمية", min_value=0.0)

    if st.button("تنفيذ الأمر الآن 🚀"):
        if quantity > 0:
            try:
                if side == "BUY":
                    order = client.order_market_buy(symbol=symbol, quantity=quantity)
                else:
                    order = client.order_market_sell(symbol=symbol, quantity=quantity)
                st.balloons()
                st.success(f"تم تنفيذ العملية بنجاح! رقم الأمر: {order['orderId']}")
            except Exception as e:
                st.error(f"فشل التداول: {e}")
        else:
            st.warning("يرجى تحديد كمية صحيحة")

except Exception as e:
    st.error(f"⚠️ فشل الاتصال: {e}")
