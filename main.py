import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="유럽의 과학관 가이드 🔬",
    page_icon="🔭",
    layout="wide"
)

# --- Title and Introduction ---
st.title("🔬 유럽의 과학관 가이드: 지식의 보고를 탐험하세요! 🔭")
st.markdown("""
환영합니다! 유럽은 풍부한 역사와 문화뿐만 아니라, 경이로운 과학 기술의 발전에도 기여해 온 대륙입니다. 
이 가이드에서는 과학과 기술의 세계로 여러분을 초대하는 유럽의 주요 과학관들을 아주 친절하고 자세하게 안내해 드릴게요. 
어린이부터 어른까지, 모든 연령대가 즐길 수 있는 인터랙티브한 전시와 놀라운 발견의 기회가 가득한 곳들을 함께 탐험해 볼까요?
""")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Science_Museum_London_exterior.jpg/1280px-Science_Museum_London_exterior.jpg", 
         caption="런던 과학 박물관의 전경", use_container_width=True)

st.markdown("---")

# --- Major Science Museums Data ---
science_museums = {
    "런던 과학 박물관 (Science Museum, London, UK)": {
        "description": """
        영국 런던에 위치한 과학 박물관은 세계에서 가장 크고 중요한 과학 기술 박물관 중 하나입니다. 
        산업 혁명 시대의 기계부터 현대 우주 탐사에 이르기까지 방대한 컬렉션을 자랑합니다. 
        특히 '익스플로어 원더랩(Wonderlab: The Statoil Gallery)'은 물리, 화학 등 다양한 과학 원리를 
        직접 체험하며 배울 수 있는 인터랙티브한 공간으로 어린이와 가족 단위 방문객에게 큰 인기를 끌고 있습니다. 
        입장료는 무료이지만, 특별 전시나 일부 체험은 유료일 수 있습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Wonderlab_The_Statoil_Gallery_at_the_Science_Museum.jpg/1280px-Wonderlab_The_Statoil_Gallery_at_the_Science_Museum.jpg",
        "coords": [51.4988, -0.1745]
    },
    "독일 박물관 (Deutsches Museum, Munich, Germany)": {
        "description": """
        독일 뮌헨에 있는 독일 박물관은 세계에서 가장 오래되고 큰 과학 기술 박물관 중 하나입니다. 
        약 28,000점의 소장품과 5만 평방미터에 달하는 전시 공간을 자랑하며, 
        항공, 우주, 광업, 에너지, 통신 등 다양한 분야를 다룹니다. 
        실물 크기의 잠수함과 비행기, 광산 모형 등 규모가 압도적인 전시물들이 많으며, 
        직접 작동시켜 볼 수 있는 체험 시설도 풍부합니다. 이자르 강변에 위치해 접근성도 좋습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Deutsches_Museum_Munich_-_Panorma_of_the_Museum_Island.jpg/1280px-Deutsches_Museum_Munich_-_Panorma_of_the_Museum_Island.jpg",
        "coords": [48.1309, 11.5830]
    },
    "시테 데 시앙스 에 드 랑뒤스트리 (Cité des Sciences et de l'Industrie, Paris, France)": {
        "description": """
        프랑스 파리에 위치한 '과학 산업 도시'는 유럽에서 가장 큰 과학 박물관 중 하나입니다. 
        라 빌레트 공원(Parc de la Villette)에 자리 잡고 있으며, 
        특히 현대 과학 기술과 관련된 인터랙티브한 전시가 돋보입니다. 
        '어린이 도시(Cité des Enfants)'는 유아 및 어린이들이 과학을 놀이처럼 배울 수 있는 환상적인 공간입니다. 
        이곳에서는 천문관, 잠수함 등 다양한 볼거리를 제공하며, 혁신적인 전시 방식으로 방문객의 참여를 유도합니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/C%C3%AEt%C3%A9_des_sciences_et_de_l%27industrie_-_Ext%C3%A9rieur_-_Panoramique.jpg/1280px-C%C3%AEt%C3%A9_des_sciences_et_de_l%27industrie_-_Ext%C3%A9rieur_-_Panoramique.jpg",
        "coords": [48.8947, 2.3880]
    },
    "레오나르도 다빈치 국립 과학 기술 박물관 (Museo Nazionale della Scienza e della Tecnologia Leonardo da Vinci, Milan, Italy)": {
        "description": """
        이탈리아 밀라노에 위치한 이 박물관은 이탈리아의 가장 큰 과학 기술 박물관입니다. 
        르네상스 거장 레오나르도 다빈치의 이름이 붙은 만큼, 그의 발명품과 스케치를 기반으로 한 전시가 인상적입니다. 
        에너지, 운송, 재료, 통신 등 다양한 분야를 다루며, 
        특히 실제 기차, 비행기, 선박 등이 전시되어 있어 볼거리가 풍부합니다. 
        어린이들을 위한 교육 프로그램과 워크숍도 활발하게 운영됩니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Museo_della_Scienza_e_della_Tecnologia_Leonardo_da_Vinci_-_Entrance.jpg/1280px-Museo_della_Scienza_e_della_Tecnologia_Leonardo_da_Vinci_-_Entrance.jpg",
        "coords": [45.4619, 9.1706]
    },
    "코페르니쿠스 과학 센터 (Copernicus Science Centre, Warsaw, Poland)": {
        "description": """
        폴란드 바르샤바의 비스와 강변에 위치한 코페르니쿠스 과학 센터는 동유럽의 선두적인 과학 센터 중 하나입니다. 
        니콜라우스 코페르니쿠스의 이름을 딴 이 센터는 '직접 만지고, 실험하고, 발견하는' 것을 강조하는 
        인터랙티브한 전시로 유명합니다. 
        물리, 화학, 생물학 등 다양한 과학 분야를 놀이처럼 배울 수 있으며, 
        특히 어린이와 청소년에게 과학에 대한 호기심을 불러일으키는 데 중점을 둡니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Centrum_Nauki_Kopernik_%284%29.jpg/1280px-Centrum_Nauki_Kopernik_%284%29.jpg",
        "coords": [52.2452, 21.0267]
    },
    "아하 과학 센터 (Ahhaa Science Centre, Tartu, Estonia)": {
        "description": """
        에스토니아 타르투에 있는 아하 과학 센터는 발트해 연안 국가들 중 가장 큰 과학 센터입니다. 
        '아하!'라는 감탄사처럼, 과학 원리를 발견했을 때의 놀라움을 체험할 수 있도록 설계되었습니다. 
        물리, 생물학, 기술 등 다양한 분야의 인터랙티브 전시물이 많으며, 
        특히 '물과 불의 과학' 같은 독특한 전시와 4D 영화관, 천문대 등이 인기를 끕니다. 
        어린이들에게 과학적 호기심을 자극하기에 아주 좋은 곳입니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Ahhaa_Science_Centre_-_Tartu.jpg/1280px-Ahhaa_Science_Centre_-_Tartu.jpg",
        "coords": [58.3780, 26.7262]
    }
}

