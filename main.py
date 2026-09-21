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

# ── 앞으로 그래프 2, 3, 4, 5가 이 아래에 추가됩니다 ──────────
