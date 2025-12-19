import streamlit as st
import pandas as pd
import os

# [1] 반드시 가장 첫 번째 Streamlit 명령어로 위치해야 함 (오류 방지 핵심)
st.set_page_config(
    page_title="MBTI 국가별 분석",
    page_icon="🌏",
    layout="wide"
)

def load_data():
    """데이터 로드 및 예외 처리"""
    file_path = "countries.csv"
    if not os.path.exists(file_path):
        st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")
        return None
    try:
        # 캐시를 사용하지 않고 직접 읽어 안정성 확보
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"❌ 데이터 읽기 오류: {e}")
        return None

def main():
    df = load_data()
    if df is None: return

    st.title("🌏 전 세계 MBTI 성향 분석 대시보드")
    mbti_types = df.columns[1:].tolist()

    # --- 섹션 1: 국가별 분석 ---
    st.header("🔍 국가별 상세 분석")
    selected_country = st.selectbox("국가를 선택하세요", sorted(df['Country'].unique()))
    
    country_data = df[df['Country'] == selected_country].iloc[0, 1:]
    analysis_df = pd.DataFrame({'MBTI': mbti_types, 'Ratio': country_data.values})
    analysis_df = analysis_df.sort_values(by='Ratio', ascending=False)

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(f"📊 {selected_country} 순위")
        st.dataframe(analysis_df.style.format({'Ratio': '{:.2%}'}), hide_index=True)
    with col2:
        st.subheader("분포 차트")
        st.bar_chart(analysis_df.set_index('MBTI'))

    st.divider()

    # --- 섹션 2: 전 세계 평균 ---
    st.header("🌐 전 세계 MBTI 평균")
    avg_data = df[mbti_types].mean().sort_values(ascending=False)
    st.bar_chart(avg_data)

    st.divider()

    # --- 섹션 3: 유형별 TOP 10 및 한국 비교 ---
    st.header("🏆 유형별 상위 국가 & 한국 순위")
    target_mbti = st.selectbox("비교할 MBTI 유형", mbti_types)
    
    top_10 = df[['Country', target_mbti]].sort_values(by=target_mbti, ascending=False).head(10)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader(f"{target_mbti} 상위 10개국")
        st.table(top_10.assign(Ratio=lambda x: x[target_mbti].map("{:.2%}".format)).drop(columns=[target_mbti]))
    
    with c2:
        st.subheader("🇰🇷 한국 데이터")
        korea_data = df[df['Country'].str.contains('Korea', case=False, na=False)]
        if not korea_data.empty:
            k_val = korea_data[target_mbti].values[0]
            rank = (df[target_mbti] > k_val).sum() + 1
            st.metric(f"한국의 {target_mbti} 비율", f"{k_val:.2%}")
            st.write(f"현재 전 세계 **{rank}위**입니다.")
        else:
            st.warning("한국 데이터를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()
