import streamlit as st
from binance.client import Client

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="Binance Guardian", page_icon="💰")
st.title("💰 محفظتي الرقمية الحقيقية")

try:
    # 2. جلب مفاتيح الـ API من الخزنة السرية (Secrets)
    api_key = st.secrets["BINANCE_API_KEY"]
    api_secret = st.secrets["BINANCE_SECRET_KEY"]
    
    # 3. الربط مع بينانس وتجاوز قيود الموقع الجغرافي
    # نستخدم السيرفر العالمي api.binance.me لضمان استقرار الاتصال
    client = Client(api_key, api_secret)
    client.API_URL = 'https://api.binance.me/api'

    # 4. سحب بيانات الأرصدة من المحفظة
    account = client.get_account()
    balances = account['balances']

    st.write("### 📊 الأرصدة المتوفرة حالياً:")
    
    found = False
    for b in balances:
        free_amount = float(b['free'])
        
        # إظهار العملات التي تملك فيها رصيد فقط (أكبر من الصفر)
        if free_amount > 0.00000001:
            asset = b['asset']
            
            # 5. جلب سعر العملة بالدولار (USDT) لإظهار القيمة الحقيقية
            try:
                if asset != "USDT":
                    ticker = client.get_symbol_ticker(symbol=f"{asset}USDT")
                    usd_val = float(ticker['price']) * free_amount
                    st.success(f"**{asset}**: {free_amount:,.8f} (≈ ${usd_val:,.2f})")
                else:
                    # إذا كانت العملة هي دولار أصلاً
                    st.success(f"**{asset}**: ${free_amount:,.2f}")
            except:
                # إذا كانت عملة جديدة جداً ولا يوجد لها سعر مباشر مقابل USDT
                st.success(f"**{asset}**: {free_amount:,.8f}")
                
            found = True
            
    if not found:
        st.info("✅ تم الاتصال بنجاح، ولكن يبدو أن محفظة السبوت (Spot) فارغة حالياً.")

except Exception as e:
    # رسالة ذكية تخبرك بالضبط أين المشكلة (مفاتيح غلط أو إنترنت)
    st.error(f"⚠️ تنبيه من المستشارة: {e}")
    st.info("تأكد من أنك فعلت خيار 'Enable Reading' في إعدادات الـ API بموقع بينانس.")
