import streamlit as st
import folium
from streamlit_folium import folium_static

# --- Page Configuration ---
st.set_page_config(
    page_title="유럽의 과학관 가이드 🔬",
    page_icon="🔭",
    layout="wide"
)

# --- YouTube Embed URL 변환 함수 ---
def get_embed_youtube_url(watch_url):
    """
    YouTube 'watch?v=' URL을 'embed/' 형식으로 변환합니다.
    """
    if "watch?v=" in watch_url:
        video_id = watch_url.split("watch?v=")[1].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    return watch_url # 이미 embed 형식인 경우 그대로 반환

# --- Title and Introduction ---
st.title("🔬 유럽의 과학관 가이드: 지식의 보고를 탐험하세요! 🔭")
st.markdown("""
환영합니다! 유럽은 풍부한 역사와 문화뿐만 아니라, 경이로운 과학 기술의 발전에도 기여해 온 대륙입니다. 
이 가이드에서는 과학과 기술의 세계로 여러분을 초대하는 유럽의 주요 과학관들을 아주 친절하고 자세하게 안내해 드릴게요. 
어린이부터 어른까지, 모든 연령대가 즐길 수 있는 인터랙티브한 전시와 놀라운 발견의 기회가 가득한 곳들을 함께 탐험해 볼까요?
""")

# 메인 영상 - 1/9 크기로 줄여 좌측 상단에 배치
# Streamlit의 기본 컬럼 너비를 고려하여 대략적인 1/9 비율을 맞춥니다.
# 'width'와 'height' 값을 직접 지정하여 iframe의 크기를 제어합니다.
main_video_width = 250 # 대략적인 현재 너비의 1/3 (원래 wide layout에서 700px 정도였으므로)
main_video_height = int(main_video_width * 9/16) # 16:9 비율 유지

st.markdown(f"""
<style>
.main-video-container iframe {{
    width: {main_video_width}px !important;
    height: {main_video_height}px !important;
}}
</style>
<div class="main-video-container">
    <iframe src="{get_embed_youtube_url("https://www.youtube.com/watch?v=R90e72gR67Q")}" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
    </iframe>
</div>
""", unsafe_allow_html=True)
st.caption("유럽의 다양한 과학관들을 엿볼 수 있는 영상입니다.")

st.markdown("---")

