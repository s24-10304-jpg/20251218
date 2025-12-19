import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="기온 변화 분석", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")

# 2. 파일 경로 자동 추적 (에러 방지 핵심)
# 스트림릿 클라우드 환경에 맞춰 파일 위치를 찾습니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
file_name = 'test.py.csv'
file_path = os.path.join(current_dir, file_name)

# 만약 위 경로에 없다면 현재 작업 디렉토리에서 재시도
if not os.path.exists(file_path):
    file_path = file_name

@st.cache_data
def load_data(path):
    # 인코딩 문제(cp949, utf-8) 자동 처리
    try:
        df = pd.read_csv(path, encoding='utf-8-sig', quotechar='"')
    except:
        df = pd.read_csv(path, encoding='cp949', quotechar='"')
    
    # 날짜 데이터의 탭(\t) 및 공백 제거
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t\s]', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['연도'] = df['날짜'].dt.year
    return df

# 3. 메인 실행 부분
if os.path.exists(file_path):
    try:
        data = load_data(file_path)
        
        # 연도별 평균 기온 계산
        yearly_avg = data.groupby('연도')['평균기온(℃)'].mean().reset_index()

        # 사이드바 설정
        st.sidebar.header("🗓️ 기간 설정")
        min_y, max_y = int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max())
        start_y, end_y = st.sidebar.slider("조회 기간 선택", min_y, max_y, (min_y, max_y))

        # 필터링
        filtered = yearly_avg[(yearly_avg['연도'] >= start_y) & (yearly_avg['연도'] <= end_y)]

        # 결과 지표
        v1 = filtered.iloc[0]['평균기온(℃)']
        v2 = filtered.iloc[-1]['평균기온(℃)']
        
        c1, c2 = st.columns(2)
        c1.metric(f"{start_y}년 평균", f"{v1:.2f} ℃")
        c2.metric(f"{end_y}년 평균", f"{v2:.2f} ℃", delta=f"{v2-v1:.2f} ℃")

        # 4. Plotly 인터랙티브 그래프
        st.subheader("연도별 평균 기온 추이 (Interactive)")
        fig = px.line(filtered, x='연도', y='평균기온(℃)', 
                      labels={'평균기온(℃)': '평균 기온 (℃)', '연도': '연도'},
                      template="plotly_white")
        
        # 추세선 추가
        z = np.polyfit(filtered['연도'], filtered['평균기온(℃)'], 1)
        p = np.poly1d(z)
        fig.add_trace(go.Scatter(x=filtered['연도'], y=p(filtered['연도']),
                                 mode='lines', name='기온 상승 추세',
                                 line=dict(color='red', dash='dash')))
        
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
else:
    # 파일이 없을 때 나오는 경고창
    st.error(f"❌ 파일을 찾을 수 없습니다: {file_name}")
    st.info("""
    **해결 방법:**
    1. GitHub에 접속합니다.
    2. 'Add file' -> 'Upload files'를 누릅니다.
    3. 내 컴퓨터에 있는 'test.py.csv' 파일을 선택해 업로드합니다.
    4. **파일 이름이 정확히 'test.py.csv'인지 확인하세요.**
    """)
