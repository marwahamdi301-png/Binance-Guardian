import streamlit as st
from binance.client import Client

# إعداد واجهة البوت الاحترافية
st.set_page_config(page_title="Binance Mega Bot", page_icon="⚡", layout="wide")
st.title("⚡ بوت جمال الشامل: رصد + تداول آلي")

try:
    # 1. جلب المفاتيح
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    # 2. تجاوز الحظر الجغرافي (استخدام سيرفرات بديلة)
    client = Client(api_key, api_secret)
    # جربنا .me وسنضيف محاولة للاتصال المباشر عبر السيرفرات الاحتياطية
    client.API_URL = 'https://api1.binance.com/api' 

    # --- القسم الأول: الرصد الشامل لكل المحافظ ---
    st.header("🔍 كشف أرصدتك في كل مكان")
    
    # جلب أرصدة السبوت والتمويل والأرباح (Earn)
    spot = client.get_account()['balances']
    funding = client.get_funding_asset()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📍 محفظة التداول (Spot)")
        for a in spot:
            if float(a['free']) > 0:
                st.success(f"**{a['asset']}**: {a['free']}")
                
    with col2:
        st.subheader("💳 محفظة التمويل والأرباح")
        for a in funding:
            if float(a['free']) > 0:
                st.info(f"**{a['asset']}**: {a['free']}")

    # --- القسم الثاني: لوحة التداول الذكي ---
    st.divider()
    st.header("🤖 تنفيذ صفقات تداول آلي")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        symbol = st.text_input("زوج التداول", "PEPEUSDT").upper()
    with col_b:
        side = st.selectbox("نوع العملية", ["BUY", "SELL"])
    with col_c:
        qty = st.number_input("الكمية", min_value=0.0, step=0.00001)

    if st.button("تنفيذ الصفقة الآن 🚀"):
        try:
            if side == "BUY":
                order = client.order_market_buy(symbol=symbol, quantity=qty)
            else:
                order = client.order_market_sell(symbol=symbol, quantity=qty)
            st.balloons()
            st.success(f"تمت العملية بنجاح! رقم الطلب: {order['orderId']}")
        except Exception as e:
            st.error(f"فشل التداول: {e}")

except Exception as e:
    # حل مشكلة الموقع المقيد برمجياً
    st.error(f"❌ خطأ الاتصال: {e}")
    st.warning("بينانس ترفض الاتصال من سيرفر Streamlit. يرجى تفعيل VPN على جهازك وإعادة المحاولة أو تغيير API_URL في الكود.")
