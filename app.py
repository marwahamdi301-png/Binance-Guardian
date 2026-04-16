import streamlit as st
from binance.client import Client
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Jamal Portfolio", page_icon="💰", layout="wide")

st.title("📊 منصة جمال لإدارة المحفظة")
st.markdown("---")

# مفاتيحك التي نجحت في الاختبار
API_KEY = 'zNQJ1G5kGqnwSKDZin6he1GN8lW2NG6yZE0WpHsplK2SQkr01ixcE20EVMZBAWxM'
API_SECRET = 'gOH05NN1Pxfspq1nGIoviVPE6SjGX7uRVVv5mq4XXANcv1AKH6pnA4EnmcdNn68U'

try:
    client = Client(API_KEY, API_SECRET)
    
    # جلب البيانات
    acc = client.get_account()
    spot_data = [{"Asset": b['asset'], "Free": float(b['free'])} for b in acc['balances'] if float(b['free']) > 0]
    
    # عرض الأرصدة في كروت أنيقة
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 أرصدة التداول (Spot)")
        if spot_data:
            df_spot = pd.DataFrame(spot_data)
            st.dataframe(df_spot, use_container_width=True)
        else:
            st.write("لا توجد أرصدة حالياً")

    with col2:
        st.subheader("📥 أرصدة التمويل (Funding)")
        funding = client.get_user_asset()
        funding_data = [{"Asset": f['asset'], "Free": float(f['free'])} for f in funding if float(f['free']) > 0]
        if funding_data:
            df_funding = pd.DataFrame(funding_data)
            st.table(df_funding)
        else:
            st.write("المحفظة فارغة")

    st.success("✅ تم تحديث البيانات مباشرة من بينانس")

except Exception as e:
    st.error(f"حدث خطأ في الاتصال: {e}")
