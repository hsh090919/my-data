import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울의 100년간 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 100년간 연평균 기온 변화")

st.write(
    "서울의 일별 기온 데이터를 이용하여 연평균 기온을 계산했습니다. "
    "관측 자료가 없는 연도는 그래프를 임의로 연결하지 않고 "
    "불연속 구간으로 표시합니다."
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 평균기온 숫자 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(
        subset=["날짜", "평균기온"]
    )

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


# 데이터 불러오기
df = load_data()


# --------------------------------
# 연도별 평균기온 계산
# --------------------------------

yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)


# --------------------------------
# 데이터가 존재하지 않는 연도 찾기
# --------------------------------

min_year = int(yearly_temp["연도"].min())
max_year = int(yearly_temp["연도"].max())

# 전체 연도 생성
all_years = pd.DataFrame({
    "연도": range(min_year, max_year + 1)
})

# 실제 관측된 연평균과 전체 연도를 합치기
yearly_temp = all_years.merge(
    yearly_temp,
    on="연도",
    how="left"
)


# --------------------------------
# 그래프
# --------------------------------

st.subheader("📈 연도별 평균기온")

fig = px.line(
    yearly_temp,
    x="연도",
    y="평균기온",
    markers=True,
    labels={
        "연도": "연도",
        "평균기온": "연평균 기온 (℃)"
    },
    title="서울 연평균 기온 변화"
)

# 결측값(NaN)이 있는 곳에서 선이 끊어지도록 설정
fig.update_traces(
    connectgaps=False
)

fig.update_layout(
    hovermode="x unified",
    height=550
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# --------------------------------
# 통계
# --------------------------------

st.subheader("📊 기온 변화 요약")

col1, col2, col3 = st.columns(3)

valid_data = yearly_temp.dropna(
    subset=["평균기온"]
)

with col1:
    highest = valid_data.loc[
        valid_data["평균기온"].idxmax()
    ]

    st.metric(
        "가장 높은 연평균 기온",
        f"{highest['평균기온']:.1f} ℃",
        f"{int(highest['연도'])}년"
    )

with col2:
    lowest = valid_data.loc[
        valid_data["평균기온"].idxmin()
    ]

    st.metric(
        "가장 낮은 연평균 기온",
        f"{lowest['평균기온']:.1f} ℃",
        f"{int(lowest['연도'])}년"
    )

with col3:
    first = valid_data.iloc[0]
    last = valid_data.iloc[-1]

    change = last["평균기온"] - first["평균기온"]

    st.metric(
        "첫 관측연도 대비 변화",
        f"{change:+.1f} ℃"
    )


# --------------------------------
# 연도별 데이터
# --------------------------------

with st.expander("📋 연도별 평균기온 데이터 보기"):
    st.dataframe(
        yearly_temp,
        use_container_width=True,
        hide_index=True
    )


st.caption(
    "자료: 서울 기상 관측 데이터(seoul.csv)"
)
