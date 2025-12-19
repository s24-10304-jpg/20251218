import streamlit as st
import pandas as pd
import os

# [중요] 모든 Streamlit 명령 중 가장 처음에 실행되어야 합니다.
st.set_page_config(
    page_title="Global MBTI Analysis",
    page_icon="🌏",
    layout="wide"
)

def load_data():
    file_path = "countries.csv"
    if not os.path.exists(file_path):
        st.error(f"⚠️ '{file_path}' 파일을 찾을 수 없습니다. 같은 폴더에 업로드했는지 확인해주세요.")
        return None
    
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        st.error(f"⚠️ 데이터를 읽는 중 오류가 발생했습니다: {e}")
        return None

def main():
    st.title("🌏 전 세계 MBTI 성향 분석 대시보드")
    
    df = load_data()
    if df is None:
        return

    # 데이터 정리 (MBTI 컬럼만 추출)
    mbti_cols = df.columns[1:]

    # --- 섹션 1: 국가별 분석 ---
    st.header("🔍 국가별 MBTI 조회")
    countries = df['Country'].unique()
    selected_country = st.selectbox("분석할 국가를 선택하세요:", sorted(countries))
    
    c_data = df[df['Country'] == selected_
