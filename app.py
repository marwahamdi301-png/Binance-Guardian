import streamlit as st
from binance.client import Client

# 1. إعدادات الصفحة لتظهر بشكل احترافي
st.set_page_config(page_title="Binance Guardian", page_icon="💰")
st.title("💰 محفظتك الرقمية الحقيقية")

try:
    # 2. جلب المفاتيح من الأسرار (Secrets) التي أعددتها
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    # 3. إنشاء الاتصال مع تجاوز الحظر الجغرافي (استخدام بوابة عالمية)
    # جربنا كل الروابط، وهذا الرابط .me هو الأكثر استقراراً للسيرفرات
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # 4. جلب معلومات الحساب
    account = client.get_account()
    balances = account['balances']

    st.write("### 📊 قائمة عملاتك وأرصدتها الحالية:")
    
    found = False
    for b in balances:
        free_amount = float(b['free'])
        # إظهار العملات التي تملك فيها رصيد فقط (أكبر من صفر)
        if free_amount > 0.00000001:
            asset_name = b['asset']
            st.success(f"**{asset_name}**: {free_amount:,.8f}")
            found = True
            
    if not found:
        st.warning("لا توجد أرصدة حالية في محفظة السبوت (Spot).")

except Exception as e:
    # عرض الخطأ الحقيقي إذا وجد (مثل مشكلة في الصلاحيات أو الحظر)
    st.error(f"⚠️ تنبيه من المستشارة: {e}")
    st.info("نصيحة: تأكد من تفعيل 'Enable Reading' في إعدادات API في بينانس.")
