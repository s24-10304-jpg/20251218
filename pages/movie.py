import streamlit as st

# 페이지 설정
st.set_page_config(page_title="과목별 영화 추천", page_icon="🎬")

# 훨씬 안정적인 이미지 주소 (TMDB 또는 위키미디어 직접 링크)
movie_data = {
    "수학": {
        "title": "이미테이션 게임",
        "info": "장르: 드라마, 스릴러 | 주연: 베네딕트 컴버배치",
        "reason": "천재 수학자가 암호를 풀기 위해 수학적 논리를 사용하는 과정이 백미입니다.",
        "image_url": "https://image.tmdb.org/t/p/w500/zSqkw7S_p_p464971c_f603c_8.jpg" # 실제 포스터 경로
    },
    "과학": {
        "title": "인터스텔라",
        "info": "장르: SF | 감독: 크리스토퍼 놀란",
        "reason": "상대성 이론과 블랙홀 등 실제 과학 이론을 시각적으로 가장 완벽하게 구현했습니다.",
        "image_url": "https://image.tmdb.org/t/p/w500/n0997m57f3p8c71f5445763564c76.jpg" 
    },
    "역사": {
        "title": "명량",
        "info": "장르: 사극, 액션 | 주연: 최민식",
        "reason": "역사적 사실을 바탕으로 한 이순신 장군의 위대한 리더십을 배울 수 있습니다.",
        "image_url": "https://image.tmdb.org/t/p/w500/u690623f954f9441113524c96564.jpg"
    },
    "미술": {
        "title": "러빙 빈센트",
        "info": "장르: 애니메이션 | 내용: 반 고흐의 일생",
        "reason": "모든 프레임을 직접 유화로 그려낸, 미술 교과서 같은 영화입니다.",
        "image_url": "https://image.tmdb.org/t/p/w500/7754366e625516931666699313.jpg"
    }
}

st.title("🎬 과목별 영화 추천 서비스")
st.write("좋아하는 과목을 선택하면 관련 영화 정보를 보여드립니다.")

subject = st.selectbox("과목을 선택하세요", list(movie_data.keys()))

if subject:
    movie = movie_data[subject]
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # 1. 이미지 출력 시도
        try:
            st.image(movie["image_url"], use_container_width=True)
        except:
            st.warning("이미지를 불러오는 중입니다... 잠시만 기다려주세요.")
            # 2. 이미지가 안 나올 때를 대비해 링크 확인용 텍스트 출력
            st.write(f"[이미지 직접 보기]({movie['image_url']})")
            
    with col2:
        st.header(movie["title"])
        st.info(f"**정보:** {movie['info']}")
        st.success(f"**추천 이유:** {movie['reason']}")

st.caption("※ 이미지가 보이지 않는다면 새로고침(F5)을 하거나 잠시 기다려 주세요.")
