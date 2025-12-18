import streamlit as st

# 페이지 설정
st.set_page_config(page_title="과목별 맞춤 영화 추천", page_icon="🎬")

# 과목별 영화 데이터 (이미지, 정보, 추천 이유)
movie_data = {
    "수학": {
        "title": "이미테이션 게임",
        "info": "장르: 드라마, 스릴러 | 감독: 모튼 틸덤 | 주연: 베네딕트 컴버배치",
        "reason": "천재 수학자 앨런 튜링이 암호를 풀기 위해 수학적 논리를 사용하는 과정이 수학의 매력을 잘 보여줍니다.",
        "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yx%2FbtqBy8R8yX8%2Fk6y6vK6kS6K6kS6kS6kS6k%2Fimg.jpg"
    },
    "과학(물리/우주)": {
        "title": "인터스텔라",
        "info": "장르: SF | 감독: 크리스토퍼 놀란 | 주연: 매튜 맥커너히",
        "reason": "상대성 이론, 블랙홀, 웜홀 등 고도의 과학적 고증을 바탕으로 우주의 신비와 경이로움을 체험할 수 있습니다.",
        "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yx%2FbtqBy8R8yX8%2Fk6y6vK6kS6K6kS6kS6kS6k%2Fimg.jpg" # 예시용 URL
    },
    "역사": {
        "title": "명량",
        "info": "장르: 액션, 드라마 | 감독: 김한민 | 주연: 최민식",
        "reason": "역사적 사실을 바탕으로 이순신 장군의 리더십과 지략을 생생하게 그려내어 역사를 공부하는 즐거움을 줍니다.",
        "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yx%2FbtqBy8R8yX8%2Fk6y6vK6kS6K6kS6kS6kS6k%2Fimg.jpg"
    },
    "미술": {
        "title": "러빙 빈센트",
        "info": "장르: 애니메이션, 미스터리 | 감독: 도로타 코비엘라",
        "reason": "세계 최초의 유화 애니메이션으로, 고흐의 화풍을 그대로 살린 영상미가 미술적 영감을 자극합니다.",
        "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yx%2FbtqBy8R8yX8%2Fk6y6vK6kS6K6kS6kS6kS6k%2Fimg.jpg"
    },
    "체육": {
        "title": "머니볼",
        "info": "장르: 드라마 | 감독: 베넷 밀러 | 주연: 브래드 피트",
        "reason": "스포츠 뒤에 숨겨진 전략과 데이터 분석을 다루어, 운동 그 이상의 재미와 통찰력을 제공합니다.",
        "image_url": "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yx%2FbtqBy8R8yX8%2Fk6y6vK6kS6K6kS6kS6kS6k%2Fimg.jpg"
    }
}

# 메인 UI 구성
st.title("🎓 과목별 맞춤 영화 추천 서비스")
st.write("가장 좋아하는 과목을 선택하시면 그에 맞는 흥미로운 영화를 추천해 드립니다.")

# 사이드바에서 과목 선택
subject = st.sidebar.selectbox(
    "좋아하는 과목을 골라보세요:",
    options=list(movie_data.keys())
)

# 결과 표시
if subject:
    movie = movie_data[subject]
    
    st.divider()
    
    # 두 개의 열로 나누어 이미지와 정보 배치
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        # 영화 포스터 이미지 (웹 URL에서 직접 가져옴)
        st.image(movie["image_url"], use_container_width=True)
    
    with col2:
        st.header(f"🎥 {movie['title']}")
        st.write(f"**ℹ️ 기본 정보**")
        st.info(movie["info"])
        
        st.write(f"**💡 왜 이 영화를 추천하나요?**")
        st.success(movie["reason"])

st.sidebar.write("---")
st.sidebar.caption("본 앱은 Streamlit을 사용하여 제작되었습니다.")
