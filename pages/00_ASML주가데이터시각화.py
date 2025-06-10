import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

def main():
    st.set_page_config(page_title="ASML 주가 변화", layout="wide")
    st.title("ASML (ASML) 최근 20년 주가 변화")

    ticker = "ASML"
    end_date = datetime.now()
    start_date = end_date - timedelta(days=20 * 365) # 20년 전 데이터

    @st.cache_data
    def get_stock_data(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        return data

    st.write(f"**티커:** {ticker}")
    st.write(f"**데이터 기간:** {start_date.strftime('%Y-%m-%d')} 부터 {end_date.strftime('%Y-%m-%d')} 까지")

    try:
        df = get_stock_data(ticker, start_date, end_date)

        if not df.empty:
            fig = go.Figure(data=[go.Candlestick(x=df.index,
                                                    open=df['Open'],
                                                    high=df['High'],
                                                    low=df['Low'],
                                                    close=df['Close'])])

            fig.update_layout(
                title=f'{ticker} 주가 (최근 20년)',
                xaxis_title='날짜',
                yaxis_title='주가 (USD)',
                xaxis_rangeslider_visible=False,
                height=600 # 그래프 높이 조정
            )
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("주가 데이터")
            st.dataframe(df.tail()) # 최근 5개 데이터 보여주기
        else:
            st.warning(f"{ticker} 에 대한 주가 데이터를 찾을 수 없습니다. 티커를 확인해주세요.")
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
