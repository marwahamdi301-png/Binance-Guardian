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
    # استخدمنا بوابة .me لضمان عمل التطبيق في كل مكان
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # 4. جلب بيانات المحفظة
    account = client.get_account()
    balances = account['balances']

    st.write("### 📊 الأرصدة المتوفرة حالياً:")
    
    found = False
    for b in balances:
        free_amount = float(b['free'])
        # إظهار العملات التي تملك فيها رصيد فقط
        if free_amount > 0.00000001:
            asset = b['asset']
            
            # 5. جلب السعر اللحظي بالدولار
            try:
                if asset != "USDT":
                    ticker = client.get_symbol_ticker(symbol=f"{asset}USDT")
                    usd_val = float(ticker['price']) * free_amount
                    st.success(f"**{asset}**: {free_amount:,.8f} (≈ ${usd_val:,.2f})")
                else:
                    st.success(f"**{asset}**: ${free_amount:,.2f}")
            except:
                # إذا كانت العملة جديدة أو غير مقترنة بـ USDT
                st.success(f"**{asset}**: {free_amount:,.8f}")
                
            found = True
            
    if not found:
        st.info("✅ تم الاتصال بنجاح، ولكن لا توجد عملات في محفظة السبوت.")

except Exception as e:
    st.error(f"⚠️ تنبيه من المستشارة: {e}")
    st.info("تأكد من تفعيل صلاحيات (Enable Reading) في إعدادات API بينانس.")
