import streamlit as st

# 페이지 설정
st.set_page_config(page_title="과목별 영화 추천", page_icon="🎬")

# 데이터 설정 (안정적인 이미지 주소로 교체)
movie_data = {
    "수학": {
        "title": "이미테이션 게임 (The Imitation Game)",
        "info": "장르: 드라마, 스릴러 | 주연: 베네딕트 컴버배치",
        "reason": "암호 해독을 위해 수학적 논리를 사용하는 과정이 흥미진진합니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/5/5e/The_Imitation_Game_poster.jpg"
    },
    "과학": {
        "title": "인터스텔라 (Interstellar)",
        "info": "장르: SF | 감독: 크리스토퍼 놀란",
        "reason": "상대성 이론과 블랙홀 등 실제 과학 이론을 멋지게 시각화했습니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg"
    },
    "역사": {
        "title": "명량 (The Admiral)",
        "info": "장르: 사극, 액션 | 주연: 최민식",
        "reason": "역사적 사실을 바탕으로 한 위대한 승리의 기록을 볼 수 있습니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a5/The_Admiral_Roaring_Currents_poster.jpg"
    },
    "미술": {
        "title": "러빙 빈센트 (Loving Vincent)",
        "info": "장르: 애니메이션 | 내용: 반 고흐의 일생",
        "reason": "모든 장면이 유화로 그려진 미술 작품 그 자체인 영화입니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/0/01/Loving_Vincent_poster.jpg"
    },
    "체육": {
        "title": "머니볼 (Moneyball)",
        "info": "장르: 드라마, 야구 | 주연: 브래드 피트",
        "reason": "데이터 분석을 통해 야구 경기의 판도를 바꾸는 전략적인 영화입니다.",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/2/2e/Moneyball_Poster.jpg"
    }
}

st.title("🎬 좋아하는 과목별 영화 추천")
st.write("과목을 선택하면 관련 영화를 추천해 드립니다.")

# 과목 선택
subject = st.selectbox("어떤 과목을 가장 좋아하시나요?", list(movie_data.keys()))

if subject:
    movie = movie_data[subject]
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # 이미지를 불러오지 못할 경우 에러 메시지 대신 텍스트가 나오도록 설정
        try:
            st.image(movie["image_url"], caption=f"<{movie['title']}> 포스터")
        except:
            st.error("이미지를 불러올 수 없습니다. 링크를 확인해주세요.")
            
    with col2:
        st.header(movie["title"])
        st.subheader("📌 영화 정보")
        st.info(movie["info"])
        st.subheader("💡 추천 이유")
        st.success(movie["reason"])