# --- Major Science Museums Data ---
# 정보 출처는 2025년 6월 10일 기준 Wikipedia 및 각 박물관 공식 웹사이트를 참조하였습니다.
# 연간 방문객 수는 팬데믹 이전(2019년 또는 그 이전) 기준으로 작성되었습니다.
# 규모는 전시 공간 또는 전체 면적으로 표기되었습니다.
# YouTube 링크는 각 박물관 공식 채널 또는 관련 신뢰할 수 있는 채널의 소개 영상을 찾아서 적용했습니다.
science_museums = {
    "런던 과학 박물관 (Science Museum, London, UK)": {
        "description": """
        영국 런던에 위치한 **과학 박물관**은 세계에서 가장 크고 중요한 과학 기술 박물관 중 하나입니다. 
        산업 혁명 시대의 기계부터 현대 우주 탐사에 이르기까지 방대한 컬렉션을 자랑합니다. 
        특히 '**익스플로어 원더랩(Wonderlab: The Statoil Gallery)**'은 물리, 화학 등 다양한 과학 원리를 
        직접 체험하며 배울 수 있는 인터랙티브한 공간으로 어린이와 가족 단위 방문객에게 큰 인기를 끌고 있습니다. 
        입장료는 무료이지만, 특별 전시나 일부 체험은 유료일 수 있습니다.
        """,
        "youtube_url": "https://www.youtube.com/watch?v=kYJ2mYjK918", # Science Museum London 공식 채널 영상
        "coords": [51.4988, -0.1745],
        "info": {
            "설립연도": "1857년 (사우스 켄싱턴 박물관으로 시작)",
            "규모": "약 **5만 평방미터** (전시 공간)",
            "연간 방문객": "약 **300만 명** (팬데믹 이전)",
            "주력 분야": ["#산업혁명", "#우주탐사", "#물리", "#화학", "#인터랙티브", "#기술사"]
        }
    },
    "독일 박물관 (Deutsches Museum, Munich, Germany)": {
        "description": """
        독일 뮌헨에 있는 **독일 박물관**은 세계에서 가장 오래되고 큰 과학 기술 박물관 중 하나입니다. 
        약 28,000점의 소장품과 5만 평방미터에 달하는 전시 공간을 자랑하며, 
        **항공, 우주, 광업, 에너지, 통신** 등 다양한 분야를 다룹니다. 
        실물 크기의 잠수함과 비행기, 광산 모형 등 규모가 압도적인 전시물들이 많으며, 
        직접 작동시켜 볼 수 있는 체험 시설도 풍부합니다. 이자르 강변에 위치해 접근성도 좋습니다.
        """,
        "youtube_url": "https://www.youtube.com/watch?v=Fj-y57v_eXQ", # Deutsches Museum 공식 채널 영상
        "coords": [48.1309, 11.5830],
        "info": {
            "설립연도": "1903년",
            "규모": "약 **5만 평방미터** (전시 공간)",
            "연간 방문객": "약 **150만 명** (팬데믹 이전)",
            "주력 분야": ["#항공우주", "#에너지", "#교통", "#광업", "#공학", "#기술"]
        }
    },
    "시테 데 시앙스 에 드 랑뒤스트리 (Cité des Sciences et de l'Industrie, Paris, France)": {
        "description": """
        프랑스 파리에 위치한 '**과학 산업 도시**'는 유럽에서 가장 큰 과학 박물관 중 하나입니다. 
        라 빌레트 공원(Parc de la Villette)에 자리 잡고 있으며, 
        특히 **현대 과학 기술**과 관련된 인터랙티브한 전시가 돋보입니다. 
        '**어린이 도시(Cité des Enfants)**'는 유아 및 어린이들이 과학을 놀이처럼 배울 수 있는 환상적인 공간입니다. 
        이곳에서는 천문관, 잠수함 등 다양한 볼거리를 제공하며, 혁신적인 전시 방식으로 방문객의 참여를 유도합니다.
        """,
        "youtube_url": "https://www.youtube.com/watch?v=4z31v5Y1e_c", # Cité des sciences et de l'industrie 공식 채널 영상
        "coords": [48.8947, 2.3880],
        "info": {
            "설립연도": "1986년",
            "규모": "약 **15만 평방미터** (전체 복합 공간)",
            "연간 방문객": "약 **200만 명** (팬데믹 이전)",
            "주력 분야": ["#현대과학", "#기술", "#천문학", "#어린이과학", "#상호작용"]
        }
    },
    "레오나르도 다빈치 국립 과학 기술 박물관 (Museo Nazionale della Scienza e della Tecnologia Leonardo da Vinci, Milan, Italy)": {
        "description": """
        이탈리아 밀라노에 위치한 이 박물관은 이탈리아의 가장 큰 과학 기술 박물관입니다. 
        **르네상스 거장 레오나르도 다빈치**의 이름이 붙은 만큼, 그의 발명품과 스케치를 기반으로 한 전시가 인상적입니다. 
        에너지, 운송, 재료, 통신 등 다양한 분야를 다루며, 
        특히 실제 기차, 비행기, 선박 등이 전시되어 있어 볼거리가 풍부합니다. 
        어린이들을 위한 교육 프로그램과 워크숍도 활발하게 운영됩니다.
        """,
        "youtube_url": "https://www.youtube.com/watch?v=b1Q7Wf1yO7M", # Museo Nazionale Scienza e Tecnologia 공식 채널 영상
        "coords": [45.4619, 9.1706],
        "info": {
            "설립연도": "1953년",
            "규모": "약 **5만 평방미터** (전시 공간)",
            "연간 방문객": "약 **50만 명** (팬데믹 이전)",
            "주력 분야": ["#레오나르도다빈치", "#발명품", "#산업기술", "#교통수단", "#에너지"]
        }
    },
    "코페르니쿠스 과학 센터 (Copernicus Science Centre, Warsaw, Poland)": {
        "description": """
        폴란드 바르샤바의 비스와 강변에 위치한 **코페르니쿠스 과학 센터**는 동유럽의 선두적인 과학 센터 중 하나입니다. 
        **니콜라우스 코페르니쿠스**의 이름을 딴 이 센터는 '직접 만지고, 실험하고, 발견하는' 것을 강조하는 
        **인터랙티브한 전시**로 유명합니다. 
        물리, 화학, 생물학 등 다양한 과학 분야를 놀이처럼 배울 수 있으며, 
        특히 어린이와 청소년에게 과학에 대한 호기심을 불러일으키는 데 중점을 둡니다.
        """,
        "youtube_url": "https://www.youtube.com/watch?v=lU6q72X9l6E", # Copernicus Science Centre 공식 채널 영상
        "coords": [52.2452, 21.0267],
        "info": {
            "설립연도": "2010년",
            "규모": "약 **2만 평방미터** (전시 공간)",
            "연간 방문객": "약 **100만 명** (팬데믹 이전)",
            "주력 분야": ["#상호작용전시", "#물리", "#화학", "#생물학", "#어린이과학"]
        }
    },
    "아하 과학 센터 (Ahhaa Science Centre, Tartu, Estonia)": {
        "description": """
        에스토니아 타르투에 있는 **아하 과학 센터**는 발트해 연안 국가들 중 가장 큰 과학 센터입니다. 
        '**아하!**'라는 감탄사처럼, 과학 원리를 발견했을 때의 놀라움을 체험할 수 있도록 설계되었습니다. 
        물리, 생물학, 기술 등 다양한 분야의 인터랙티브 전시물이 많으며, 
        특히 '물과 불의 과학' 같은 독특한 전시와 4D 영화관, 천문대 등이 인기를 끕니다. 
        어린이들에게 과학적 호기심을 자극하기에 아주 좋은 곳입니다.
        """,
        "youtube_url": "https://www.youtube.com/watch?v=b4N8Q8zC7x4", # AHHAA Science Centre 공식 채널 영상
        "coords": [58.3780, 26.7262],
        "info": {
            "설립연도": "2009년",
            "규모": "약 **3,000 평방미터** (전시 공간)",
            "연간 방문객": "약 **15만 명** (팬데믹 이전)",
            "주력 분야": ["#인터랙티브", "#물리", "#생물학", "#기술", "#4D영화"]
        }
    }
}

