import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image # Pillow 라이브러리 (이미지 처리에 사용)

# --- Page Configuration ---
st.set_page_config(
    page_title="스페인 북부 관광지 가이드 🇪🇸",
    page_icon="🇪🇸",
    layout="wide" # 넓은 레이아웃 사용
)

# --- Title and Introduction ---
st.title("🇪🇸 스페인 북부 관광지 가이드 🇪🇸")
st.markdown("""
환영합니다! 스페인 북부의 숨겨진 보석 같은 매력들을 탐험할 준비가 되셨나요? 
이 가이드에서는 대서양의 시원한 바람, 웅장한 산맥, 그리고 풍부한 역사와 미식 문화가 어우러진 
스페인 북부의 꼭 방문해야 할 주요 명소들을 아주 친절하고 자세하게 안내해 드릴게요. 
바스크 지방의 현대적인 예술부터 갈리시아의 순례길까지, 스페인 북부는 모든 여행자의 마음을 사로잡을 준비가 되어 있습니다!
""")

# 이미지 파라미터 수정: use_column_width -> use_container_width
st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/San_Sebastian_Old_Town_2021.jpg/1280px-San_Sebastian_Old_Town_2021.jpg", 
         caption="산세바스티안의 아름다운 구시가지 풍경", use_container_width=True)

st.markdown("---")

# --- Major Attractions Data ---
attractions = {
    "빌바오 (Bilbao)": {
        "description": """
        바스크 지방의 심장부인 빌바오는 산업 도시에서 문화 예술의 중심지로 성공적으로 변모한 도시입니다. 
        프랭크 게리가 설계한 구겐하임 미술관은 빌바오의 상징이자 현대 건축의 걸작으로, 
        티타늄 외벽이 햇빛에 반짝이며 시시각각 다른 모습을 보여줍니다. 
        미술관 주변으로는 아름다운 산책로와 다리들이 이어져 있으며, 
        구시가지(Casco Viejo)에서는 핀초(Pinxto)를 맛보며 현지 문화를 체험할 수 있습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Guggenheim_Museum_Bilbao_Spain.jpg/1280px-Guggenheim_Museum_Bilbao_Spain.jpg",
        "coords": [43.2688, -2.9345]
    },
    "산세바스티안 (San Sebastián)": {
        "description": """
        '북부의 진주'라 불리는 산세바스티안은 스페인 최고의 해변 휴양 도시 중 하나입니다. 
        아름다운 라 콘차 해변(La Concha Beach)은 초승달 모양으로 펼쳐져 있으며, 
        주변으로는 고급스러운 건축물들이 늘어서 있습니다. 
        산세바스티안은 또한 미식의 도시로도 유명하며, 
        세계적으로 인정받는 미슐랭 스타 레스토랑이 많고, 작은 바에서 즐기는 핀초 문화가 발달해 있습니다. 
        몬테 이겔도(Monte Igueldo)에서는 도시의 파노라마 전경을 감상할 수 있습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/San_Sebasti%C3%A1n_-_La_Concha_Beach_Panorama_2021.jpg/1280px-San_Sebasti%C3%A1n_-_La_Concha_Beach_Panorama_2021.jpg",
        "coords": [43.3183, -1.9812]
    },
    "산탄데르 (Santander)": {
        "description": """
        칸타브리아 지방의 주도인 산탄데르는 우아한 해변 도시입니다. 
        막달레나 반도에 위치한 막달레나 궁전(Palacio de la Magdalena)은 아름다운 정원과 함께 멋진 해안 경치를 자랑하며, 
        이곳에서 바라보는 도시와 바다의 전경이 일품입니다. 
        엘 사르디네로(El Sardinero) 해변은 휴식을 취하기에 좋으며, 
        도시 곳곳에서 신선한 해산물 요리를 맛볼 수 있습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Santander_from_Magdalena_Palace.jpg/1280px-Santander_from_Magdalena_Palace.jpg",
        "coords": [43.4623, -3.8040]
    },
    "오비에도 (Oviedo)": {
        "description": """
        아스투리아스 지방의 매력적인 수도인 오비에도는 중세 시대의 분위기가 물씬 풍기는 도시입니다. 
        유네스코 세계유산으로 등재된 프레로마네스크 양식의 교회들(산 미겔 데 릴로, 산타 마리아 델 나랑코)은 
        유럽 건축사의 중요한 유산입니다. 
        구시가지는 아기자기한 광장들과 좁은 골목길로 이루어져 있으며, 
        사과주(Sidra)와 함께 신선한 해산물 요리를 즐길 수 있는 시드라 바(Sidrería)들이 많습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Cathedral_of_San_Salvador%2C_Oviedo%2C_Asturias%2C_Spain.jpg/1280px-Cathedral_of_San_Salvador%2C_Oviedo%2C_Asturias%2C_Spain.jpg",
        "coords": [43.3602, -5.8447]
    },
    "산티아고 데 콤포스텔라 (Santiago de Compostela)": {
        "description": """
        세계적으로 유명한 산티아고 순례길의 최종 목적지이자 갈리시아 지방의 주도입니다. 
        웅장한 산티아고 데 콤포스텔라 대성당은 순례자들의 영혼을 울리는 장엄함을 지니고 있습니다. 
        유네스코 세계유산으로 지정된 구시가지는 로마네스크, 고딕, 바로크 양식의 건축물들이 조화를 이루며, 
        순례자들의 활기찬 에너지와 역사적인 분위기가 독특한 조화를 이룹니다. 
        갈리시아 특유의 해산물 요리도 꼭 맛봐야 할 별미입니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Catedral_de_Santiago_de_Compostela_y_Praza_do_Obradoiro.jpg/1280px-Catedral_de_Santiago_de_Compostela_y_Praza_do_Obradoiro.jpg",
        "coords": [42.8782, -8.5448]
    },
    "코바동가 (Covadonga)": {
        "description": """
        아스투리아스 지방의 픽스 데 에우로파 국립공원 내에 위치한 코바동가는 스페인 역사에서 중요한 의미를 지니는 곳입니다. 
        이곳은 8세기 무어인에 대항하여 기독교 세력이 첫 승리를 거둔 곳으로, 스페인 재정복 운동의 시발점이 되었습니다. 
        신비로운 코바동가 동굴과 아름다운 성당, 그리고 웅장한 산악 경관이 어우러져 영적인 아름다움을 선사합니다. 
        인근의 코바동가 호수(Lagos de Covadonga)는 그림 같은 풍경으로 유명합니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Santuario_de_Covadonga_Asturias.jpg/1280px-Santuario_de_Covadonga_Asturias.jpg",
        "coords": [43.3039, -5.0232]
    }
}

