"""
🎲 랜덤 취미 추천 웹앱
취미가 없는 사람들에게 다양한 카테고리의 취미를 랜덤으로 추천해주는 Streamlit 앱
"""

import random
import streamlit as st
import pandas as pd
from hobby_data import HOBBIES, CATEGORIES

# ──────────────────────────────────────────────
# 페이지 설정
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="🎲 랜덤 취미 추천",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
# 커스텀 CSS
# ──────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');

/* ── 전역 스타일 ── */
html, body, [class*="st-"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* ── 헤더 영역 ── */
.hero-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    color: white;
    text-align: center;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
}
.hero-header h1 {
    font-size: 2.2rem;
    font-weight: 900;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.hero-header p {
    font-size: 1rem;
    opacity: 0.9;
    margin: 0;
}

/* ── 추천 카드 ── */
.hobby-card {
    background: linear-gradient(145deg, #ffffff 0%, #f8f9ff 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(102, 126, 234, 0.1);
    margin: 1.5rem 0;
    animation: fadeInUp 0.6s ease-out;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.hobby-card .hobby-emoji {
    font-size: 4rem;
    display: block;
    text-align: center;
    margin-bottom: 0.5rem;
}
.hobby-card .hobby-name {
    font-size: 1.8rem;
    font-weight: 900;
    text-align: center;
    color: #2d3436;
    margin-bottom: 0.3rem;
}

/* ── 카테고리 배지 ── */
.badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    color: white;
}
.badge-창작 { background: #FF6B6B; }
.badge-운동 { background: #4ECDC4; }
.badge-실내 { background: #45B7D1; }
.badge-실외 { background: #96CEB4; }
.badge-사교 { background: #F0932B; }
.badge-학습 { background: #A29BFE; }

/* ── 정보 그리드 ── */
.info-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 1rem 0;
}
.info-item {
    background: #f0f2f6;
    border-radius: 12px;
    padding: 12px 16px;
    text-align: center;
}
.info-item .info-label {
    font-size: 0.75rem;
    color: #636e72;
    margin-bottom: 4px;
}
.info-item .info-value {
    font-size: 1.1rem;
    font-weight: 700;
    color: #2d3436;
}

/* ── 준비물 태그 ── */
.supply-tag {
    display: inline-block;
    background: linear-gradient(135deg, #667eea22, #764ba222);
    border: 1px solid #667eea44;
    color: #5f3dc4;
    padding: 4px 12px;
    border-radius: 8px;
    font-size: 0.85rem;
    margin: 3px 4px 3px 0;
    font-weight: 500;
}

/* ── 관심 목록 카드 ── */
.fav-card {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
    border: 1px solid #eee;
    margin-bottom: 0.8rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.fav-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

/* ── 사이드바 스타일 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8f9ff 0%, #eef0ff 100%);
}

/* ── 빈 상태 메시지 ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: #b2bec3;
}
.empty-state .empty-emoji {
    font-size: 4rem;
    display: block;
    margin-bottom: 1rem;
}

/* ── 메인 추천 버튼 ── */
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 0.8rem 2rem;
    font-size: 1.2rem;
    font-weight: 700;
    border-radius: 14px;
    width: 100%;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}
div.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(102, 126, 234, 0.5);
}

/* ── 탭 스타일 ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 8px 20px;
    font-weight: 600;
}
</style>
""",
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# 세션 상태 초기화
# ──────────────────────────────────────────────
if "favorites" not in st.session_state:
    st.session_state.favorites = []
if "current_hobby" not in st.session_state:
    st.session_state.current_hobby = None
if "recommend_count" not in st.session_state:
    st.session_state.recommend_count = 0


# ──────────────────────────────────────────────
# 유틸 함수
# ──────────────────────────────────────────────
def get_difficulty_stars(level: int) -> str:
    """난이도를 별로 변환"""
    return "⭐" * level + "☆" * (5 - level)


def get_cost_indicator(level: int) -> str:
    """비용을 원화 아이콘으로 변환"""
    return "💰" * level + "•" * (5 - level)


def get_cost_text(level: int) -> str:
    """비용 레벨을 텍스트로 변환"""
    labels = {1: "거의 무료", 2: "저비용", 3: "보통", 4: "고비용", 5: "매우 고비용"}
    return labels.get(level, "")


def get_difficulty_text(level: int) -> str:
    """난이도 레벨을 텍스트로 변환"""
    labels = {1: "매우 쉬움", 2: "쉬움", 3: "보통", 4: "어려움", 5: "매우 어려움"}
    return labels.get(level, "")


def filter_hobbies(
    hobbies: list,
    categories: list,
    diff_range: tuple,
    cost_range: tuple,
    indoor_only: bool,
) -> list:
    """필터 조건에 맞는 취미 목록 반환"""
    filtered = hobbies
    if categories:
        filtered = [h for h in filtered if h["category"] in categories]
    filtered = [
        h for h in filtered if diff_range[0] <= h["difficulty"] <= diff_range[1]
    ]
    filtered = [h for h in filtered if cost_range[0] <= h["cost"] <= cost_range[1]]
    if indoor_only:
        filtered = [h for h in filtered if h["indoor"]]
    return filtered


# ──────────────────────────────────────────────
# 헤더
# ──────────────────────────────────────────────
st.markdown(
    """
<div class="hero-header">
    <h1>🎲 랜덤 취미 추천</h1>
    <p>뭘 해야 할지 모르겠다면? 버튼 하나로 새로운 취미를 발견하세요!</p>
</div>
""",
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
# 사이드바 필터
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 필터 설정")
    st.markdown("---")

    # 카테고리 선택
    all_categories = list(CATEGORIES.keys())
    category_labels = [f"{CATEGORIES[c]['emoji']} {c}" for c in all_categories]
    selected_labels = st.multiselect(
        "카테고리 선택",
        options=category_labels,
        default=[],
        placeholder="전체 카테고리",
    )
    # 라벨에서 카테고리명 추출
    selected_categories = [label.split(" ", 1)[1] for label in selected_labels]

    st.markdown("")

    # 난이도 범위
    diff_range = st.slider(
        "난이도 범위",
        min_value=1,
        max_value=5,
        value=(1, 5),
        format="%d",
        help="1: 매우 쉬움 ~ 5: 매우 어려움",
    )

    # 비용 범위
    cost_range = st.slider(
        "비용 범위",
        min_value=1,
        max_value=5,
        value=(1, 5),
        format="%d",
        help="1: 거의 무료 ~ 5: 매우 고비용",
    )

    st.markdown("")

    # 실내 전용
    indoor_only = st.checkbox("🏠 실내 활동만 보기", value=False)

    st.markdown("---")

    # 필터된 결과 수 표시
    filtered = filter_hobbies(
        HOBBIES, selected_categories, diff_range, cost_range, indoor_only
    )
    st.info(f"🎯 조건에 맞는 취미: **{len(filtered)}개** / 전체 {len(HOBBIES)}개")

# ──────────────────────────────────────────────
# 탭 구성
# ──────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎲 취미 추천", "📋 전체 취미 목록", "⭐ 내 관심 목록"])

# ──────────────────────────────────────────────
# 탭 1: 랜덤 취미 추천
# ──────────────────────────────────────────────
with tab1:
    # 필터링된 취미
    filtered_hobbies = filter_hobbies(
        HOBBIES, selected_categories, diff_range, cost_range, indoor_only
    )

    # 추천 버튼
    col_btn_l, col_btn_c, col_btn_r = st.columns([1, 2, 1])
    with col_btn_c:
        recommend_clicked = st.button(
            "🎲 랜덤 취미 추천받기!",
            type="primary",
            use_container_width=True,
        )

    if recommend_clicked:
        if filtered_hobbies:
            st.session_state.current_hobby = random.choice(filtered_hobbies)
            st.session_state.recommend_count += 1
            if st.session_state.recommend_count % 3 == 0:
                st.balloons()
        else:
            st.warning("😅 조건에 맞는 취미가 없어요! 필터를 조정해보세요.")
            st.session_state.current_hobby = None

    # 추천 결과 표시
    hobby = st.session_state.current_hobby
    if hobby:
        cat_info = CATEGORIES[hobby["category"]]

        # 카드 시작
        st.markdown(
            f"""
        <div class="hobby-card">
            <span class="hobby-emoji">{hobby['emoji']}</span>
            <div class="hobby-name">{hobby['name']}</div>
            <div style="text-align:center; margin: 0.5rem 0;">
                <span class="badge badge-{hobby['category']}">{cat_info['emoji']} {hobby['category']}</span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # 정보 그리드
        st.markdown(
            f"""
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">난이도</div>
                <div class="info-value">{get_difficulty_stars(hobby['difficulty'])}</div>
                <div class="info-label">{get_difficulty_text(hobby['difficulty'])}</div>
            </div>
            <div class="info-item">
                <div class="info-label">비용</div>
                <div class="info-value">{get_cost_indicator(hobby['cost'])}</div>
                <div class="info-label">{get_cost_text(hobby['cost'])}</div>
            </div>
            <div class="info-item">
                <div class="info-label">활동 장소</div>
                <div class="info-value">{'🏠 실내' if hobby['indoor'] else '🌿 실외'}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

        # 설명
        st.markdown(f"### 📝 설명")
        st.write(hobby["description"])

        # 준비물
        st.markdown("### 🛒 필요한 준비물")
        supplies_html = "".join(
            [f'<span class="supply-tag">{s}</span>' for s in hobby["supplies"]]
        )
        st.markdown(supplies_html, unsafe_allow_html=True)

        # 팁
        st.markdown("")
        st.info(f"💡 **팁**: {hobby['tip']}")

        # 액션 버튼들
        col1, col2 = st.columns(2)
        with col1:
            youtube_query = hobby["name"] + " 취미 시작하기"
            youtube_url = f"https://www.youtube.com/results?search_query={youtube_query}"
            st.link_button(
                "▶️ 유튜브에서 검색하기",
                youtube_url,
                use_container_width=True,
            )
        with col2:
            # 관심 목록 추가/제거
            is_fav = hobby["name"] in [f["name"] for f in st.session_state.favorites]
            if is_fav:
                if st.button(
                    "💔 관심 목록에서 제거",
                    use_container_width=True,
                    key="remove_from_recommend",
                ):
                    st.session_state.favorites = [
                        f
                        for f in st.session_state.favorites
                        if f["name"] != hobby["name"]
                    ]
                    st.rerun()
            else:
                if st.button(
                    "⭐ 관심 목록에 추가",
                    use_container_width=True,
                    key="add_from_recommend",
                ):
                    st.session_state.favorites.append(hobby)
                    st.toast(f"⭐ '{hobby['name']}'을(를) 관심 목록에 추가했어요!")
                    st.rerun()

    else:
        # 초기 안내 메시지
        st.markdown(
            """
        <div class="empty-state">
            <span class="empty-emoji">🎯</span>
            <h3>위의 버튼을 눌러 취미를 추천받아 보세요!</h3>
            <p>사이드바에서 필터를 설정하면 더 정확한 추천을 받을 수 있어요.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ──────────────────────────────────────────────
# 탭 2: 전체 취미 목록
# ──────────────────────────────────────────────
with tab2:
    st.markdown("### 📋 전체 취미 데이터")

    # DataFrame 생성
    df = pd.DataFrame(
        [
            {
                "이모지": h["emoji"],
                "취미": h["name"],
                "카테고리": h["category"],
                "난이도": h["difficulty"],
                "비용": h["cost"],
                "실내": "✅" if h["indoor"] else "❌",
                "설명": h["description"],
            }
            for h in HOBBIES
        ]
    )

    # 검색 기능
    search = st.text_input("🔍 취미 검색", placeholder="취미 이름이나 설명을 검색하세요...")
    if search:
        mask = df["취미"].str.contains(search, case=False) | df["설명"].str.contains(
            search, case=False
        )
        df_display = df[mask]
    else:
        df_display = df

    st.dataframe(
        df_display,
        use_container_width=True,
        height=400,
        hide_index=True,
        column_config={
            "난이도": st.column_config.ProgressColumn(
                "난이도", min_value=0, max_value=5, format="%d"
            ),
            "비용": st.column_config.ProgressColumn(
                "비용", min_value=0, max_value=5, format="%d"
            ),
        },
    )

    st.markdown(f"총 **{len(df_display)}개** 취미 표시 중")

    st.markdown("---")

    # 차트 영역
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("### 📊 카테고리별 취미 수")
        cat_counts = (
            pd.DataFrame(HOBBIES)[["category"]]
            .value_counts()
            .reset_index()
        )
        cat_counts.columns = ["카테고리", "수"]
        st.bar_chart(cat_counts, x="카테고리", y="수", color="#667eea", horizontal=True)

    with chart_col2:
        st.markdown("### 📈 난이도 vs 비용 분포")
        scatter_df = pd.DataFrame(
            [
                {
                    "취미": h["name"],
                    "난이도": h["difficulty"],
                    "비용": h["cost"],
                    "카테고리": h["category"],
                }
                for h in HOBBIES
            ]
        )
        st.scatter_chart(
            scatter_df,
            x="난이도",
            y="비용",
            color="카테고리",
            size=80,
        )

# ──────────────────────────────────────────────
# 탭 3: 관심 목록
# ──────────────────────────────────────────────
with tab3:
    st.markdown("### ⭐ 내 관심 목록")

    if not st.session_state.favorites:
        st.markdown(
            """
        <div class="empty-state">
            <span class="empty-emoji">📭</span>
            <h3>아직 관심 목록이 비어있어요</h3>
            <p>취미 추천에서 마음에 드는 취미를 ⭐ 추가해보세요!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.success(f"총 **{len(st.session_state.favorites)}개**의 취미를 저장했어요!")
        st.markdown("")

        for i, fav in enumerate(st.session_state.favorites):
            cat_info = CATEGORIES[fav["category"]]
            with st.container():
                col_info, col_action = st.columns([5, 1])
                with col_info:
                    st.markdown(
                        f"""
                    <div class="fav-card">
                        <div style="display:flex; align-items:center; gap:12px;">
                            <span style="font-size:2rem;">{fav['emoji']}</span>
                            <div>
                                <strong style="font-size:1.1rem;">{fav['name']}</strong>
                                <span class="badge badge-{fav['category']}" style="margin-left:8px; font-size:0.75rem;">{cat_info['emoji']} {fav['category']}</span>
                                <br/>
                                <span style="color:#636e72; font-size:0.85rem;">
                                    난이도 {get_difficulty_stars(fav['difficulty'])} · 비용 {get_cost_indicator(fav['cost'])}
                                </span>
                            </div>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
                with col_action:
                    st.markdown("<br/>", unsafe_allow_html=True)
                    if st.button("🗑️", key=f"del_{i}", help="관심 목록에서 삭제"):
                        removed_name = st.session_state.favorites[i]["name"]
                        st.session_state.favorites.pop(i)
                        st.toast(f"🗑️ '{removed_name}'을(를) 삭제했어요.")
                        st.rerun()

        st.markdown("---")
        if st.button("🗑️ 관심 목록 전체 비우기", type="secondary"):
            st.session_state.favorites = []
            st.rerun()

# ──────────────────────────────────────────────
# 푸터
# ──────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
<div style="text-align:center; color:#b2bec3; font-size:0.8rem; padding: 1rem 0;">
    🎲 랜덤 취미 추천 · Made with Streamlit ❤️ · 데이터는 참고용이며, 실제 비용은 다를 수 있습니다.
</div>
""",
    unsafe_allow_html=True,
)
