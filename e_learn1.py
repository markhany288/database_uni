import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import urllib
import plotly.express as px
from ai_engine import ask_grok_sql # استدعاء الوظيفة الجديدة

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="AI Data Investigator", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .sql-box { background-color: #1c1f26; padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; }
    h1, h2, h3 { color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. ربط الداتابيز
@st.cache_resource
def get_engine():
    conn_str = 'DRIVER={SQL Server};SERVER=DESKTOP-PQ5UQRR;DATABASE=ELearningDB3;Trusted_Connection=yes;'
    quoted_conn_str = urllib.parse.quote_plus(conn_str)
    return create_engine(f"mssql+pyodbc:///?odbc_connect={quoted_conn_str}")

engine = get_engine()

st.title("📊 محقق البيانات الذكي (Text-to-SQL)")
st.write("اسأل أي سؤال عن الكورسات، الطلاب، أو الإيرادات والـ AI هيكتب الـ Query ويطلع لك الناتج.")

# 3. واجهة الشات والتحليل
query_input = st.text_input("✍️ اكتب سؤالك هنا (مثلاً: مين أعلى 5 طلاب جابوا درجات؟)")

if query_input:
    with st.spinner("🤖 الـ AI بيفكر في الـ SQL المناسبة..."):
        full_response = ask_grok_sql(query_input)
        
        # منطق فصل الكود عن الشرح
        if "---SQL---" in full_response:
            try:
                # استخراج الـ SQL
                sql_part = full_response.split("---SQL---")[1].split("---END_SQL---")[0].strip()
                # استخراج الشرح
                explanation = full_response.split("---END_SQL---")[1].strip()
                
                # أ. عرض كود الـ SQL للمستخدم
                st.markdown("### 🛠️ كود الـ SQL المُنشأ:")
                st.code(sql_part, language="sql")
                
                # ب. تنفيذ الكود وعرض النتائج
                df_result = pd.read_sql(sql_part, engine)
                
                st.markdown("### 📈 النتائج:")
                if not df_result.empty:
                    st.dataframe(df_result, use_container_width=True)
                    
                    # ج. عرض شرح الـ AI
                    st.success(f"**تفسير الـ AI:** {explanation}")
                    
                    # د. تحويل النتيجة لرسم بياني تلقائي لو أمكن
                    if len(df_result.columns) >= 2:
                        st.markdown("### 📊 تمثيل بياني سريع:")
                        fig = px.bar(df_result, x=df_result.columns[0], y=df_result.columns[1], template="plotly_dark")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("الـ Query اشتغلت صح بس مفيش داتا مطابقة للبحث ده.")
                    
            except Exception as e:
                st.error(f"حصلت مشكلة وأنا بنفذ الـ SQL: {e}")
                st.info("ده الكود اللي الـ AI كتبه وكان فيه غلطة، جرب تغير صيغة السؤال.")
        else:
            st.write(full_response)

st.divider()

st.caption("supervised by DR samar and eng mariam")