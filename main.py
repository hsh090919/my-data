import streamlit as st
import pandas as pd
import plotly.graph_objects as go


# ==============================
# 페이지 설정
# ==============================

st.set_page_config(
    page_title="서울의 100년간 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)


# ==============================
# 제목
# ==============================

st.title("🌡️ 서울의 100년간 연평균 기온 변화")

st.write(
    "서울의 일별 평균기온 데이터를 이용하여 연도별 평균기온을 계산했습니다. "
    "관측 데이터가 없는 연도는 선을 임의로 연결하지 않고 끊어서 표시합니다."
)


# ==============================
# 데이터 주소
# ==============================

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


# ==============================
# 데이터 불러오기
# ==============================

@st.cache_data
def load_data():

    try:
        df = pd.read_csv(
            DATA_URL,
            encoding="utf-8-sig"
        )

    except UnicodeDecodeError:
        df = pd.read_csv(
            DATA_URL,
            encoding="cp949"
        )

    # 열 이름 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 날짜 또는 평균기온이 없는 행 제거
    df = df.dropna(
        subset=["날짜", "평균기온"]
    )

    # 날짜순 정렬
    df = df.sort_values("날짜")

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


# ==============================
# 데이터 불러오기
# ==============================

try:
    df = load_data()

except Exception as e:

    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.exception(e)

    st.stop()


# ==============================
# 연도별 평균기온 계산
# ==============================

yearly_temp = (
    df.groupby("연도", as_index=False)["평균기온"]
    .mean()
)

yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)


# ==============================
# 전체 연도 생성
# ==============================

min_year = int(yearly_temp["연도"].min())
max_year = int(yearly_temp["연도"].max())

all_years = pd.DataFrame(
    {
        "연도": range(
            min_year,
            max_year + 1
        )
    }
)


# ==============================
# 실제 데이터와 전체 연도 합치기
# ==============================

yearly_temp = pd.merge(
    all_years,
    yearly_temp,
    on="연도",
    how="left"
)


# ==============================
# 그래프
# ==============================

st.subheader("📈 연도별 평균기온")

fig = go.Figure()


fig.add_trace(
    go.Scatter(
        x=yearly_temp["연도"],
        y=yearly_temp["평균기온"],

        mode="lines+markers",

        name="연평균 기온",

        connectgaps=False,

        hovertemplate=(
            "연도: %{x}년<br>"
            "연평균 기온: %{y:.2f}℃"
            "<extra></extra>"
        )
    )
)


fig.update_layout(

    title="서울 연도별 평균기온 변화",

    xaxis_title="연도",

    yaxis_title="연평균 기온 (℃)",

    height=600,

    hovermode="x",

    showlegend=False,

    font=dict(
        size=15
    )
)


fig.update_xaxes(
    range=[
        min_year,
        max_year
    ]
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ==============================
# 실제 데이터만 사용
# ==============================

valid_data = yearly_temp.dropna(
    subset=["평균기온"]
)


# ==============================
# 통계 정보
# ==============================

st.subheader("📊 기온 변화 요약")

col1, col2, col3 = st.columns(3)


# 가장 높은 기온

highest = valid_data.loc[
    valid_data["평균기온"].idxmax()
]


with col1:

    st.metric(
        "가장 높은 연평균 기온",
        f"{highest['평균기온']:.2f} ℃",
        f"{int(highest['연도'])}년"
    )


# 가장 낮은 기온

lowest = valid_data.loc[
    valid_data["평균기온"].idxmin()
]


with col2:

    st.metric(
        "가장 낮은 연평균 기온",
        f"{lowest['평균기온']:.2f} ℃",
        f"{int(lowest['연도'])}년"
    )


# 첫 연도와 마지막 연도 비교

first_data = valid_data.iloc[0]

last_data = valid_data.iloc[-1]

temperature_change = (
    last_data["평균기온"]
    - first_data["평균기온"]
)


with col3:

    st.metric(
        "첫 관측 연도 대비 변화",
        f"{temperature_change:+.2f} ℃"
    )


# ==============================
# 데이터 정보
# ==============================

st.subheader("📌 데이터 정보")

col4, col5, col6 = st.columns(3)


with col4:

    st.metric(
        "첫 관측 연도",
        f"{int(valid_data.iloc[0]['연도'])}년"
    )


with col5:

    st.metric(
        "마지막 관측 연도",
        f"{int(valid_data.iloc[-1]['연도'])}년"
    )


with col6:

    st.metric(
        "연평균 데이터가 있는 연도",
        f"{len(valid_data)}년"
    )


# ==============================
# 데이터 표
# ==============================

with st.expander("📋 연도별 평균기온 데이터 보기"):

    st.dataframe(
        yearly_temp,
        use_container_width=True,
        hide_index=True
    )


# ==============================
# 출처
# ==============================

st.caption(
    "자료: 서울 기상 관측 데이터(seoul.csv)"
)
