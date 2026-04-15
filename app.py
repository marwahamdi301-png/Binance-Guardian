import streamlit as st
from binance.client import Client
import os

st.set_page_config(page_title="Binance Mega Bot", page_icon="⚡")
st.title("⚡ بوت جمال الشامل: رصد + تداول")

try:
    # 1. جلب المفاتيح
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    # 2. إعداد الاتصال باستخدام سيرفرات بديلة متعددة
    # سنحاول تجربة رابط السيرفر الأمريكي أو السيرفرات الاحتياطية
    client = Client(api_key, api_secret)
    
    # جرب تغيير هذا الرابط في كل مرة إذا استمر الخطأ:
    # خيار 1: https://api.binance.us/api (لأمريكا)
    # خيار 2: https://api1.binance.com/api
    # خيار 3: https://api2.binance.com/api
    client.API_URL = 'https://api3.binance.com/api' 

    # محاولة جلب الحالة للتأكد من الاتصال
    status = client.get_system_status()
    if status['status'] == 0:
        st.success("✅ تم كسر الحصار! البوت متصل الآن.")

    # --- عرض الأرصدة (البحث الشامل) ---
    spot = client.get_account()['balances']
    funding = client.get_funding_asset()
    
    for a in spot:
        if float(a['free']) > 0.00001:
            st.write(f"🟢 **{a['asset']} (Spot)**: {a['free']}")
            
    for a in funding:
        if float(a['free']) > 0.00001:
            st.write(f"🔵 **{a['asset']} (Funding)**: {a['free']}")

    # --- لوحة التداول ---
    st.divider()
    symbol = st.text_input("الزوج", "PEPEUSDT").upper()
    qty = st.number_input("الكمية", min_value=0.0)
    
    if st.button("شراء الآن 🚀"):
        order = client.order_market_buy(symbol=symbol, quantity=qty)
        st.success("تم الشراء!")

except Exception as e:
    st.error(f"❌ بينانس لا تزال ترفض السيرفر: {e}")
    st.info("يا جمال، الحل النهائي هو تشغيل هذا الكود على (كمبيوترك الشخصي) وليس على Streamlit Cloud، لأن بينانس تحظر السيرفرات السحابية.")
