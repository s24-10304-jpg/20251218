import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="Global MBTI Analysis", layout="wide")

@st.cache_data
def load_data():
    # 동일 폴더에 있는 countries.csv 로드
    df = pd.read_csv("countries.csv")
    return df

try:
    df = load_data()
    
    st.title("🌏 전 세계 MBTI 성향 분석 대시보드")
    st.markdown("`countries.csv` 데이터를 기반으로 한 국가별 MBTI 분포 분석입니다.")
    
    # 1. 국가별 MBTI 성향 분석
    st.header("🔍 국가별 MBTI 조회")
    countries = df['Country'].unique()
    selected_country = st.selectbox("분석할 국가를 선택하세요:", countries)
    
    country_data = df[df['Country'] == selected_country].iloc[:, 1:].T
    country_data.columns = ['비율']
    country_data = country_data.sort_values(by='비율', ascending=False)
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"{selected_country}의 성향 순위")
        st.dataframe(country_data.style.format("{:.2%}"))
    
    with col2:
        st.subheader(f"{selected_country} MBTI 분포 차트")
        st.bar_chart(country_data)

    st.divider()

    # 2. 전체 국가의 MBTI 평균 비율
    st.header("📊 전 세계 MBTI 평균 비율")
    avg_mbti = df.iloc[:, 1:].mean().sort_values(ascending=False)
    
    st.write("모든 국가의 데이터를 합산하여 계산한 평균 분포입니다.")
    st.bar_chart(avg_mbti)
    
    cols = st.columns(4)
    for i, (mbti, val) in enumerate(avg_mbti.items()):
        cols[i % 4].metric(mbti, f"{val:.2%}")

    st.divider()

    # 3. MBTI 유형별 TOP 10 국가 & 한국 비교
    st.header("🏆 MBTI 유형별 상위 국가 TOP 10")
    mbti_types = df.columns[1:]
    selected_type = st.selectbox("확인하고 싶은 MBTI 유형을 선택하세요:", mbti_types)
    
    top_10 = df[['Country', selected_type]].sort_values(by=selected_type, ascending=False).head(10)
    
    # 한국 데이터 추출 (데이터에 'South Korea' 또는 'Korea, South' 등으로 존재할 수 있음)
    korea_data = df[df['Country'].str.contains('Korea', case=False)]
    
    st.subheader(f"{selected_type} 비율이 가장 높은 국가")
    st.table(top_10.assign(비율=lambda x: x[selected_type].map("{:.2%}".format)).drop(columns=[selected_type]))

    if not korea_data.empty:
        k_val = korea_data[selected_type].values[0]
        k_name = korea_data['Country'].values[0]
        rank = (df[selected_type] > k_val).sum() + 1
        
        st.info(f"🇰🇷 **{k_name}**의 {selected_type} 비율은 **{k_val:.2%}**이며, 전 세계 **{rank}위**입니다.")
    else:
        st.warning("데이터에서 한국(Korea) 정보를 찾을 수 없습니다.")

except FileNotFoundError:
    st.error("`countries.csv` 파일을 찾을 수 없습니다. 파이썬 파일과 같은 폴더에 업로드해주세요.")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
