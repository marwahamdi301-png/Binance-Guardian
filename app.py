import streamlit as st
from binance.client import Client

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="Binance Guardian", page_icon="💰")
st.title("💰 محفظتي الرقمية الحقيقية")

try:
    # 2. جلب المفاتيح من الأسرار (Secrets)
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    # 3. إنشاء الاتصال وتجاوز الحظر الجغرافي
    # استخدمنا الرابط api.binance.me لضمان استقرار السيرفرات
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # 4. جلب معلومات الحساب
    account = client.get_account()
    balances = account['balances']

    st.write("### 📊 قائمة أرصدتي الحالية:")
    
    found = False
    for b in balances:
        free_amount = float(b['free'])
        # إظهار العملات التي تملك فيها رصيد حقيقي فقط
        if free_amount > 0.00000001:
            asset = b['asset']
            
            # محاولة جلب السعر بالدولار لإضافة قيمة حقيقية للتطبيق
            try:
                if asset != "USDT":
                    ticker = client.get_symbol_ticker(symbol=f"{asset}USDT")
                    usd_val = float(ticker['price']) * free_amount
                    st.success(f"**{asset}**: {free_amount:,.8f} (≈ ${usd_val:,.2f})")
                else:
                    st.success(f"**{asset}**: ${free_amount:,.2f}")
            except:
                # في حال كانت عملة نادرة لا تملك سعراً مباشراً بالدولار
                st.success(f"**{asset}**: {free_amount:,.8f}")
                
            found = True
            
    if not found:
        st.info("✅ تم الاتصال بنجاح، ولكن محفظة السبوت فارغة حالياً.")

except Exception as e:
    # رسالة ذكية تشرح لك أي عطل فني
    st.error(f"⚠️ تنبيه من المستشارة: {e}")
    st.info("تأكد من تفعيل صلاحيات (Enable Reading) في إعدادات API بينانس.")