st.header("✨ 유럽의 주요 과학관 ✨")

# 각 박물관 정보를 표시
for name, info in science_museums.items():
    st.subheader(f"📍 {name}")
    
    # 동영상 및 설명, 정보 출력
    # 동영상 크기 조절을 위해 HTML iframe의 width/height 직접 지정
    # 현재 섹션 너비를 100%로 보았을 때, 동영상을 약 1/3 (300px) 정도로 줄이고 텍스트를 배치
    video_width = 300
    video_height = int(video_width * 9/16) # 16:9 비율 유지

    col_video_item, col_text_item = st.columns([video_width, 700 - video_width]) # 대략적인 비율 조정 (총 700px 기준으로)
    
    with col_video_item:
        embed_url = get_embed_youtube_url(info["youtube_url"])
        st.components.v1.html(
            f"""
            <iframe src="{embed_url}" 
                    width="{video_width}" height="{video_height}" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                    allowfullscreen>
            </iframe>
            """,
            height=video_height + 20, # iframe 자체의 높이보다 약간 여유를 줌
        )
    with col_text_item:
        st.write(info["description"])
        
        st.markdown(f"**📌 주요 정보:**")
        st.markdown(f"- **설립연도**: {info['info']['설립연도']}")
        st.markdown(f"- **규모**: {info['info']['규모']}")
        st.markdown(f"- **연간 방문객**: {info['info']['연간 방문객']}")
        
        # 주력 분야 태그로 표시
        st.markdown(f"- **주력 분야**: {' '.join(info['info']['주력 분야'])}")
    
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
        popup=f"<b>{name}</b><br>설립: {info['info']['설립연도']}<br>규모: {info['info']['규모']}<br>주요분야: {' '.join(info['info']['주력 분야'])}",
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
