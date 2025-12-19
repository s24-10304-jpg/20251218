import streamlit as st
import pandas as pd
import os

# 1. 페이지 설정
st.set_page_config(page_title="기온 분석 앱", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")

# 2. 파일 경로 찾기 (현재 실행 중인 파일의 폴더 내에서 검색)
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'test.py.csv')

# 만약 위 경로에 없다면 현재 작업 디렉토리에서 재시도
if not os.path.exists(file_path):
    file_path = 'test.py.csv'

# 3. 데이터 로드 및 전처리
@st.cache_data
def load_data(path):
    # 다양한 인코딩 시도 (한글 깨짐 방지)
    try:
        df = pd.read_csv(path, encoding='cp949')
    except:
        df = pd.read_csv(path, encoding='utf-8-sig')
    
    # '날짜' 컬럼의 숨겨진 탭(\t)과 따옴표 제거
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t\s"]', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['연도'] = df['날짜'].dt.year
    return df

# 파일 존재 여부 최종 확인 후 실행
if os.path.exists(file_path):
    try:
        data = load_data(file_path)
        
        # 연도별 평균 기온 계산
        yearly_avg = data.groupby('연도')['평균기온(℃)'].mean().reset_index()

        # 사이드바 기간 선택
        st.sidebar.header("🗓️ 기간 설정")
        min_y, max_y = int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max())
        start_y, end_y = st.sidebar.slider("분석 기간", min_y, max_y, (min_y, max_y))

        # 데이터 필터링
        filtered = yearly_avg[(yearly_avg['연도'] >= start_y) & (yearly_avg['연도'] <= end_y)]

        # 메인 지표
        v1 = filtered.iloc[0]['평균기온(℃)']
        v2 = filtered.iloc[-1]['평균기온(℃)']
        
        c1, c2 = st.columns(2)
        c1.metric(f"{start_y}년 평균", f"{v1:.2f} ℃")
        c2.metric(f"{end_y}년 평균", f"{v2:.2f} ℃", delta=f"{v2-v1:.2f} ℃")

        # 시각화 (추가 설치 불필요)
        st.subheader("연도별 평균 기온 변화")
        st.line_chart(filtered.set_index('연도')['평균기온(℃)'])

    except Exception as e:
        st.error(f"데이터를 읽는 중 오류가 발생했습니다: {e}")
else:
    st.error(f"⚠️ '{file_path}' 파일을 찾을 수 없습니다.")
    st.info("해결 방법: GitHub 레포지토리에 'test.py.csv' 파일이 'app.py'와 같은 위치에 있는지 확인해 주세요.")
