import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 페이지 설정
st.set_page_config(page_title="기온 상승 분석기", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")
st.markdown("업로드된 데이터를 바탕으로 장기적인 기온 변화 추세를 확인합니다.")

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    file_name = 'test.py.csv'
    
    # 파일이 없는 경우를 대비한 예외 처리
    if not os.path.exists(file_name):
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. GitHub 레포지토리에 파일이 있는지 확인해주세요.")
        return None

    try:
        # 데이터 읽기 (한글 깨짐 방지 및 따옴표 처리)
        df = pd.read_csv(file_name, encoding='cp949', quotechar='"')
        
        # '날짜' 컬럼의 숨겨진 탭(\t) 기호 제거 및 날짜 형식 변환
        df['날짜'] = df['날짜'].astype(str).str.replace(r'\s+', '', regex=True)
        df['날짜'] = pd.to_datetime(df['날짜'])
        
        # 분석을 위한 '연도' 컬럼 생성
        df['연도'] = df['날짜'].dt.year
        return df
    except Exception as e:
        st.error(f"데이터 읽기 오류: {e}")
        return None

data = load_data()

if data is not None:
    # 3. 데이터 가공 (연도별 평균 기온)
    yearly_avg = data.groupby('연도')['평균기온(℃)'].mean().reset_index()

    # 4. 사이드바 - 분석 기간 선택
    st.sidebar.header("📊 분석 설정")
    min_year = int(yearly_avg['연도'].min())
    max_year = int(yearly_avg['연도'].max())
    
    year_range = st.sidebar.slider(
        "조회 기간을 선택하세요",
        min_year, max_year, (min_year, max_year)
    )

    # 필터링 데이터
    filtered = yearly_avg[(yearly_avg['연도'] >= year_range[0]) & (yearly_avg['연도'] <= year_range[1])]

    # 5. 핵심 지표 표시 (Metric)
    st.subheader(f"📅 {year_range[0]}년 대비 기온 변화")
    
    start_temp = filtered.iloc[0]['평균기온(℃)']
    end_temp = filtered.iloc[-1]['평균기온(℃)']
    diff = end_temp - start_temp

    c1, c2, c3 = st.columns(3)
    c1.metric(f"{year_range[0]}년 평균", f"{start_temp:.2f} ℃")
    c2.metric(f"{year_range[1]}년 평균", f"{end_temp:.2f} ℃")
    c3.metric("기온 상승폭", f"{diff:+.2f} ℃", delta=f"{diff:.2f} ℃")

    # 6. 그래프 시각화 (Matplotlib)
    st.write("---")
    st.subheader("연도별 평균 기온 추이 및 추세선")
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(filtered['연도'], filtered['평균기온(℃)'], color='#ff9999', marker='o', markersize=3, label='연평균 기온')
    
    # 단순 선형 추세선 계산 (기온이 실제로 오르는지 확인용)
    import numpy as np
    z = np.polyfit(filtered['연도'], filtered['평균기온(℃)'], 1)
    p = np.poly1d(z)
    ax.plot(filtered['연도'], p(filtered['연도']), "r--", linewidth=2, label="상승 추세선")

    ax.set_title(f"{year_range[0]}년 - {year_range[1]}년 기온 변화", fontsize=15)
    ax.set_xlabel("연도")
    ax.set_ylabel("평균 기온 (℃)")
    ax.legend()
    ax.grid(True, axis='y', alpha=0.3)
    
    st.pyplot(fig)

    # 7. 데이터 테이블 보기
    with st.expander("상세 데이터 확인"):
        st.dataframe(filtered)
