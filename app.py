import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# 1. Load the hidden API Key
load_dotenv()
API_KEY = os.getenv("FINNHUB_API_KEY")
if not API_KEY:
    st.error("The App can't find your .env file. Make sure it's in the same folder as app.py!")
else:
    st.success(f"✅ API Key detected! (Starts with: {API_KEY[:4]}...)")

# 2. App Styling
st.set_page_config(page_title="FinNews Pro", layout="wide")
st.title("📈 Real-Time Financial Intelligence")
st.markdown("---")

# 3. User Input (The Sidebar)
ticker = st.sidebar.text_input("Enter Ticker (e.g. AAPL, TSLA, BTC):", "AAPL").upper()

# 4. Fetch the Data
if st.sidebar.button("Fetch News"):
    # 1. Calculate the dynamic dates
    # 'today' becomes the current date (e.g., 2026-03-10) 
    today = datetime.now().strftime('%Y-%m-%d')
    # 'one_week_ago' looks back 7 days from now
    one_week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    url = f'https://finnhub.io/api/v1/company-news?symbol={ticker}&from={one_week_ago}&to={today}&token={API_KEY}'
    
    with st.spinner('Accessing market feeds...'):
        response = requests.get(url)
        
        if response.status_code == 200:
            news = response.json()
            
            if not news:
                st.warning("No recent news found for this ticker.")
            
            for article in news[:5]: # Show top 5
                col1, col2 = st.columns([1, 4])
                with col1:
                    if article['image']:
                        st.image(article['image'], use_container_width=True)
                with col2:
                    st.subheader(article['headline'])
                    st.caption(f"Source: {article['source']} | {article['category'].upper()}")
                    st.write(article['summary'])
                    st.link_button("Read Full Article", article['url'])
                st.markdown("---")
        else:
            st.error("Failed to connect to Finnhub. Check your API key.")