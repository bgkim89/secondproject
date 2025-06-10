import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# gwpy는 LIGO/Virgo 데이터를 다루는 데 매우 유용합니다.
# pip install gwpy h5py matplotlib
try:
    from gwpy.timeseries import TimeSeries
    from gwpy.segments import Segment
    from gwpy.plot import Plot
except ImportError:
    st.error("gwpy 라이브러리가 설치되어 있지 않습니다. `pip install gwpy h5py matplotlib`을 실행해주세요.")
    st.stop()


st.title("LIGO 중력파 데이터 시각화")
st.write("yfinance는 금융 데이터 라이브러리이므로 LIGO 중력파 데이터를 가져올 수 없습니다.")
st.markdown("""
**LIGO 중력파 데이터를 시각화하는 방법:**
1.  **데이터 획득:** GWOSC (Gravitational-Wave Open Science Center)에서 중력파 데이터 파일을 다운로드하거나, `gwpy` 라이브러리를 사용하여 프로그램적으로 데이터를 가져옵니다.
2.  **데이터 처리:** `gwpy` 또는 `scipy`를 사용하여 노이즈 제거, 필터링, 스펙트로그램 생성 등을 수행합니다.
3.  **시각화:** `matplotlib` 또는 `plotly`를 사용하여 그래프를 그립니다.
""")

st.header("예시: GWOSC에서 데이터 가져오기 (실제로는 시간이 걸릴 수 있음)")

# GWOSC에서 특정 이벤트의 데이터를 가져오는 예시
# 실제 중력파 이벤트 ID와 탐지기, 시간 범위를 지정해야 합니다.
# 예시: GW150914 (최초 중력파 탐지)
event_name = st.selectbox("중력파 이벤트 선택", ["GW150914", "GW170817", "GW190412"])

if event_name == "GW150914":
    # GW150914의 시간 범위를 설정합니다 (중앙 시점).
    # GWOSC에서 정확한 이벤트를 검색하여 시간 범위를 확인해야 합니다.
    t_start = 1126259446 # UTC 초
    duration = 32 # 데이터 가져올 기간 (초)
    segment = Segment(t_start - duration/2, t_start + duration/2) # 이벤트 전후 16초씩

    detector = st.selectbox("탐지기 선택", ["H1", "L1", "V1"])

    if st.button(f"{event_name} 데이터 로드 및 시각화 ({detector})"):
        st.info(f"{detector} 데이터 로드 중... 잠시 기다려주세요.")
        try:
            # GWOSC에서 데이터 스트레인(strain)을 가져옵니다.
            # 이 과정은 네트워크 상태에 따라 시간이 걸릴 수 있습니다.
            strain = TimeSeries.fetch_open_data(detector, segment.active[0].start, segment.active[0].duration)

            st.success(f"{detector} 데이터 로드 완료!")

            # 1. 시간 영역 파형 시각화
            st.subheader(f"{detector} - 시간 영역 파형")
            fig_waveform = strain.plot(figsize=(10, 4), color='teal', title=f"{detector} Strain Data for {event_name}")
            fig_waveform.set_xlabel("Time (s)")
            fig_waveform.set_ylabel("Strain")
            st.pyplot(fig_waveform)

            # 2. 파워 스펙트럼 밀도 (PSD) 시각화
            st.subheader(f"{detector} - 파워 스펙트럼 밀도 (PSD)")
            # strain_clean = strain.filter(f_low=30, f_high=500) # 노이즈 필터링 (선택 사항)
            psd = strain.psd(fftlength=4, overlap=2, window='hann')
            fig_psd = psd.plot(figsize=(10, 4), color='purple', title=f"{detector} Power Spectral Density for {event_name}")
            fig_psd.set_xlabel("Frequency (Hz)")
            fig_psd.set_ylabel("ASD (Hz$^{-1/2}$)")
            fig_psd.set_xscale("log")
            fig_psd.set_yscale("log")
            st.pyplot(fig_psd)

            # 3. 스펙트로그램 시각화 (시간-주파수 플롯)
            st.subheader(f"{detector} - 스펙트로그램")
            # 스펙트로그램을 계산하고 플롯합니다.
            specgram = strain.spectrogram(fftlength=1, overlap=0.5, window='hann', frequency_resolution=1)
            # gwpy의 plot 메소드를 사용하여 스펙트로그램을 그립니다.
            plot_spec = specgram.plot(figsize=(10, 6), cmap='viridis', vmin=1e-24, vmax=1e-20)
            plot_spec.colorbar(label='Strain (Hz$^{-1/2}$)')
            plot_spec.axes[0].set_yscale('log')
            plot_spec.axes[0].set_ylim(20, 1024) # 관심 있는 주파수 범위
            plot_spec.axes[0].set_title(f"{detector} Spectrogram for {event_name}")
            st.pyplot(plot_spec)


        except Exception as e:
            st.error(f"데이터를 로드하거나 처리하는 중 오류가 발생했습니다: {e}")
            st.info("GWOSC에서 데이터를 가져오는 데 시간이 걸리거나 네트워크 문제일 수 있습니다.")
            st.info("특정 이벤트의 정확한 시간 범위는 GWOSC 웹사이트에서 확인해주세요.")

