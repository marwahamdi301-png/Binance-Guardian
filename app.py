import streamlit as st
from binance.client import Client

# 1. إعدادات الصفحة (تأكد من كتابة st. قبل الأوامر)
st.set_page_config(page_title="Binance Guardian", page_icon="💰")
st.title("💰 حسابك الحقيقي")

try:
    # 2. جلب المفاتيح من الأسرار (Secrets)
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    # 3. إنشاء الاتصال وتغيير الرابط لتجاوز الحظر الجغرافي
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # 4. جلب معلومات الحساب والأرصدة
    account = client.get_account()
    balances = account['balances']

    st.write("### 📊 قائمة عملاتك وأرصدتها الحالية:")
    
    found = False
    for b in balances:
        free_amount = float(b['free'])
        # إظهار العملات التي تملك فيها رصيد فقط
        if free_amount > 0.00000001:
            st.success(f"**{b['asset']}**: {free_amount:,.8f}")
            found = True
            
    if not found:
        st.warning("لا توجد أرصدة حالية في محفظة السبوت (Spot).")

except Exception as e:
    # كشف الخطأ الحقيقي إذا وجد
    st.error(f"⚠️ حدث خطأ تقني: {e}")
    st.info("تأكد من صحة المفاتيح وصلاحيات الـ API في بينانس.")
