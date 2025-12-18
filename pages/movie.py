import streamlit as st

# 페이지 설정
st.set_page_config(page_title="과목별 영화 추천 서비스", page_icon="📚", layout="wide")

# 14개 과목 데이터 (이미지 URL 포함)
movie_data = {
    "프로그래밍": [
        {"title": "소셜 네트워크", "info": "드라마 | 주연: 제시 아이젠버그", "ott": "넷플릭스, 웨이브", "reason": "알고리즘이 세상의 소통 방식을 어떻게 바꾸는지 보여줍니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/8/8c/The_Social_Network_poster.png"},
        {"title": "잡스", "info": "전기, 드라마 | 주연: 애쉬튼 커쳐", "ott": "티빙, 왓챠", "reason": "IT 혁신가 스티브 잡스의 삶과 소프트웨어의 가치를 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/e/e0/Jobs_film_poster.jpg"}
    ],
    "수학": [
        {"title": "이미테이션 게임", "info": "드라마 | 주연: 베네딕트 컴버배치", "ott": "넷플릭스, 티빙", "reason": "수학적 논리로 전쟁의 암호를 해독하는 긴박한 과정을 담았습니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/5/5e/The_Imitation_Game_poster.jpg"},
        {"title": "이상한 나라의 수학자", "info": "드라마 | 주연: 최민식", "ott": "넷플릭스, 왓챠", "reason": "수학의 아름다움과 정답보다 중요한 과정의 가치를 일깨워줍니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/4/45/%EC%9D%B4%EC%83%81%ED%95%9C_%EB%82%98%EB%9D%BC%EC%9D%98_%EC%88%98%ED%95%99%EC%9E%90_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"}
    ],
    "영어": [
        {"title": "킹스 스피치", "info": "드라마 | 주연: 콜린 퍼스", "ott": "넷플릭스, 티빙", "reason": "언어의 힘과 소통의 중요성을 느낄 수 있는 실화 바탕 영화입니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a0/Kings_speech_poster.jpg"},
        {"title": "죽은 시인의 사회", "info": "드라마 | 주연: 로빈 윌리엄스", "ott": "디즈니+, 왓챠", "reason": "문학을 통해 삶의 주인이 되는 법을 배우는 감동적인 작품입니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/4/49/Dead_Poets_Society_poster.jpg"}
    ],
    "국어": [
        {"title": "말모이", "info": "드라마 | 주연: 유해진", "ott": "넷플릭스, 티빙", "reason": "우리말을 지키기 위한 노력을 통해 국어의 소중함을 깨닫게 합니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/c/c9/%EB%A7%90%EB%AA%A8%EC%9D%B4_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"},
        {"title": "동주", "info": "드라마 | 주연: 강하늘", "ott": "넷플릭스, 왓챠", "reason": "시인 윤동주의 삶을 통해 우리 문학에 담긴 시대적 아픔을 보여줍니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/6/67/%EB%8F%99%EC%A3%BC_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"}
    ],
    "역사": [
        {"title": "1987", "info": "드라마 | 주연: 김윤석", "ott": "넷플릭스, 티빙", "reason": "한국 현대사의 큰 전환점을 진정성 있게 그려낸 역사물입니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/e/e0/1987_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"},
        {"title": "남한산성", "info": "사극 | 주연: 이병헌", "ott": "넷플릭스, 티빙", "reason": "병자호란 당시의 기록을 통해 역사의 무게를 조명합니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/c/c2/%EB%82%A8%ED%95%9C%EC%82%B0%EC%84%B1_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"}
    ],
    "물리": [
        {"title": "오펜하이머", "info": "전기, 드라마 | 감독: 놀란", "ott": "티빙, 웨이브", "reason": "양자역학과 원자폭탄 개발을 통해 물리학자의 세계를 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/4/4a/Oppenheimer_%28film%29.jpg"},
        {"title": "인터스텔라", "info": "SF | 감독: 놀란", "ott": "넷플릭스", "reason": "상대성 이론과 우주 물리학을 경이로운 영상으로 구현했습니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/b/bc/Interstellar_film_poster.jpg"}
    ],
    "화학": [
        {"title": "마담 퀴리", "info": "전기 | 주연: 로자먼드 파이크", "ott": "왓챠", "reason": "방사능 발견이라는 화학사적 업적과 헌신을 보여줍니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a2/Radioactive_film_poster.jpg"},
        {"title": "다크 워터스", "info": "드라마 | 주연: 마크 러팔로", "ott": "넷플릭스", "reason": "화학물질의 사회적 책임과 위험성을 알리는 과정을 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/0/00/Dark_Waters_%282019_film%29.png"}
    ],
    "지구과학": [
        {"title": "투모로우", "info": "재난 | 주연: 데니스 퀘이드", "ott": "디즈니+", "reason": "기후 변화로 인한 빙하기를 통해 지구 환경을 고찰하게 합니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/5/58/The_Day_After_Tomorrow_movie.jpg"},
        {"title": "컨택트", "info": "SF | 주연: 에이미 아담스", "ott": "넷플릭스", "reason": "외계 생명체와의 조우를 통해 우주적 상상력을 자극합니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/d/df/Arrival%2C_Movie_Poster.jpg"}
    ],
    "생명과학": [
        {"title": "가타카", "info": "SF | 주연: 에단 호크", "ott": "넷플릭스", "reason": "유전자 조작 사회를 통해 생명 윤리의 중요성을 질문합니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/b/bb/Gattaca_poster.jpg"},
        {"title": "아일랜드", "info": "SF | 주연: 이완 맥그리거", "ott": "티빙", "reason": "복제인간 테마를 통해 생명 복제와 존엄성을 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/5/52/The_Island_poster.jpg"}
    ],
    "사회문제": [
        {"title": "기생충", "info": "드라마 | 감독: 봉준호", "ott": "넷플릭스, 티빙", "reason": "현대 사회의 계급 갈등 문제를 날카롭게 묘사한 수작입니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/6/60/%EA%B8%B0%EC%83%9D%EC%B6%A9_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"},
        {"title": "나, 다니엘 블레이크", "info": "드라마 | 감독: 켄 로치", "ott": "왓챠", "reason": "복지 제도의 허점과 인간 존엄성 문제를 심도 있게 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/a/a2/I%2C_Daniel_Blake_poster.jpg"}
    ],
    "윤리와사상": [
        {"title": "매트릭스", "info": "SF | 주연: 키아누 리브스", "ott": "넷플릭스", "reason": "실재와 허구에 대한 철학적 질문을 던지는 SF의 고전입니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/c/c1/The_Matrix_Poster.jpg"},
        {"title": "트루먼 쇼", "info": "드라마 | 주연: 짐 캐리", "ott": "넷플릭스", "reason": "자아의 실존과 진실에 대한 윤리적 고찰을 하게 만드는 영화입니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/a/ad/Truman_show_poster.jpg"}
    ],
    "세계지리": [
        {"title": "라이온", "info": "드라마 | 주연: 데브 파텔", "ott": "넷플릭스", "reason": "지리적 환경을 뛰어넘는 여정을 통해 세계의 문화를 보여줍니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/4/4c/Lion_2016_film_poster.png"},
        {"title": "슬럼독 밀리어네어", "info": "드라마 | 주연: 데브 파텔", "ott": "티빙", "reason": "인도의 사회상과 도시 지리적 배경을 생생하게 담았습니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/f/fe/Slumdog_Millionaire_poster.png"}
    ],
    "한국지리": [
        {"title": "고산자, 대동여지도", "info": "사극 | 주연: 차승원", "ott": "티빙", "reason": "우리나라 지형을 지도로 남기려 했던 김정호의 열정을 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/5/52/%EA%B3%A0%EC%82%B0%EC%9E%90%2C_%EB%8C%80%EB%8F%99%EC%97%AC%EC%A7%80%EB%8F%84_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"},
        {"title": "리틀 포레스트", "info": "드라마 | 주연: 김태리", "ott": "넷플릭스", "reason": "한국의 사계절 풍경과 농촌의 지리적 특성을 따뜻하게 담았습니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/a/a8/%EB%A6%AC%ED%8B%80_%ED%8F%AC%EB%A0%88%EC%8A%A4%ED%8A%B8_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"}
    ],
    "생활과 윤리": [
        {"title": "소원", "info": "드라마 | 주연: 설경구", "ott": "넷플릭스", "reason": "피해자와 연대의 힘을 통해 인간적 윤리 가치를 일깨웁니다.", "image_url": "https://upload.wikimedia.org/wikipedia/ko/7/77/%EC%86%8C%EC%9B%90_%ED%8F%AC%EC%8A%A4%ED%84%B0.jpg"},
        {"title": "미안해요, 리키", "info": "드라마 | 감독: 켄 로치", "ott": "왓챠", "reason": "현대 노동 윤리와 가족의 가치 문제를 진지하게 다룹니다.", "image_url": "https://upload.wikimedia.org/wikipedia/en/e/e4/Sorry_We_Missed_You_poster.png"}
    ]
}

