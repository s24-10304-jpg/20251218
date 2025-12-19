import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 페이지 설정
st.set_page_config(page_title="기온 변화 분석", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")

# 2. 파일 경로 설정 (절대 경로 추적)
# 현재 실행 중인 파일(app.py)의 폴더 위치를 찾습니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, 'test.py.csv')

# 만약 위 경로에 없다면 현재 작업 폴더에서 다시 시도
if not os.path.exists(file_path):
    file_path = 'test.py.csv'

@st.cache_data
def load_data(path):
    try:
        # 데이터 로드 (cp949 인코딩 및 따옴표 처리)
        df = pd.read_csv(path, encoding='cp949', quotechar='"')
        
        # 날짜 데이터의 탭(\t) 제거 및 변환
        df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
        df['날짜'] = pd.to_datetime(df['날짜'])
        df['연도'] = df['날짜'].dt.year
        return df
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return None

# 3. 메인 로직
if os.path.exists(file_path):
    df = load_data(file_path)
    if df is not None:
        # 연도별 평균 계산
        yearly_avg = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
        
        # 슬라이더
        min_y, max_y = int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max())
        start_y, end_y = st.sidebar.slider("조회 기간", min_y, max_y, (min_y, max_y))
        
        filtered = yearly_avg[(yearly_avg['연도'] >= start_y) & (yearly_avg['연도'] <= end_y)]
        
        # 지표 출력
        v1 = filtered.iloc[0]['평균기온(℃)']
        v2 = filtered.iloc[-1]['평균기온(℃)']
        st.metric(f"{start_y}년 대비 {end_y}년 기온 변화", f"{v2:.2f} ℃", f"{v2-v1:+.2f} ℃")
        
        # 그래프
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(filtered['연도'], filtered['평균기온(℃)'], color='red')
        ax.set_title("Annual Average Temperature Trend")
        ax.set_xlabel("Year")
        ax.set_ylabel("Temp (℃)")
        st.pyplot(fig)
else:
    st.error(f"❌ '{file_path}' 파일을 찾을 수 없습니다.")
    st.warning("GitHub에 'test.py.csv' 파일이 업로드 되었는지 확인해 주세요. 파일명이 정확해야 합니다.")
