
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.title("간단한 중력렌즈 효과 시뮬레이션")
st.write("이 앱은 점 질량 렌즈(point-mass lens)가 배경 광원(source)을 어떻게 왜곡하는지 간단히 시뮬레이션하여 시각화합니다.")

# 사용자 입력 파라미터
st.sidebar.header("시뮬레이션 파라미터")
einstein_radius_px = st.sidebar.slider(
    "아인슈타인 반경 (픽셀)",
    min_value=10,
    max_value=200,
    value=50,
    step=5,
    help="렌즈의 강도를 조절합니다. 값이 클수록 왜곡이 심해집니다."
)
source_pos_x = st.sidebar.slider(
    "광원 X 위치 (픽셀)",
    min_value=-150,
    max_value=150,
    value=50,
    step=5,
    help="렌즈 중심(0,0)에 대한 광원의 X축 상대 위치"
)
source_pos_y = st.sidebar.slider(
    "광원 Y 위치 (픽셀)",
    min_value=-150,
    max_value=150,
    value=0,
    step=5,
    help="렌즈 중심(0,0)에 대한 광원의 Y축 상대 위치"
)
source_size = st.sidebar.slider(
    "광원 크기",
    min_value=5,
    max_value=50,
    value=20,
    step=1,
    help="배경 광원의 크기 (픽셀)"
)
grid_size = st.sidebar.slider(
    "격자 크기",
    min_value=100,
    max_value=500,
    value=200,
    step=20,
    help="시뮬레이션 영역의 한 변의 픽셀 수"
)

# 배경 광원 이미지 생성
def create_source_image(size, cx, cy, source_radius):
    y, x = np.mgrid[-size/2:size/2, -size/2:size/2]
    dist_sq = (x - cx)**2 + (y - cy)**2
    # 가우시안 형태의 광원
    source = np.exp(-dist_sq / (2 * (source_radius/3)**2))
    return source

# 렌즈 방정식 구현 (점 질량 렌즈)
def lens_equation(x_lens, y_lens, alpha_x, alpha_y):
    # 실제 렌즈 위치 (image plane)에서 소스 위치 (source plane)로 역추적
    # x_source = x_lens - alpha_x
    # y_source = y_lens - alpha_y
    return x_lens - alpha_x, y_lens - alpha_y

# 왜곡장 계산 (Deflection field for point mass lens)
def deflection_angle(x, y, einstein_radius):
    r_sq = x**2 + y**2
    r_sq[r_sq == 0] = 1e-9 # 0으로 나누는 것을 방지
    alpha = (einstein_radius**2) / r_sq
    return alpha * x, alpha * y # x, y 방향 왜곡 각도

# 시뮬레이션 실행
if st.button("중력렌즈 시뮬레이션 실행"):
    with st.spinner("시뮬레이션 중..."):
        # 격자 생성 (렌즈 평면)
        half_grid = grid_size / 2
        y_grid, x_grid = np.mgrid[-half_grid:half_grid, -half_grid:half_grid]

        # 왜곡 각도 계산
        alpha_x, alpha_y = deflection_angle(x_grid, y_grid, einstein_radius_px)

        # 렌즈된 이미지 픽셀이 매핑될 소스 평면의 위치 계산 (역추적)
        # 이 (x_source, y_source)는 소스 이미지에서 픽셀 값을 가져올 좌표
        x_source_plane, y_source_plane = lens_equation(x_grid, y_grid, alpha_x, alpha_y)

        # 소스 이미지 생성 (중앙이 0,0)
        source_image = create_source_image(grid_size, source_pos_x, source_pos_y, source_size)

        # 렌즈된 이미지 생성
        lensed_image = np.zeros_like(x_grid)
        
        # 보간법을 사용하여 렌즈된 이미지 생성 (nearest-neighbor interpolation)
        # 실제 구현에서는 scipy.ndimage.map_coordinates 등을 사용하는 것이 더 정확합니다.
        # 여기서는 간단화를 위해 인덱스를 직접 매핑합니다.
        
        # 소스 평면 좌표를 픽셀 인덱스로 변환 (0 ~ grid_size-1)
        # 소스 평면의 중앙도 0,0으로 가정하고 변환
        x_src_idx = np.round(x_source_plane + half_grid).astype(int)
        y_src_idx = np.round(y_source_plane + half_grid).astype(int)

        # 유효한 인덱스 범위 확인
        valid_indices = (x_src_idx >= 0) & (x_src_idx < grid_size) & \
                        (y_src_idx >= 0) & (y_src_idx < grid_size)

        # 유효한 위치에 대해 픽셀 값 할당
        lensed_image[valid_indices] = source_image[y_src_idx[valid_indices], x_src_idx[valid_indices]]

        # 시각화
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("원본 광원 이미지 (Source Plane)")
            fig_source, ax_source = plt.subplots(figsize=(6, 6))
            ax_source.imshow(source_image, cmap='magma', origin='lower',
                             extent=[-half_grid, half_grid, -half_grid, half_grid])
            ax_source.set_title("Original Source")
            ax_source.set_xlabel("X (pixels)")
            ax_source.set_ylabel("Y (pixels)")
            ax_source.axvline(0, color='gray', linestyle='--', linewidth=0.5)
            ax_source.axhline(0, color='gray', linestyle='--', linewidth=0.5)
            ax_source.plot(source_pos_x, source_pos_y, 'x', color='cyan', markersize=10, label='Source Center')
            ax_source.legend()
            st.pyplot(fig_source)

        with col2:
            st.subheader("중력렌즈된 이미지 (Image Plane)")
            fig_lensed, ax_lensed = plt.subplots(figsize=(6, 6))
            ax_lensed.imshow(lensed_image, cmap='magma', origin='lower',
                              extent=[-half_grid, half_grid, -half_grid, half_grid])
            ax_lensed.set_title("Lensed Image")
            ax_lensed.set_xlabel("X (pixels)")
            ax_lensed.set_ylabel("Y (pixels)")
            ax_lensed.axvline(0, color='gray', linestyle='--', linewidth=0.5)
            ax_lensed.axhline(0, color='gray', linestyle='--', linewidth=0.5)
            ax_lensed.plot(0, 0, 'o', color='white', markersize=10, label='Lens Center')
            ax_lensed.legend()
            st.pyplot(fig_lensed)

    st.success("시뮬레이션 완료!")

st.markdown("""
---
**참고:**
* 이 시뮬레이션은 매우 간단한 점 질량 렌즈 모델을 사용하며, 실제 천체 물리 현상을 완벽하게 반영하지 않습니다.
* 실제 중력렌즈 연구에서는 `PyAutoLens`, `lenstronomy`, `Caustics`와 같은 전문 라이브러리를 사용하여 더 복잡한 렌즈 및 광원 모델, 이미지 처리, 통계적 모델링 등을 수행합니다.
* `h5py`나 `astropy.io.fits`를 사용하여 FITS 형식의 실제 관측 데이터를 로드하고 시각화할 수도 있습니다.
""")
