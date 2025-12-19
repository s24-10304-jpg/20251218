import streamlit as st
import pandas as pd

# 1. 페이지 설정 (가장 상단에 위치)
st.set_page_config(page_title="기온 변화 분석", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")
st.info("별도의 라이브러리 설치 없이 스트림릿 내장 차트 기능을 사용하여 안전하게 실행됩니다.")

# 2. 데이터 불러오기 함수
@st.cache_data
def load_data():
    # 파일 인코딩 및 데이터 구조 대응
    try:
        # 한국어 데이터 특성상 cp949 인코딩을 우선 시도합니다.
        df = pd.read_csv('test.py.csv', encoding='cp949')
    except:
        df = pd.read_csv('test.py.csv', encoding='utf-8')
    
    # '날짜' 컬럼의 탭(\t) 문자 및 불필요한 공백 제거
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t\s]', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'])
    
    # 연도 컬럼 추출
    df['연도'] = df['날짜'].dt.year
    return df

try:
    # 데이터 로드
    df = load_data()
    
    # 3. 데이터 분석 (연도별 평균 기온 계산)
    # 데이터에서 '평균기온(℃)' 컬럼을 사용합니다.
    yearly_avg = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
    
    # 4. 사이드바 기간 선택 슬라이더
    st.sidebar.header("조회 범위 설정")
    min_year = int(yearly_avg['연도'].min())
    max_year = int(yearly_avg['연vear'].max())
    
    selected_years = st.sidebar.slider(
        "분석할 연도를 선택하세요",
        min_year, max_year, (min_year, max_year)
    )
    
    # 필터링
    filtered_df = yearly_avg[
        (yearly_avg['연도'] >= selected_years[0]) & 
        (yearly_avg['연도'] <= selected_years[1])
    ]

    # 5. 주요 지표 표시
    col1, col2, col3 = st.columns(3)
    start_temp = filtered_df.iloc[0]['평균기온(℃)']
    end_temp = filtered_df.iloc[-1]['평균기온(℃)']
    diff = end_temp - start_temp

    col1.metric(f"{selected_years[0]}년 기온", f"{start_temp:.2f} ℃")
    col2.metric(f"{selected_years[1]}년 기온", f"{end_temp:.2f} ℃")
    col3.metric("기온 변화폭", f"{diff:+.2f} ℃", delta=f"{diff:.2f} ℃")

    # 6. 시각화 (matplotlib 대신 스트림릿 내장 차트 사용)
    st.subheader(f"📅 {selected_years[0]}년 - {selected_years[1]}년 평균 기온 변화")
    
    # 차트용 데이터 정렬
    chart_data = filtered_df.set_index('연도')[['평균기온(℃)']]
    st.line_chart(chart_data)

    # 7. 데이터 보기
    with st.expander("원본 통계 데이터 확인"):
        st.write(filtered_df)

except Exception as e:
    st.error(f"데이터를 처리하는 중 오류가 발생했습니다: {e}")
    st.write("파일 이름이 'test.py.csv'이고 앱과 같은 폴더에 있는지 확인해주세요.")