st.header("✨ 스페인 북부의 주요 관광 명소 ✨")

for name, info in attractions.items():
    st.subheader(f"📍 {name}")
    col1, col2 = st.columns([1, 2])
    with col1:
        # 이미지 파라미터 수정: use_column_width -> use_container_width
        st.image(info["image"], caption=name, use_container_width=True)
    with col2:
        st.write(info["description"])
    st.markdown("---")

# --- Interactive Map with Folium ---
st.header("🗺️ 스페인 북부 주요 관광지 지도")
st.markdown("아래 지도에서 스페인 북부의 주요 관광지들을 한눈에 확인해 보세요!")

# Create a Folium map centered on Northern Spain
m = folium.Map(location=[43.2, -4.5], zoom_start=6.5, control_scale=True) # Adjusted zoom for Northern Spain

# Add markers for each attraction
for name, info in attractions.items():
    folium.Marker(
        location=info["coords"],
        popup=f"<b>{name}</b><br>{info['description'][:100]}...", # Show first 100 chars of description
        tooltip=name,
        icon=folium.Icon(color="darkblue", icon="info-sign") # Changed marker color for Spain
    ).add_to(m)

# Display the map
folium_static(m, width=700, height=500) # Adjust width/height as needed

st.markdown("---")

# --- Closing Remarks ---
st.header("💖 스페인 북부 여행, 즐거운 추억 만드시길 바랍니다!")
st.markdown("""
이 가이드가 여러분의 스페인 북부 여행 계획에 도움이 되었기를 바랍니다. 
아름다운 자연과 깊은 역사가 공존하는 스페인 북부에서 잊지 못할 아름다운 추억을 많이 만드시길 진심으로 응원합니다! 
궁금한 점이 있다면 언제든지 다시 찾아주세요! 감사합니다!
""")

st.markdown("---")
st.caption("Made with ❤️ by Your Friendly AI Guide")
