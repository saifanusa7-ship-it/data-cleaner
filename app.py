import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Data Cleaner", layout="centered")
st.title("🧹 AI Data Cleaner")
st.markdown("Upload CSV, get clean file!")

uploaded = st.file_uploader("📤 Choose CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.subheader("📄 Original Data")
    st.dataframe(df)
    
    if st.button("✨ Clean Data"):
        df_clean = df.drop_duplicates()
        
        if 'Name' in df_clean.columns:
            df_clean['Name'] = df_clean['Name'].str.title()
        
        if 'Phone' in df_clean.columns:
            df_clean['Phone'] = df_clean['Phone'].apply(
                lambda x: f"+91-{str(x)[:5]}-{str(x)[5:]}" if len(str(x)) == 10 else str(x)
            )
        
        if 'City' in df_clean.columns:
            df_clean['City'] = df_clean['City'].fillna('Unknown')
        
        df_clean['Data_Quality'] = df_clean.apply(
            lambda row: 'Clean' if row.notna().all() else 'Needs Review', axis=1
        )
        
        st.success("✅ Done!")
        st.subheader("✨ Cleaned Data")
        st.dataframe(df_clean)
        
        csv = df_clean.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download", csv, "cleaned.csv", "text/csv")
