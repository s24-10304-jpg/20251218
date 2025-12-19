import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 페이지 설정
st.set_page_config(page_title="기온 데이터 분석 앱", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")
st.markdown("업로드된 데이터를 바탕으로 연도별 평균 기온의 변화를 확인합니다.")

# 데이터 불러오기
@st.cache_data
def load_data():
    # 데이터의 날짜 컬럼에 탭(\t) 문자가 포함되어 있어 이를 처리합니다.
    df = pd.read_csv('test.py.csv')
    
    # '날짜' 컬럼의 공백 및 특수문자 제거 후 데이트타임 변환
    df['날짜'] = df['날짜'].str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # '연도' 컬럼 생성
    df['연도'] = df['날짜'].dt.year
    return df

try:
    data = load_data()

    # 1. 연도별 평균 기온 계산
    yearly_avg = data.groupby('연도')['평균기온(℃)'].mean().reset_index()

    # 사이드바 레이아웃
    st.sidebar.header("설정")
    year_range = st.sidebar.slider(
        "분석 기간 선택",
        int(yearly_avg['연도'].min()),
        int(yearly_avg['연도'].max()),
        (int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max()))
    )

    # 필터링 데이터
    filtered_data = yearly_avg[(yearly_avg['연도'] >= year_range[0]) & (yearly_avg['연도'] <= year_range[1])]

    # 메인 화면 지표
    col1, col2 = st.columns(2)
    start_temp = filtered_data.iloc[0]['평균기온(℃)']
    end_temp = filtered_data.iloc[-1]['평균기온(℃)']
    diff = end_temp - start_temp

    col1.metric(f"{year_range[0]}년 평균 기온", f"{start_temp:.2f} ℃")
    col2.metric(f"{year_range[1]}년 평균 기온", f"{end_temp:.2f} ℃", delta=f"{diff:.2f} ℃")

    # 시각화
    st.subheader(f"📅 {year_range[0]}년 ~ {year_range[1]}년 기온 변화 추이")
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(filtered_data['연도'], filtered_data['평균기온(℃)'], marker='o', linestyle='-', color='red', markersize=2)
    ax.set_xlabel("연도")
    ax.set_ylabel("평균 기온 (℃)")
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # 추세선 추가 (간단한 선형 회귀 느낌)
    import numpy as np
    z = np.polyfit(filtered_data['연도'], filtered_data['평균기온(℃)'], 1)
    p = np.poly1d(z)
    ax.plot(filtered_data['연도'], p(filtered_data['연도']), "b--", label="추세선")
    
    ax.legend()
    st.pyplot(fig)

    # 데이터 요약
    with st.expander("데이터 상세보기"):
        st.dataframe(filtered_data)

except FileNotFoundError:
    st.error("파일을 찾을 수 없습니다. 'test.py.csv' 파일이 같은 폴더에 있는지 확인해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
