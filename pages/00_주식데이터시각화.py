import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Streamlit 페이지 설정
st.set_page_config(layout="wide")

# 앱 제목 및 설명
st.title("글로벌 시총 상위 10개 기업 주가 변화 시각화")
st.markdown("최근 3년간 글로벌 시가총액 상위 기업들의 주가 변화를 시각화합니다.")

# 현재 시점에서 글로벌 시가총액 상위 기업 티커 및 이름 (변동될 수 있음)
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
    # 365일 * 년수 로 정확한 날짜를 계산하지만, 윤년 등을 고려하여 약간의 오차가 있을 수 있습니다.
    start_date = end_date - timedelta(days=years * 365) 

    all_data = pd.DataFrame()
    for ticker, name in tickers_dict.items():
        try:
            # yfinance 0.1.63 버전에서는 auto_adjust=True 일 때 'Close' 컬럼에 조정된 종가가 포함됩니다.
            # progress=False를 추가하여 다운로드 진행 바가 터미널에 표시되지 않도록 합니다.
            data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True, progress=False)
            
            if not data.empty:
                data['Ticker'] = ticker
                data['Company'] = name
                
                # 'Close' 컬럼에 이미 조정된 가격이 있으므로, 이 컬럼을 사용합니다.
                # 이후의 정규화 및 시각화 로직에서 'Adj Close'라는 컬럼 이름을 사용하므로,
                # 'Close' 컬럼의 이름을 'Adj Close'로 변경하여 통일성을 유지합니다.
                if 'Close' in data.columns:
                    # NaN 값 제거: 주가 데이터에 누락된 값이 있을 수 있으므로 제거합니다.
                    data = data.dropna(subset=['Close']) 
                    
                    if not data.empty: # NaN 제거 후 데이터가 비어있지 않은지 다시 확인
                        data = data.rename(columns={'Close': 'Adj Close'}) # 컬럼 이름 변경
                        all_data = pd.concat([all_data, data[['Adj Close', 'Ticker', 'Company']]])
                    else:
                        st.warning(f"데이터를 가져왔으나 'Close' 컬럼에 유효한 값이 없습니다: **{name} ({ticker})**")
                else:
                    st.warning(f"데이터를 가져왔으나 'Close' 컬럼이 없습니다: **{name} ({ticker})**")
            else:
                st.warning(f"데이터를 가져오지 못했습니다 (빈 데이터): **{name} ({ticker})**")
        except Exception as e:
            st.warning(f"데이터 다운로드 중 오류 발생: **{name} ({ticker})**: {e}")
    return all_data

# 주가 데이터 가져오기 (캐싱 적용)
df_stocks = get_stock_data(TICKERS, years=3)

# 데이터가 성공적으로 로드되었는지 확인
if not df_stocks.empty:
    st.subheader("주가 추이")

    # 모든 종목을 선택할지 여부 체크박스
    select_all = st.checkbox("모든 기업 선택", value=True)

    if select_all:
        selected_tickers = list(TICKERS.keys())
    else:
        selected_tickers = st.multiselect(
            "시각화할 기업을 선택하세요:",
            options=list(TICKERS.keys()),
            format_func=lambda x: TICKERS[x], # 티커 대신 회사 이름 표시
            default=list(TICKERS.keys()) # 기본적으로 모든 기업 선택
        )

    # 선택된 기업이 있을 경우에만 시각화 진행
    if selected_tickers:
        # 선택된 티커의 데이터만 필터링
        filtered_df = df_stocks[df_stocks['Ticker'].isin(selected_tickers)].copy()

        # 주가 정규화 옵션 체크박스
        normalize = st.checkbox("주가 정규화 (시작점 100)", value=False)

        plot_column = 'Adj Close' # 기본 시각화 컬럼
        y_axis_title = '주가 (USD)' # 기본 Y축 제목

        if normalize:
            normalized_data = pd.DataFrame()
            for ticker in selected_tickers:
                ticker_df = filtered_df[filtered_df['Ticker'] == ticker].copy()
                
                # 데이터 유효성 검사: DataFrame이 비어있지 않고 'Adj Close' 컬럼이 존재하는지 확인
                if not ticker_df.empty and 'Adj Close' in ticker_df.columns:
                    # 첫 번째 주가 값을 가져옴 (정규화 기준)
                    initial_price = ticker_df['Adj Close'].iloc[0]
                    
                    # 0으로 나누는 오류 및 NaN 값 방지
                    if initial_price != 0 and pd.notnull(initial_price): 
                        ticker_df['Adj Close Normalized'] = (ticker_df['Adj Close'] / initial_price) * 100
                        normalized_data = pd.concat([normalized_data, ticker_df])
                    else:
                        st.warning(f"**{TICKERS[ticker]} ({ticker})**의 시작 주가가 0이거나 유효하지 않아 정규화할 수 없습니다.")
                else:
                    st.warning(f"**{TICKERS[ticker]} ({ticker})**의 주가 데이터를 찾을 수 없거나 'Adj Close' 컬럼이 없어 정규화할 수 없습니다.")
            
            # 정규화된 데이터가 하나라도 있다면 사용
            if not normalized_data.empty: 
                filtered_df = normalized_data # 정규화된 데이터로 원본 데이터프레임 교체
                plot_column = 'Adj Close Normalized'
                y_axis_title = '정규화된 주가 (시작점 100)'
            else:
                st.info("선택된 기업 중 정규화할 수 있는 유효한 데이터가 없습니다. 원본 주가를 표시합니다.")
                # 정규화 실패 시 기본값으로 돌아가므로, 추가 처리 필요 없음
        
        # Plotly 그래프 생성
        fig = go.Figure()

        for ticker in selected_tickers:
            company_df = filtered_df[filtered_df['Ticker'] == ticker]
            
            # 시각화할 컬럼이 존재하는지, 그리고 데이터가 비어있지 않은지 확인
            if plot_column in company_df.columns and not company_df[plot_column].empty:
                fig.add_trace(go.Scatter(
                    x=company_df.index, # 날짜를 X축으로 사용
                    y=company_df[plot_column], # 선택된 주가 컬럼을 Y축으로 사용
                    mode='lines', # 선 그래프
                    name=f"{TICKERS[ticker]} ({ticker})" # 범례에 회사 이름 및 티커 표시
                ))
            else:
                st.warning(f"**{TICKERS[ticker]} ({ticker})**에 대한 시각화 데이터가 부족합니다.")

        # 그래프에 최소한 하나의 트레이스(선)가 추가되었는지 확인
        if fig.data: 
            fig.update_layout(
                title="글로벌 시총 상위 기업 주가 추이",
                xaxis_title="날짜",
                yaxis_title=y_axis_title,
                hovermode="x unified", # 마우스 오버 시 모든 트레이스의 정보 표시
                legend_title="기업",
                height=600 # 그래프 높이 설정
            )
            st.plotly_chart(fig, use_container_width=True) # Streamlit에 그래프 표시
        else:
            st.warning("선택된 기업 중 시각화할 수 있는 유효한 데이터가 없습니다.")

    else:
        st.info("시각화할 기업을 하나 이상 선택해주세요.")

else:
    st.error("주가 데이터를 가져오는데 실패했습니다. 네트워크 연결을 확인하거나 티커 목록을 다시 확인해주세요.")

st.markdown("---")
st.markdown("Made with ❤️ using Streamlit, yfinance, and Plotly.")
