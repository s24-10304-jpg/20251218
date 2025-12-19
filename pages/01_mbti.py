import streamlit as st
import pandas as pd
import os

# [필수] 모든 Streamlit 명령 중 가장 첫 줄에 위치해야 합니다. (주석/임포트 제외)
st.set_page_config(
    page_title="Global MBTI Analysis",
    page_icon="🌏",
    layout="wide"
)

def load_data():
    """데이터 파일을 로드하는 함수"""
    file_name = "countries.csv"
    if not os.path.exists(file_name):
        st.error(f"❌ 파일을 찾을 수 없습니다: {file_name}")
        st.info("데이터 파일이 파이썬 코드와 같은 폴더에 있는지 확인해주세요.")
        return None
    try:
        df = pd.read_csv(file_name)
        return df
    except Exception as e:
        st.error(f"❌ 데이터 로딩 오류: {e}")
        return None

def main():
    st.title("🌏 전 세계 MBTI 성향 분석 대시보드")
    
    df = load_data()
    if df is None:
        return

    # MBTI 컬럼 이름들 (첫 번째 컬럼인 'Country' 제외)
    mbti_columns = df.columns[1:].tolist()

    # ---------------------------------------------------------
    # 1. 국가별 MBTI 성향 분석
    # ---------------------------------------------------------
    st.header("🔍 국가별 MBTI 상세 조회")
    all_countries = sorted(df['Country'].unique())
    selected_country = st.selectbox("분석할 국가를 선택하세요:", all_countries)
    
    country_row = df[df['Country'] == selected_country].iloc[0]
    # 데이터를 보기 좋게 변환
    country_mbti = pd.DataFrame({
        'MBTI 유형': mbti_columns,
        '비율': country_row[mbti_columns].values
    }).sort_values(by='비율', ascending=False)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"📊 {selected_country} 내 비중 순위")
        st.dataframe(
            country_mbti.style.format({'비율': '{:.2%}'}),
            hide_index=True,
            use_container_width=True
        )
    with col2:
        st.subheader("분포 차트")
        st.bar_chart(country_mbti.set_index('MBTI 유형'))

    st.divider()

    # ---------------------------------------------------------
    # 2. 전체 국가의 MBTI 평균 비율
    # ---------------------------------------------------------
    st.header("🌐 전 세계 MBTI 평균 분포")
    global_avg = df[mbti_columns].mean().sort_values(ascending=False)
    
    st.bar_chart(global_avg)
    
    # 주요 지표 표시 (상위 4개)
    m_cols = st.columns(4)
    for i in range(4):
        m_cols[i].metric(global_avg.index[i], f"{global_avg.values[i]:.2%}", "Global Avg")

    st.divider()

    # ---------------------------------------------------------
    # 3. MBTI 유형별 TOP 10 & 한국 비교
    # ---------------------------------------------------------
    st.header("🏆 MBTI 유형별 국가 순위 및 한국 비교")
    target_type = st.selectbox("비교할 MBTI 유형을 선택하세요:", mbti_columns)
    
    # 상위 10개국 추출
    top_10 = df[['Country', target_type]].sort_values(by=target_type, ascending=False).head(10)
    
    # 한국(Korea) 데이터 찾기
    korea_df = df[df['Country'].str.contains('Korea', case=False, na=False)]
    
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.subheader(f"{target_type} 비율 상위 10개국")
        # 출력용 데이터프레임 가공
        display_top_10 = top_10.copy()
        display_top_10[target_type] = display_top_10[target_type].map('{:.2%}'.format)
        st.table(display_top_10.reset_index(drop=True))

    with t_col2:
        st.subheader("🇰🇷 대한민국의 위치")
        if not korea_df.empty:
            k_name = korea_df['Country'].values[0]
            k_val = korea_df[target_type].values[0]
            # 순위 계산
            rank = (df[target_type] > k_val).sum() + 1
            total_countries = len(df)
            
            st.metric(label=f"{k_name}의 {target_type} 비율", value=f"{k_val:.2%}")
            st.write(f"현재 이 유형은 전체 {total_countries}개국 중 **{rank}위**입니다.")
            
            # 간단한 비교 게이지 (진척도 바 활용)
            st.progress(k_val / df[target_type].max())
            st.caption(f"최고 국가({top_10.iloc[0]['Country']}) 대비 상대적 비중")
        else:
            st.warning("데이터셋에서 'Korea' 관련 국가명을 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
