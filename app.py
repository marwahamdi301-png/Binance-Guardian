import streamlit as st
from binance.client import Client

st.set_page_config(page_title="Binance Guardian", page_icon="💰")
st.title("💰 حسابك الحقيقي")

try:
    # جلب المفاتيح من الأسرار
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
      # إنشاء الاتصال مع تجاوز الحظر الجغرافي
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'


    # جلب معلومات الحساب والأرصدة
    account = client.get_account()
    balances = account['balances']

    st.write("### 📊 قائمة عملاتك وأرصدتها:")
    
    found = False
    for b in balances:
        free_amount = float(b['free'])
        # إظهار العملات التي تملك فيها رصيد فقط
        if free_amount > 0.00000001:
            st.success(f"**{b['asset']}**: {free_amount:,.8f}")
            found = True
            
    if not found:
        st.warning("لا توجد أرصدة حالية في المحفظة.")

except Exception as e:
    st.error(f"⚠️ خطأ تقني من بينانس: {e}")
    st.info("انسخ النص الذي ظهر بالأعلى وأرسله لي فوراً.")

