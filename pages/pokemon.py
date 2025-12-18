import streamlit as st

# 페이지 설정
st.set_page_config(page_title="MBTI & 포켓몬 매칭 서비스", page_icon="🐾")

# MBTI-포켓몬 데이터 (딕셔너리로 구현)
# 이미지 URL은 포켓몬 공식 사이트나 신뢰할 수 있는 위키에서 가져오는 것이 좋습니다.
# 여기서는 예시 URL을 사용합니다. 실제 서비스 시에는 안정적인 이미지 호스팅을 고려하세요.
pokemon_data = {
    "ISTJ": {
        "name": "거북왕",
        "reason": "신중하고 책임감이 강하며, 꾸준한 노력으로 목표를 달성하는 모습이 ISTJ와 닮았습니다. 든든한 등껍질처럼 믿음직스럽죠.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/009.png"
    },
    "ISFJ": {
        "name": "이상해꽃",
        "reason": "타인을 돌보고 보호하며, 안정감을 추구하는 성향이 강합니다. 주변을 배려하고 헌신적인 ISFJ의 모습과 일치합니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/003.png"
    },
    "INFJ": {
        "name": "뮤츠",
        "reason": "내면이 복잡하고 깊은 통찰력을 가졌으며, 강한 신념으로 이상을 추구하는 모습이 INFJ와 유사합니다. 신비로운 분위기도 닮았죠.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/150.png"
    },
    "INTJ": {
        "name": "뮤",
        "reason": "지적이고 독립적이며, 전략적으로 사고하는 능력이 뛰어납니다. 새로운 것을 탐구하고 분석하는 INTJ의 특성을 가졌습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/151.png"
    },
    "ISTP": {
        "name": "망나뇽",
        "reason": "독립적이고 실용적이며, 문제 해결 능력이 뛰어납니다. 차분하면서도 필요할 때 엄청난 힘을 발휘하는 ISTP와 닮았습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/149.png"
    },
    "ISFP": {
        "name": "피카츄",
        "reason": "자유롭고 예술적인 감각이 뛰어나며, 현재를 즐기는 성향이 강합니다. 사랑스럽고 순수한 ISFP의 매력을 가졌습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/025.png"
    },
    "INFP": {
        "name": "푸린",
        "reason": "이상적이고 창의적이며, 따뜻한 마음을 지닌 포켓몬입니다. 감성적이고 타인과 깊은 공감을 나누려는 INFP와 비슷합니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/039.png"
    },
    "INTP": {
        "name": "메타몽",
        "reason": "호기심이 많고 분석적이며, 끊임없이 지식을 탐구합니다. 어떤 모습으로든 변할 수 있는 메타몽처럼 유연한 사고를 가졌습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/132.png"
    },
    "ESTP": {
        "name": "리자몽",
        "reason": "에너지가 넘치고 모험심이 강하며, 도전을 즐깁니다. 활발하고 즉흥적인 ESTP의 특성을 잘 보여줍니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/006.png"
    },
    "ESFP": {
        "name": "꼬부기",
        "reason": "밝고 사교적이며, 주변 사람들과 어울리는 것을 좋아합니다. 즐거움을 추구하고 낙천적인 ESFP와 닮았습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/007.png"
    },
    "ENFP": {
        "name": "파이리",
        "reason": "열정적이고 창의적이며, 새로운 아이디어를 끊임없이 탐색합니다. 사람들에게 영감을 주는 ENFP의 특성과 비슷합니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/004.png"
    },
    "ENTP": {
        "name": "팬텀",
        "reason": "재치 있고 논쟁을 즐기며, 기발한 아이디어로 사람들을 놀라게 합니다. 지적이고 재기 발랄한 ENTP와 닮았습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/094.png"
    },
    "ESTJ": {
        "name": "웅이", # 인간 캐릭터로 대체 (딱 맞는 포켓몬이 없어서)
        "reason": "현실적이고 논리적이며, 계획을 세워 목표를 달성하는 리더십이 뛰어납니다. 책임감이 강하고 실용적인 ESTJ의 특징을 가졌습니다.",
        "image_url": "https://archives.bulbagarden.net/media/upload/thumb/f/f6/Brock_OS.png/250px-Brock_OS.png"
    },
    "ESFJ": {
        "name": "럭키",
        "reason": "배려심이 깊고 친절하며, 사람들과의 관계를 중요하게 생각합니다. 주변을 잘 챙기는 ESFJ의 따뜻한 마음과 비슷합니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/113.png"
    },
    "ENFJ": {
        "name": "레쿠쟈",
        "reason": "카리스마 넘치고 통솔력이 뛰어나며, 모두를 이끌어 목표를 향해 나아갑니다. 이상을 추구하며 사람들에게 긍정적인 영향을 주는 ENFJ와 닮았습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/384.png"
    },
    "ENTJ": {
        "name": "그란돈",
        "reason": "결단력 있고 추진력이 강하며, 목표 달성을 위해 모든 것을 계획하고 실행합니다. 타고난 리더십을 가진 ENTJ의 모습과 같습니다.",
        "image_url": "https://assets.pokemon.com/assets/cms2/img/pokedex/full/383.png"
    },
}

# 메인 UI
st.title("🐾 MBTI와 포켓몬의 특별한 만남!")
st.write("당신의 MBTI를 선택하고, 가장 잘 어울리는 포켓몬 친구를 만나보세요!")

# 사용자 선택
selected_mbti = st.selectbox(
    "당신의 MBTI는 무엇인가요?",
    options=list(pokemon_data.keys())
)

if st.button("나의 포켓몬 보기!"):
    st.divider()
    
    match_result = pokemon_data[selected_mbti]
    
    st.subheader(f"🎉 당신의 MBTI '{selected_mbti}'와 닮은 포켓몬은...")
    
    col1, col2 = st.columns([1, 2]) # 이미지와 텍스트 비율 조절
    
    with col1:
        st.image(match_result["image_url"], caption=match_result["name"], use_column_width=True)
    
    with col2:
        st.markdown(f"## {match_result['name']}!")
        st.write("---")
        st.markdown(f"**💖 왜 닮았을까요?**")
        st.info(match_result["reason"])
        
    st.success(f"{selected_mbti} 유형의 당신, {match_result['name']}처럼 멋진 하루 되세요!")