st.header("✨ 유럽의 주요 과학관 ✨")

for name, info in science_museums.items():
    st.subheader(f"📍 {name}")
    col1, col2 = st.columns([1, 2])
    with col1:
        # 이미지 파라미터 수정: use_column_width -> use_container_width
        st.image(info["image"], caption=name, use_container_width=True)
    with col2:
        st.write(info["description"])
    st.markdown("---")

# --- Interactive Map with Folium ---
st.header("🗺️ 유럽 과학관 지도")
st.markdown("아래 지도에서 유럽의 주요 과학관들을 한눈에 확인해 보세요!")

# Create a Folium map centered on Europe
m = folium.Map(location=[50.0, 10.0], zoom_start=4, control_scale=True) 

# Add markers for each museum
for name, info in science_museums.items():
    folium.Marker(
        location=info["coords"],
        popup=f"<b>{name}</b><br>{info['description'][:100]}...", # Show first 100 chars of description
        tooltip=name,
        icon=folium.Icon(color="blue", icon="flask", prefix="fa") # 과학관에 어울리는 아이콘 변경 (Font Awesome 아이콘)
    ).add_to(m)

# Display the map
folium_static(m, width=700, height=500) # Adjust width/height as needed

st.markdown("---")

# --- Closing Remarks ---
st.header("💖 유럽 과학관 여행, 즐거운 지식 탐험 되시길 바랍니다!")
st.markdown("""
이 가이드가 여러분의 유럽 여행에 과학적인 즐거움을 더하는 데 도움이 되었기를 바랍니다. 
흥미진진한 과학의 세계에서 잊지 못할 경험을 많이 만드시길 진심으로 응원합니다! 
궁금한 점이 있다면 언제든지 다시 찾아주세요! 감사합니다!
""")

st.markdown("---")
st.caption("Made with ❤️ by Your Friendly AI Guide")
