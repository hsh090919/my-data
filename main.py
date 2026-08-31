import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울의 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 100년간 연평균 기온 변화")

st.write(
    "서울의 일별 기온 데이터를 바탕으로 "
    "각 연도의 평균기온을 계산하여 나타낸 그래프입니다."
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 필요한 데이터가 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


# 데이터 불러오기
df = load_data()

# 날짜에서 연도 추출
df["연도"] = df["날짜"].dt.year

# 연도별 평균기온 계산
yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# 소수점 둘째 자리까지 표시
yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)


# 그래프
st.subheader("📈 연도별 평균기온")

chart_data = yearly_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)"
)


# 통계
st.subheader("📊 기온 변화 요약")

col1, col2, col3 = st.columns(3)

with col1:
    highest = yearly_temp.loc[
        yearly_temp["평균기온"].idxmax()
    ]

    st.metric(
        "가장 높은 연평균 기온",
        f"{highest['평균기온']:.1f} ℃",
        f"{int(highest['연도'])}년"
    )

with col2:
    lowest = yearly_temp.loc[
        yearly_temp["평균기온"].idxmin()
    ]

    st.metric(
        "가장 낮은 연평균 기온",
        f"{lowest['평균기온']:.1f} ℃",
        f"{int(lowest['연도'])}년"
    )

with col3:
    first_temp = yearly_temp.iloc[0]["평균기온"]
    last_temp = yearly_temp.iloc[-1]["평균기온"]
    change = last_temp - first_temp

    st.metric(
        "첫해 대비 마지막 해 변화",
        f"{change:+.1f} ℃"
    )


# 연도별 데이터 확인
with st.expander("📋 연도별 평균기온 데이터 보기"):
    st.dataframe(
        yearly_temp,
        use_container_width=True,
        hide_index=True
    )


st.caption("자료: 서울 기상 관측 데이터(seoul.csv)")