elif event_name in ["GW170817", "GW190412"]:
    st.warning("이벤트에 대한 코드 로직은 아직 구현되지 않았습니다. GW150914를 선택하여 예시를 확인하세요.")


st.subheader("직접 데이터 파일 업로드 (선택 사항)")
uploaded_file = st.file_uploader("LIGO 중력파 HDF5/GWF 파일 업로드", type=["hdf5", "hdf", "gwf"])

if uploaded_file is not None:
    st.info("업로드된 파일을 처리 중... 잠시 기다려주세요.")
    try:
        # gwpy의 TimeSeries.read를 사용하여 파일을 읽습니다.
        # Streamlit Cloud에서 파일을 직접 쓰는 것은 제한적일 수 있으므로,
        # io.BytesIO를 사용하여 메모리에서 처리하는 것이 좋습니다.
        import io
        byte_data = uploaded_file.getvalue()
        # gwpy는 파일 경로 또는 파일 객체를 직접 받을 수 있습니다.
        # 여기서는 임시 파일을 사용하여 읽는 방법을 보여줍니다.
        # 실제 Streamlit Cloud에서는 더 robust한 파일 처리 방법이 필요할 수 있습니다.
        # 예를 들어, named_temporary_file을 사용하는 방법도 있습니다.

        with open("uploaded_ligo_data.gwf", "wb") as f:
            f.write(byte_data)

        # 파일 유형에 따라 적절한 읽기 방법 선택
        if uploaded_file.name.endswith(('.hdf5', '.hdf')):
            strain_uploaded = TimeSeries.read("uploaded_ligo_data.gwf", format='hdf5') # 또는 'hdf'
        elif uploaded_file.name.endswith('.gwf'):
            strain_uploaded = TimeSeries.read("uploaded_ligo_data.gwf", format='gwf')
        else:
            st.error("지원되지 않는 파일 형식입니다. .hdf5, .hdf, .gwf 파일만 지원합니다.")
            st.stop()

        st.success(f"파일 '{uploaded_file.name}'이 성공적으로 로드되었습니다.")

        # 업로드된 데이터 시각화 (위의 GWOSC 데이터와 동일한 방식)
        st.subheader(f"업로드된 데이터 - 시간 영역 파형")
        fig_uploaded_waveform = strain_uploaded.plot(figsize=(10, 4), color='darkblue', title=f"Uploaded Data Strain")
        fig_uploaded_waveform.set_xlabel("Time (s)")
        fig_uploaded_waveform.set_ylabel("Strain")
        st.pyplot(fig_uploaded_waveform)

        st.subheader(f"업로드된 데이터 - 파워 스펙트럼 밀도 (PSD)")
        psd_uploaded = strain_uploaded.psd(fftlength=4, overlap=2, window='hann')
        fig_uploaded_psd = psd_uploaded.plot(figsize=(10, 4), color='darkred', title=f"Uploaded Data Power Spectral Density")
        fig_uploaded_psd.set_xlabel("Frequency (Hz)")
        fig_uploaded_psd.set_ylabel("ASD (Hz$^{-1/2}$)")
        fig_uploaded_psd.set_xscale("log")
        fig_uploaded_psd.set_yscale("log")
        st.pyplot(fig_uploaded_psd)

        # 스펙트로그램 시각화 (선택 사항)
        st.subheader(f"업로드된 데이터 - 스펙트로그램")
        specgram_uploaded = strain_uploaded.spectrogram(fftlength=1, overlap=0.5, window='hann', frequency_resolution=1)
        plot_spec_uploaded = specgram_uploaded.plot(figsize=(10, 6), cmap='magma', vmin=1e-24, vmax=1e-20)
        plot_spec_uploaded.colorbar(label='Strain (Hz$^{-1/2}$)')
        plot_spec_uploaded.axes[0].set_yscale('log')
        plot_spec_uploaded.axes[0].set_ylim(20, 1024)
        plot_spec_uploaded.axes[0].set_title(f"Uploaded Data Spectrogram")
        st.pyplot(plot_spec_uploaded)


    except Exception as e:
        st.error(f"업로드된 파일을 읽거나 처리하는 중 오류가 발생했습니다: {e}")
        st.info("파일이 손상되었거나 지원되지 않는 형식이거나, 파일 구조가 예상과 다를 수 있습니다.")
