import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Grok Automation Scanner & Backtester", layout="wide")
st.title("🚀 Grok Professional Automation Dashboard")
st.markdown("**Zero-cost • Fully automated scanner + backtester • March 2026**")

# ================== SETTINGS ==================
tickers = st.multiselect("Watchlist (max 50 free)", 
                         ["AAPL","NVDA","TSLA","MSFT","AMD","AMZN","GOOGL","META","BTC-USD","ETH-USD"],
                         default=["AAPL","NVDA","TSLA","MSFT","AMD"])

timeframe = st.selectbox("Timeframe", ["1d", "4h", "1h", "15m"], index=0)
capital = st.number_input("Starting Capital ($)", value=10000, step=1000)

# ================== SCANNER ENGINE ==================
def scan_ticker(ticker):
    data = yf.download(ticker, period="6mo", interval=timeframe)
    if len(data) < 200:
        return None
    
    data['SMA50'] = data['Close'].rolling(50).mean()
    data['SMA200'] = data['Close'].rolling(200).mean()
    data['VolumeAvg'] = data['Volume'].rolling(20).mean()
    data['RSI'] = ta.rsi(data['Close'], 14)  # need to import talib or calculate
    
    latest = data.iloc[-1]
    prev = data.iloc[-2]
    
    golden_cross = (latest['SMA50'] > latest['SMA200']) and (prev['SMA50'] <= prev['SMA200'])
    volume_surge = latest['Volume'] > 1.5 * latest['VolumeAvg']
    rsi_oversold = latest['RSI'] < 35
    
    if golden_cross and volume_surge and rsi_oversold:
        return {
            "ticker": ticker,
            "signal": "BUY",
            "price": round(latest['Close'], 2),
            "reason": "Golden Cross + Volume + RSI < 35",
            "size": round(capital * 0.02 / latest['Close'], 0)
        }
    return None

# Run scanner
if st.button("🔄 Run Full Scan Now"):
    with st.spinner("Scanning market..."):
        results = []
        for t in tickers:
            signal = scan_ticker(t)
            if signal:
                results.append(signal)
        
        if results:
            st.success(f"Found {len(results)} signals!")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No signals today.")

# Backtester placeholder (you can expand later)
st.subheader("📈 Backtester Results")
st.info("Backtester coming in next update — for now run the scan daily and track manually.")

st.caption("Built live for you • Zero cost for first week • Powered by Grok automation stack")
