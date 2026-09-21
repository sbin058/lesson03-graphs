import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------------
# 기본 설정
# ----------------------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")
    # 날짜 열(예: 20250901)을 진짜 날짜 타입으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

st.caption(
    "일별 박스오피스 10위권 데이터(약 1년치)를 다양한 그래프로 살펴봅니다. "
    "이 페이지는 '시간'을 기준으로 한 그래프들을 모아 둔 도감입니다."
)

# ============================================================================
# 구역 1. 영화별 일관객 수 변화 (날짜에 따른 선 그래프)
# ============================================================================
st.header("1. 영화별 일별 관객수 변화")

movie_list = sorted(df["영화명"].dropna().unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .loc[:, ["날짜", "일관객"]]
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객수 변화",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(xaxis_title="날짜", yaxis_title="일관객 수(명)")

st.plotly_chart(fig1, use_container_width=True)

st.markdown("**이 그래프로 알 수 있는 것:**")
st.info("(여기에 이 그래프에서 발견한 내용을 한 문장으로 적어보세요.)")

# ============================================================================
# 구역 2. (다음 그래프 추가 예정)
# ============================================================================
st.header("2. 다음 그래프 자리")
st.write("앞으로 추가할 시간 기준 그래프가 여기에 들어갑니다.")

# ============================================================================
# 구역 3. (다음 그래프 추가 예정)
# ============================================================================
st.header("3. 다음 그래프 자리")
st.write("앞으로 추가할 시간 기준 그래프가 여기에 들어갑니다.")
