# 영화 데이터 그래프 도감 1 - 시간
import streamlit as st
import pandas as pd

st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

# plotly가 설치되어 있지 않아도(requirements.txt 미반영 등) 앱이 죽지 않도록
# 안전하게 불러옵니다. 설치돼 있으면 plotly로, 안 돼 있으면 기본 차트로 대체합니다.
try:
    import plotly.express as px
    HAS_PLOTLY = True
except ModuleNotFoundError:
    HAS_PLOTLY = False
    st.warning(
        "plotly 모듈을 찾을 수 없어 기본 선 그래프로 대신 표시합니다. "
        "requirements.txt에 plotly가 들어있는지, 저장소 루트에 있는지 확인한 뒤 "
        "'Manage app > Reboot app'으로 앱을 재부팅해 보세요."
    )

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    # 1년치(365일) 일별 박스오피스 10위권 기록을 불러옵니다.
    df = pd.read_csv(DATA_URL)
    # 여덟 자리 숫자로 된 날짜 열을 진짜 날짜로 바꿉니다.
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

# ── 그래프 1. 영화 하나의 흥행 곡선 ──────────────────────────
st.header("1. 한 영화의 흥행 곡선")

# 드롭다운으로 영화를 고릅니다.
movie_list = sorted(df["영화명"].unique())
movie = st.selectbox("영화를 고르세요", movie_list)

one = df[df["영화명"] == movie].sort_values("날짜")

if HAS_PLOTLY:
    fig = px.line(one, x="날짜", y="일관객", markers=True)
    fig.update_traces(hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra></extra>")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.line_chart(one.set_index("날짜")["일관객"])

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 그래프 2. 일관객 합계 상위 5편 비교 ──────────────────────
st.header("2. 일관객 합계 상위 5편의 흥행 곡선 비교")

# 영화별로 이 기간 일관객을 모두 더해서, 합계가 가장 큰 5편을 고릅니다.
top5_names = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)
top5_df = df[df["영화명"].isin(top5_names)].sort_values("날짜")

if HAS_PLOTLY:
    fig2 = px.line(
        top5_df,
        x="날짜",
        y="일관객",
        color="영화명",
        markers=True,
    )
    fig2.update_traces(
        hovertemplate="날짜 %{x|%Y-%m-%d}<br>관객 %{y:,}명<extra>%{fullData.name}</extra>"
    )
    fig2.update_layout(legend_title_text="영화명 (범례를 눌러 켜고 끌 수 있어요)")
    st.plotly_chart(fig2, use_container_width=True)
else:
    pivot = top5_df.pivot_table(index="날짜", columns="영화명", values="일관객")
    st.line_chart(pivot)

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 그래프 3. 날짜별 10위권 일관객 합계(영역 그래프) ─────────
st.header("3. 날짜별 10위권 전체 관객수 추이")

# 날짜별로 그날 10위권에 든 영화들의 일관객을 모두 더합니다.
daily_total = df.groupby("날짜")["일관객"].sum().reset_index()

# 합계가 가장 컸던 날 3일을 찾습니다.
top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

if HAS_PLOTLY:
    fig3 = px.area(daily_total, x="날짜", y="일관객")
    fig3.update_traces(
        hovertemplate="날짜 %{x|%Y-%m-%d}<br>합계 관객 %{y:,}명<extra></extra>"
    )

    # 최고 3일을 점과 날짜 라벨로 표시합니다.
    fig3.add_scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers+text",
        text=top3_days["날짜"].dt.strftime("%Y-%m-%d"),
        textposition="top center",
        marker=dict(size=10, color="crimson"),
        name="합계 최고 3일",
        hovertemplate="날짜 %{x|%Y-%m-%d}<br>합계 관객 %{y:,}명<extra></extra>",
    )
    fig3.update_layout(yaxis_title="일관객 합계(명)")
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.area_chart(daily_total.set_index("날짜")["일관객"])
    st.write("합계가 가장 컸던 날 3일:", top3_days["날짜"].dt.strftime("%Y-%m-%d").tolist())

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 그래프 4. 누적 일관객 TOP 10 영화(가로 막대) ─────────────
st.header("4. 이 기간 일관객 합계 TOP 10 영화")

movie_stats = (
    df.groupby("영화명")
    .agg(합계일관객=("일관객", "sum"), 등장일수=("일관객", "size"))
    .reset_index()
)
top10_movies = movie_stats.sort_values("합계일관객", ascending=False).head(10)
# 그래프에서 큰 값이 위쪽에 오도록, 오름차순으로 다시 정렬합니다.
top10_movies_sorted = top10_movies.sort_values("합계일관객", ascending=True)

if HAS_PLOTLY:
    fig4 = px.bar(
        top10_movies_sorted,
        x="합계일관객",
        y="영화명",
        orientation="h",
        custom_data=["등장일수"],
    )
    fig4.update_traces(
        hovertemplate=(
            "%{y}<br>합계 일관객 %{x:,}명"
            "<br>10위권에 든 날수 %{customdata[0]}일<extra></extra>"
        )
    )
    fig4.update_layout(xaxis_title="합계 일관객 수(명)", yaxis_title="")
    st.plotly_chart(fig4, use_container_width=True)
else:
    st.bar_chart(top10_movies_sorted.set_index("영화명")["합계일관객"])

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 그래프 5. 월×요일 일관객 합계 히트맵 ─────────────────────
st.header("5. 월 × 요일별 일관객 합계 히트맵")

heat_df = df.copy()
heat_df["월"] = heat_df["날짜"].dt.month
weekday_order_kr = ["월", "화", "수", "목", "금", "토", "일"]
weekday_map = {0: "월", 1: "화", 2: "수", 3: "목", 4: "금", 5: "토", 6: "일"}
heat_df["요일"] = heat_df["날짜"].dt.weekday.map(weekday_map)

pivot_heat = (
    heat_df.groupby(["월", "요일"])["일관객"]
    .sum()
    .reset_index()
    .pivot(index="월", columns="요일", values="일관객")
    .reindex(columns=weekday_order_kr)
    .sort_index()
)

if HAS_PLOTLY:
    fig5 = px.imshow(
        pivot_heat,
        labels=dict(x="요일", y="월", color="일관객 합계"),
        x=pivot_heat.columns,
        y=[f"{m}월" for m in pivot_heat.index],
        color_continuous_scale="Reds",
        aspect="auto",
    )
    fig5.update_traces(
        hovertemplate="%{y} %{x}요일<br>합계 관객 %{z:,}명<extra></extra>"
    )
    st.plotly_chart(fig5, use_container_width=True)
else:
    st.dataframe(pivot_heat)

st.caption("이 그래프로 알 수 있는 것: (한 문장으로 적어 보세요)")

# ── 앞으로 6, 7번째 그래프가 이 아래에 추가됩니다 ──────────
