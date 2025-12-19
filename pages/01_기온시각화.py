import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. 페이지 설정
st.set_page_config(page_title="기온 변화 분석", layout="wide")

st.title("🌡️ 지난 110년 기온 상승 분석")

# 2. 파일 경로 설정
# 현재 폴더, 혹은 부모 폴더까지 뒤져서 파일을 찾습니다.
file_name = 'test.py.csv'
possible_paths = [
    file_name,
    os.path.join(os.getcwd(), file_name),
    os.path.join(os.path.dirname(__file__), file_name) if '__file__' in locals() else file_name
]

file_path = None
for path in possible_paths:
    if os.path.exists(path):
        file_path = path
        break

@st.cache_data
def load_data(path):
    # 인코딩 에러(cp949) 해결을 위해 시도 순서 변경
    try:
        # 1순위: UTF-8 (최근 가장 많이 쓰임)
        df = pd.read_csv(path, encoding='utf-8', quotechar='"')
    except UnicodeDecodeError:
        try:
            # 2순위: CP949 (한글 윈도우 표준)
            df = pd.read_csv(path, encoding='cp949', quotechar='"')
        except UnicodeDecodeError:
            # 3순위: UTF-8-SIG (엑셀에서 저장한 한글 CSV)
            df = pd.read_csv(path, encoding='utf-8-sig', quotechar='"')
    
    # '날짜' 컬럼의 숨겨진 특수문자(\t)와 공백 제거
    df['날짜'] = df['날짜'].astype(str).str.replace(r'[\t\s"]', '', regex=True)
    df['날짜'] = pd.to_datetime(df['날짜'])
    df['연도'] = df['날짜'].dt.year
    return df

# 3. 메인 실행 부분
if file_path:
    try:
        df = load_data(file_path)
        
        # 연도별 평균 기온 계산
        yearly_avg = df.groupby('연도')['평균기온(℃)'].mean().reset_index()
        
        # 사이드바 설정
        st.sidebar.header("🗓️ 기간 설정")
        min_y, max_y = int(yearly_avg['연도'].min()), int(yearly_avg['연도'].max())
        start_y, end_y = st.sidebar.slider("조회 기간", min_y, max_y, (min_y, max_y))
        
        # 데이터 필터링
        filtered = yearly_avg[(yearly_avg['연도'] >= start_y) & (yearly_avg['연도'] <= end_y)]
        
        # 지표 출력
        v1 = filtered.iloc[0]['평균기온(℃)']
        v2 = filtered.iloc[-1]['평균기온(℃)']
        
        c1, c2 = st.columns(2)
        c1.metric(f"{start_y}년 평균", f"{v1:.2f} ℃")
        c2.metric(f"{end_y}년 평균", f"{v2:.2f} ℃", delta=f"{v2-v1:.2f} ℃")
        
        # 그래프 그리기
        st.subheader(f"📈 {start_y}년~{end_y}년 기온 변화 추이")
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(filtered['연도'], filtered['평균기온(℃)'], color='orange', linewidth=2)
        ax.set_xlabel("Year")
        ax.set_ylabel("Temp (C)")
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"데이터 처리 중 오류 발생: {e}")
else:
    st.error(f"❌ '{file_name}' 파일을 찾을 수 없습니다.")
    st.info("GitHub 레포지토리에 파일이 app.py와 같은 폴더에 업로드되어 있는지 확인해주세요.")
