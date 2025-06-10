import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("글로벌 시총 상위 10개 기업 주가 변화 시각화")
st.markdown("최근 3년간 글로벌 시가총액 상위 기업들의 주가 변화를 시각화합니다.")

TICKERS = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet (Google) A",
    "AMZN": "Amazon",
    "META": "Meta Platforms",
    "TSLA": "Tesla",
    "BRK-A": "Berkshire Hathaway A",
    "LLY": "Eli Lilly",
    "AVGO": "Broadcom"
}

@st.cache_data
def get_stock_data(tickers_dict, years=3):
    """
    지정된 티커 목록에 대해 지난 N년 동안의 주가 데이터를 가져옵니다.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years * 365)

    all_data = pd.DataFrame()
    for ticker, name in tickers_dict.items():
        try:
            data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False, progress=False) # progress=False 추가
            if not data.empty:
                data['Ticker'] = ticker
                data['Company'] = name
                if 'Adj Close' in data.columns:
                    # NaN 값 제거 또는 처리 (정규화 전 중요)
                    data = data.dropna(subset=['Adj Close']) # NaN 값 제거
                    if not data.empty: # NaN 제거 후 데이터가 비어있지 않은지 다시 확인
                        all_data = pd.concat([all_data, data[['Adj Close', 'Ticker', 'Company']]])
                    else:
                        st.warning(f"데이터를 가져왔으나 'Adj Close' 컬럼에 유효한 값이 없습니다: {name} ({ticker})")
                elif 'Close' in data.columns:
                    data = data.rename(columns={'Close': 'Adj Close'})
                    data = data.dropna(subset=['Adj Close']) # NaN 값 제거
                    if not data.empty: # NaN 제거 후 데이터가 비어있지 않은지 다시 확인
                        all_data = pd.concat([all_data, data[['Adj Close', 'Ticker', 'Company']]])
                    else:
                        st.warning(f"데이터를 가져왔으나 'Close' 컬럼에 유효한 값이 없습니다: {name} ({ticker})")
                else:
                    st.warning(f"데이터를 가져왔으나 'Adj Close' 또는 'Close' 컬럼이 없습니다: {name} ({ticker})")
            else:
                st.warning(f"데이터를 가져오지 못했습니다 (빈 데이터): {name} ({ticker})")
        except Exception as e:
            st.warning(f"Error downloading data for {name} ({ticker}): {e}")
    return all_data

# 주가 데이터 가져오기
df_stocks = get_stock_data(TICKERS, years=3)

if not df_stocks.empty:
    st.subheader("주가 추이")

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
        # 선택된 티커의 데이터만 필터링
        filtered_df = df_stocks[df_stocks['Ticker'].isin(selected_tickers)].copy()

        normalize = st.checkbox("주가 정규화 (시작점 100)", value=False)

        if normalize:
            normalized_data = pd.DataFrame()
            for ticker in selected_tickers:
                ticker_df = filtered_df[filtered_df['Ticker'] == ticker].copy()
                
                # --- 주가 정규화 로직 개선 시작 ---
                if not ticker_df.empty and 'Adj Close' in ticker_df.columns:
                    initial_price = ticker_df['Adj Close'].iloc[0]
                    if initial_price != 0 and pd.notnull(initial_price): # initial_price가 0이 아니고 NaN이 아닌지 확인
                        ticker_df['Adj Close Normalized'] = (ticker_df['Adj Close'] / initial_price) * 100
                        normalized_data = pd.concat([normalized_data, ticker_df])
                    else:
                        st.warning(f"'{TICKERS[ticker]}' ({ticker})의 시작 주가가 0이거나 유효하지 않아 정규화할 수 없습니다.")
                else:
                    st.warning(f"'{TICKERS[ticker]}' ({ticker})의 주가 데이터를 찾을 수 없거나 'Adj Close' 컬럼이 없어 정규화할 수 없습니다.")
                # --- 주가 정규화 로직 개선 끝 ---

            if not normalized_data.empty: # 정규화된 데이터가 하나라도 있는지 확인
                filtered_df = normalized_data # 정규화된 데이터로 교체
                plot_column = 'Adj Close Normalized'
                y_axis_title = '정규화된 주가 (시작점 100)'
            else:
                st.warning("선택된 기업 중 정규화할 수 있는 데이터가 없습니다. 원본 주가를 표시합니다.")
                plot_column = 'Adj Close'
                y_axis_title = '주가 (USD)'
        else:
            plot_column = 'Adj Close'
            y_axis_title = '주가 (USD)'

        fig = go.Figure()

        for ticker in selected_tickers:
            company_df = filtered_df[filtered_df['Ticker'] == ticker]
            
            # 시각화할 컬럼이 존재하는지 확인
            if plot_column not in company_df.columns or company_df[plot_column].empty:
                st.warning(f"'{TICKERS[ticker]}' ({ticker})에 대한 시각화 데이터가 없습니다.")
                continue

            fig.add_trace(go.Scatter(
                x=company_df.index,
                y=company_df[plot_column],
                mode='lines',
                name=f"{TICKERS[ticker]} ({ticker})"
            ))

        if fig.data: # 그래프에 최소한 하나의 트레이스가 있는지 확인
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
            st.warning("선택된 기업 중 시각화할 수 있는 유효한 데이터가 없습니다.")

    else:
        st.info("시각화할 기업을 하나 이상 선택해주세요.")

else:
    st.warning("주가 데이터를 가져오는데 실패했습니다. 네트워크 연결을 확인하거나 티커 목록을 다시 확인해주세요.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, yfinance, and Plotly.")
