import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시총 상위 10개 기업 주가 변화 시각화")
st.markdown("최근 3년간 글로벌 시가총액 상위 기업들의 주가 변화를 시각화합니다.")

# 현재 시점에서 글로벌 시가총액 상위 기업 (변동될 수 있음)
# 실제 시총 상위 기업 목록은 수시로 변동되므로, 이 목록은 예시입니다.
# 더 정확한 최신 목록을 원하시면 별도의 API나 웹 스크래핑이 필요합니다.
TICKERS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet (Google) A",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "TSLA": "Tesla",
    "BRK-A": "Berkshire Hathaway A", # A주 (매우 비쌈)
    "LLY": "Eli Lilly",
    "AVGO": "Broadcom"
}

@st.cache_data
def get_stock_data(tickers_dict, years=3):
    """
    지정된 티커 목록에 대해 지난 N년 동안의 주가 데이터를 가져옵니다.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365) # 대략 3년 전

    all_data = pd.DataFrame()
    for ticker, name in tickers_dict.items():
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if not data.empty:
                data['Ticker'] = ticker
                data['Company'] = name
                all_data = pd.concat([all_data, data[['Adj Close', 'Ticker', 'Company']]])
        except Exception as e:
            st.warning(f"Error downloading data for {name} ({ticker}): {e}")
    return all_data

# 주가 데이터 가져오기
df_stocks = get_stock_data(TICKERS, years=3)

if not df_stocks.empty:
    st.subheader("주가 추이")

    # 모든 종목을 선택할지 여부
    select_all = st.checkbox("모든 기업 선택", value=True)

    if select_all:
        selected_tickers = list(TICKERS.keys())
    else:
        selected_tickers = st.multiselect(
            "시각화할 기업을 선택하세요:",
            options=list(TICKERS.keys()),
            format_func=lambda x: TICKERS[x],
            default=list(TICKERS.keys())
        )

    if selected_tickers:
        filtered_df = df_stocks[df_stocks['Ticker'].isin(selected_tickers)].copy()

        # 주가 데이터 정규화 (선택 사항: 주가 시작점을 100으로 설정)
        normalize = st.checkbox("주가 정규화 (시작점 100)", value=False)

        if normalize:
            # 각 종목별로 첫 번째 'Adj Close' 값을 찾아서 나누기
            normalized_data = pd.DataFrame()
            for ticker in selected_tickers:
                ticker_df = filtered_df[filtered_df['Ticker'] == ticker].copy()
                if not ticker_df.empty:
                    initial_price = ticker_df['Adj Close'].iloc[0]
                    if initial_price != 0:
                        ticker_df['Adj Close Normalized'] = (ticker_df['Adj Close'] / initial_price) * 100
                    else:
                        ticker_df['Adj Close Normalized'] = 0 # 0으로 나누는 경우 방지
                    normalized_data = pd.concat([normalized_data, ticker_df])
            plot_column = 'Adj Close Normalized'
            y_axis_title = '정규화된 주가 (시작점 100)'
        else:
            plot_column = 'Adj Close'
            y_axis_title = '주가 (USD)'

        fig = go.Figure()

        for ticker in selected_tickers:
            company_df = filtered_df[filtered_df['Ticker'] == ticker]
            if normalize:
                 # 정규화된 데이터가 없으면 건너뛰기
                if 'Adj Close Normalized' not in company_df.columns or company_df['Adj Close Normalized'].empty:
                    continue
            
            fig.add_trace(go.Scatter(
                x=company_df.index,
                y=company_df[plot_column],
                mode='lines',
                name=f"{TICKERS[ticker]} ({ticker})"
            ))

        fig.update_layout(
            title="글로벌 시총 상위 기업 주가 추이",
            xaxis_title="날짜",
            yaxis_title=y_axis_title,
            hovermode="x unified",
            legend_title="기업",
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("시각화할 기업을 하나 이상 선택해주세요.")

else:
    st.warning("주가 데이터를 가져오는데 실패했습니다. 네트워크 연결을 확인하거나 티커 목록을 다시 확인해주세요.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, yfinance, and Plotly.")
