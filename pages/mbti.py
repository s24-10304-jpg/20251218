import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI 진로 추천 서비스", page_icon="📚")

# MBTI 데이터 사전 (별도 DB 없이 딕셔너리로 구현)
mbti_data = {
    "ISTJ": {"jobs": ["회계사", "공무원"], "book": "아주 작은 습관의 힘 (제임스 클리어)"},
    "ISFJ": {"jobs": ["간호사", "초등교사"], "book": "나를 사랑하는 법 (나태주)"},
    "INFJ": {"jobs": ["상담심리사", "작가"], "book": "데미안 (헤르만 헤세)"},
    "INTJ": {"jobs": ["전략 기획가", "데이터 과학자"], "book": "이기적 유전자 (리처드 도킨스)"},
    "ISTP": {"jobs": ["엔지니어", "파일럿"], "book": "월든 (헨리 데이비드 소로)"},
    "ISFP": {"jobs": ["디자이너", "작곡가"], "book": "빨강머리 앤 (루시 모드 몽고메리)"},
    "INFP": {"jobs": ["예술가", "NGO 활동가"], "book": "어린 왕자 (생텍쥐페리)"},
    "INTP": {"jobs": ["소프트웨어 개발자", "철학자"], "book": "사피엔스 (유발 하라리)"},
    "ESTP": {"jobs": ["기업가", "스포츠 매니저"], "book": "백만장자 시크릿 (T. 하브 에커)"},
    "ESFP": {"jobs": ["연예인", "홍보 전문가"], "book": "긍정의 힘 (조엘 오스틴)"},
    "ENFP": {"jobs": ["마케터", "이벤트 기획자"], "book": "연금술사 (파울로 코엘료)"},
    "ENTP": {"jobs": ["변호사", "광고 제작자"], "book": "생각에 관한 생각 (대니얼 카너먼)"},
    "ESTJ": {"jobs": ["경영자", "군 장교"], "book": "원칙 (레이 달리오)"},
    "ESFJ": {"jobs": ["호텔리어", "사회복지사"], "book": "인간관계론 (데일 카네기)"},
    "ENFJ": {"jobs": ["정치인", "교사"], "book": "정의란 무엇인가 (마이클 샌델)"},
    "ENTJ": {"jobs": ["CEO", "경제 분석가"], "book": "손자병법 (손무)"},
}

# 메인 UI
st.title("✨ MBTI 맞춤 진로 & 도서 추천")
st.write("당신의 MBTI를 선택하면 가장 잘 어울리는 진로와 책을 추천해 드립니다.")

# 사용자 선택
selected_mbti = st.selectbox(
    "당신의 MBTI는 무엇인가요?",
    options=list(mbti_data.keys())
)

if st.button("추천 결과 보기"):
    result = mbti_data[selected_mbti]
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 추천 진로")
        for job in result["jobs"]:
            st.write(f"- {job}")
            
    with col2:
        st.subheader("📖 추천 도서")
        st.info(result["book"])
        
    st.success(f"{selected_mbti} 유형인 당신의 미래를 응원합니다!")
