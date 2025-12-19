import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="기온 변화 분석", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")

# 파일 경로 설정 (현재 폴더의 파일을 찾음)
file_name = 'test.py.csv'

# 2. 파일 존재 여부 확인 및 데이터 로드
if not os.path.exists(file_name):
    st.error(f"❌ 파일을 찾을 수 없습니다: '{file_name}'")
    st.info("파일이 GitHub 레포지토리에 업로드되었는지, 그리고 파일명이 정확히 'test.py.csv'인지 확인해주세요.")
else:
    @st.cache_data
    def load_data():
        # 데이터가 따옴표로 감싸여 있고 탭(\t) 문자가 포함된 경우를 처리
        # 한글 깨짐 방지를 위해 cp949 인코딩 사용
        df = pd.read_csv(file_name, encoding='cp949', quotechar='"')
        
        # '날짜' 컬럼 내의 탭(\t) 기호와 불필요한 공백 완벽 제거
        df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
        df['날짜'] = pd.to_datetime(df['날짜'])
        
        # 연도 컬럼 생성
        df['연도'] = df['날짜'].dt.year
        return df

    try:
        data = load_data()
        
        # 연도별 평균 기온 계산
        yearly_avg = data.groupby('연도')['평균기온(℃)'].mean().reset_index()

        # 3. 사이드바 기간 설정
        st.sidebar.header("분석 설정")
        min_y, max_y = int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max())
        year_range = st.sidebar.slider("조회 기간 선택", min_y, max_y, (min_y, max_y))

        # 데이터 필터링
        filtered = yearly_avg[(yearly_avg['연도'] >= year_range[0]) & (yearly_avg['연도'] <= year_range[1])]

        # 4. 결과 지표 표시
        start_t = filtered.iloc[0]['평균기온(℃)']
        end_t = filtered.iloc[-1]['평균기온(℃)']
        
        col1, col2 = st.columns(2)
        col1.metric(f"{year_range[0]}년 평균 기온", f"{start_t:.2f} ℃")
        col2.metric(f"{year_range[1]}년 평균 기온", f"{end_t:.2f} ℃", delta=f"{end_t - start_t:.2f} ℃")

        # 5. 시각화 (추가 설치가 필요 없는 내장 차트 사용)
        st.subheader("연도별 평균 기온 추이")
        st.line_chart(filtered.set_index('연도')['평균기온(℃)'])

        # 데이터 테이블
        with st.expander("상세 데이터 보기"):
            st.dataframe(filtered)

    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
