import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image

# --- Page Configuration ---
st.set_page_config(
    page_title="캐나다 주요 관광지 가이드 🍁",
    page_icon="🍁",
    layout="wide"
)

# --- Title and Introduction ---
st.title("🍁 캐나다 주요 관광지 가이드 🍁")
st.markdown("""
환영합니다! 광활하고 아름다운 캐나다의 매력적인 관광지들을 탐험할 준비가 되셨나요? 
이 가이드에서는 캐나다의 꼭 방문해야 할 주요 명소들을 아주 친절하고 자세하게 안내해 드릴게요. 
대자연의 경이로움부터 활기찬 도시의 매력까지, 캐나다는 모든 여행자의 마음을 사로잡을 준비가 되어 있습니다!
""")

st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Canadian_Rockies_Mountain_Range.jpg/1280px-Canadian_Rockies_Mountain_Range.jpg", 
         caption="웅장한 캐나다 로키 산맥의 풍경", use_column_width=True)

st.markdown("---")

# --- Major Attractions Data ---
attractions = {
    "밴프 국립공원 (Banff National Park)": {
        "description": """
        캐나다 최초의 국립공원이자 유네스코 세계유산으로 등재된 밴프 국립공원은 캐나다 로키의 심장부입니다. 
        에메랄드빛 호수, 웅장한 산봉우리, 그림 같은 빙하가 어우러져 숨 막히는 절경을 선사합니다. 
        루이스 호수, 모레인 호수, 존스턴 캐년 등 셀 수 없이 많은 명소가 있으며, 
        하이킹, 카누, 스키 등 다양한 아웃도어 활동을 즐길 수 있습니다. 
        특히 루이스 호수는 그 어떤 설명으로도 부족할 만큼 아름다운 풍경을 자랑합니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Lake_Louise_in_Banff_National_Park%2C_Alberta%2C_Canada.jpg/1280px-Lake_Louise_in_Banff_National_Park%2C_Alberta%2C_Canada.jpg",
        "coords": [51.4259, -116.2759] # Lake Louise
    },
    "나이아가라 폭포 (Niagara Falls)": {
        "description": """
        세계 3대 폭포 중 하나인 나이아가라 폭포는 캐나다와 미국의 국경에 걸쳐 있으며, 
        그 엄청난 규모와 웅장함으로 방문객을 압도합니다. 
        말발굽 모양의 캐나다 폭포(Horseshoe Falls)는 특히 유명하며, 
        안개 속의 숙녀호(Maid of the Mist) 유람선을 타고 폭포 바로 앞까지 다가가 그 위엄을 직접 느낄 수 있습니다. 
        밤에는 화려한 조명으로 더욱 환상적인 분위기를 연출합니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Niagara_Falls%2C_Ontario%2C_Canada_2016.jpg/1280px-Niagara_Falls%2C_Ontario%2C_Canada_2016.jpg",
        "coords": [43.0891, -79.0837]
    },
    "토론토 (Toronto)": {
        "description": """
        캐나다 최대의 도시이자 온타리오주의 주도인 토론토는 다문화가 공존하는 활기찬 대도시입니다. 
        상징적인 CN 타워에서는 도시의 멋진 스카이라인을 한눈에 볼 수 있으며, 
        세인트 로렌스 마켓, 로열 온타리오 박물관, 디스틸러리 디스트릭트 등 다양한 명소들이 있습니다. 
        세계적인 수준의 레스토랑, 쇼핑, 예술을 경험할 수 있는 도시입니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Toronto_-_ON_-_Toronto_Waterfront.jpg/1280px-Toronto_-_ON_-_Toronto_Waterfront.jpg",
        "coords": [43.6532, -79.3832]
    },
    "밴쿠버 (Vancouver)": {
        "description": """
        브리티시컬럼비아주의 해안가에 위치한 밴쿠버는 산, 바다, 도시가 아름답게 어우러진 세계적으로 살기 좋은 도시 중 하나입니다. 
        스탠리 파크는 도심 속의 오아시스 같은 곳이며, 그랜빌 아일랜드에서는 신선한 해산물과 예술 작품을 만날 수 있습니다. 
        개스타운의 역사적인 거리와 랍슨 스트리트의 쇼핑 또한 놓칠 수 없는 즐거움입니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Vancouver_Skyline_from_Kits_Beach.jpg/1280px-Vancouver_Skyline_from_Kits_Beach.jpg",
        "coords": [49.2827, -123.1207]
    },
    "퀘벡 시티 (Quebec City)": {
        "description": """
        북미에서 가장 오래된 유럽풍 도시 중 하나인 퀘벡 시티는 유네스코 세계유산으로 지정된 아름다운 도시입니다. 
        성벽으로 둘러싸인 올드 퀘벡은 마치 유럽의 작은 마을에 온 듯한 착각을 불러일으킵니다. 
        프롱트낙 성, 테라스 뒤프랭, 노트르담 대성당 등 역사적인 명소들이 가득하며, 
        겨울에는 세계적인 퀘벡 윈터 카니발이 열려 더욱 특별한 경험을 선사합니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Quebec_City_Skyline.jpg/1280px-Quebec_City_Skyline.jpg",
        "coords": [46.8139, -71.2080]
    },
    "몬트리올 (Montreal)": {
        "description": """
        퀘벡주에서 가장 큰 도시인 몬트리올은 북미 속의 작은 프랑스로 불릴 만큼 독특한 문화와 매력을 지닌 도시입니다. 
        노트르담 대성당의 웅장함, 올드 몬트리올의 cobblestone 거리, 지하 도시(Underground City)의 편리함, 
        그리고 몬트리올의 다양한 축제들은 방문객들에게 잊을 수 없는 경험을 선사합니다. 
        프랑스어와 영어가 함께 사용되는 독특한 분위기를 느낄 수 있습니다.
        """,
        "image": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Montreal_skyline_and_Mount_Royal.jpg/1280px-Montreal_skyline_and_Mount_Royal.jpg",
        "coords": [45.5017, -73.5673]
    }
}

st.header("✨ 캐나다의 주요 관광 명소 ✨")

for name, info in attractions.items():
    st.subheader(f"📍 {name}")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(info["image"], caption=name, use_column_width=True)
    with col2:
        st.write(info["description"])
    st.markdown("---")

# --- Interactive Map with Folium ---
st.header("🗺️ 캐나다 주요 관광지 지도")
st.markdown("아래 지도에서 캐나다의 주요 관광지들을 한눈에 확인해 보세요!")

# Create a Folium map centered on Canada
m = folium.Map(location=[56.1304, -106.3468], zoom_start=3.5, control_scale=True)

# Add markers for each attraction
for name, info in attractions.items():
    folium.Marker(
        location=info["coords"],
        popup=f"<b>{name}</b><br>{info['description'][:100]}...", # Show first 100 chars of description
        tooltip=name,
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# Display the map
folium_static(m, width=700, height=500) # Adjust width/height as needed

st.markdown("---")

# --- Closing Remarks ---
st.header("💖 캐나다 여행, 즐거운 추억 만드시길 바랍니다!")
st.markdown("""
이 가이드가 여러분의 캐나다 여행 계획에 도움이 되었기를 바랍니다. 
광활하고 다채로운 캐나다에서 잊지 못할 아름다운 추억을 많이 만드시길 진심으로 응원합니다! 
궁금한 점이 있다면 언제든지 다시 찾아주세요! 감사합니다!
""")

st.markdown("---")
st.caption("Made with ❤️ by Your Friendly AI Guide")
