import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# 1. 페이지 설정
st.set_page_config(page_title="기온 변화 분석기", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석 (Interactive)")
st.markdown("Plotly를 사용하여 기간을 자유롭게 확대/축소하며 기온 변화를 확인할 수 있습니다.")

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    file_name = 'test.py.csv'
    if not os.path.exists(file_name):
        return None

    try:
        # 인코딩 문제 해결을 위해 utf-8-sig와 cp949 차례로 시도
        try:
            df = pd.read_csv(file_name, encoding='utf-8-sig', quotechar='"')
        except:
            df = pd.read_csv(file_name, encoding='cp949', quotechar='"')
        
        # 날짜 컬럼의 탭(\t) 및 공백 제거 후 데이트타임 변환
        df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t\s]', '', regex=True)
        df['날짜'] = pd.to_datetime(df['날짜'])
        
        # 연도 컬럼 생성
        df['연도'] = df['날짜'].dt.year
        return df
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return None

df = load_data()

if df is not None:
    # 3. 데이터 가공 (연도별 평균 기온)
    yearly_avg = df.groupby('연도')['평균기온(℃)'].mean().reset_index()

    # 4. 사이드바 - 기간 선택
    st.sidebar.header("📊 분석 설정")
    min_year, max_year = int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max())
    year_range = st.sidebar.slider("조회 기간 선택", min_year, max_year, (min_year, max_year))

    # 필터링
    filtered = yearly_avg[(yearly_avg['연도'] >= year_range[0]) & (yearly_avg['연도'] <= year_range[1])]

    # 5. 주요 지표 표시 (Metric)
    start_temp = filtered.iloc[0]['평균기온(℃)']
    end_temp = filtered.iloc[-1]['평균기온(℃)']
    diff = end_temp - start_temp

    c1, c2, c3 = st.columns(3)
    c1.metric(f"{year_range[0]}년 평균", f"{start_temp:.2f} ℃")
    c2.metric(f"{year_range[1]}년 평균", f"{end_temp:.2f} ℃")
    c3.metric("기온 변화폭", f"{diff:+.2f} ℃", delta=f"{diff:.2f} ℃")

    # 6. Plotly 인터랙티브 시각화
    st.subheader(f"📈 {year_range[0]}년 ~ {year_range[1]}년 기온 변화 추세")
    
    fig = px.line(filtered, x='연도', y='평균기온(℃)', 
                  title="연도별 평균 기온 변화 (마우스를 올려 확인하세요)",
                  labels={'평균기온(℃)': '평균 기온 (℃)', '연도': '연도'},
                  template="plotly_white")

    # 추세선 추가 (Linear Regression Trend)
    import numpy as np
    z = np.polyfit(filtered['연도'], filtered['평균기온(℃)'], 1)
    p = np.poly1d(z)
    
    fig.add_trace(go.Scatter(x=filtered['연도'], y=p(filtered['연도']),
                             mode='lines', name='상승 추세선',
                             line=dict(color='red', dash='dash')))

    # 인터랙티브 설정 (줌, 툴팁 등)
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # 7. 데이터 테이블
    with st.expander("상세 데이터 보기"):
        st.dataframe(filtered)

else:
    st.error("파일 'test.py.csv'를 찾을 수 없습니다. GitHub의 같은 폴더에 파일을 업로드해주세요.")