# 메인 UI
st.title("🎓 14개 과목별 영화 포스터 & 추천 서비스")
st.write("좋아하는 과목을 선택하면 관련 영화 2편을 포스터와 함께 추천해 드립니다.")
st.markdown("---")

subject = st.selectbox("어떤 과목을 가장 좋아하시나요?", options=list(movie_data.keys()))

if subject:
    st.subheader(f"✨ '{subject}' 과목 추천 리스트")
    movies = movie_data[subject]
    col1, col2 = st.columns(2)
    
    for i, movie in enumerate(movies):
        with [col1, col2][i]:
            with st.container(border=True):
                # 이미지 출력 (try-except로 안정성 확보)
                try:
                    st.image(movie["image_url"], use_container_width=True)
                except:
                    st.warning("🖼️ 포스터를 불러올 수 없습니다.")
                
                st.subheader(movie["title"])
                st.write(f"**ℹ️ 정보:** {movie['info']}")
                st.write(f"**📺 OTT:** :blue[{movie['ott']}]")
                st.info(f"**💡 추천 이유**\n\n{movie['reason']}")

st.markdown("---")
st.caption("정보는 배포 시점 기준이며, 일부 이미지는 저작권 및 네트워크 환경에 따라 표시되지 않을 수 있습니다.")
