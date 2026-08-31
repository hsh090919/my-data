import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="서울의 100년 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

# 제목
st.title("🌡️ 서울의 100년간 연평균 기온 변화")
st.write(
    "서울의 일별 기온 데이터를 이용하여 연도별 평균기온을 계산하고 "
    "장기간의 기온 변화를 살펴봅니다."
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜를 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온을 숫자로 변환
    df["평균기온"] = pd.to_numeric(df["평균기온"], errors="coerce")

    # 날짜 또는 평균기온이 없는 행 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    return df


df = load_data()

# 연도 추출
df["연도"] = df["날짜"].dt.year

# 연도별 평균기온 계산
yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

# 소수점 둘째 자리까지 표시
yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)

# 데이터 기간
start_year = yearly_temp["연도"].min()
end_year = yearly_temp["연도"].max()

st.subheader(f"📈 {start_year}년 ~ {end_year}년 서울 연평균 기온")

# 선그래프
chart_data = yearly_temp.set_index("연도")

st.line_chart(
    chart_data,
    y="평균기온",
    x_label="연도",
    y_label="연평균 기온 (℃)"
)

# 간단한 통계
st.subheader("📊 기온 변화 요약")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "가장 낮은 연평균 기온",
        f"{yearly_temp['평균기온'].min():.1f} ℃"
    )

with col2:
    st.metric(
        "가장 높은 연평균 기온",
        f"{yearly_temp['평균기온'].max():.1f} ℃"
    )

with col3:
    first_temp = yearly_temp.iloc[0]["평균기온"]
    last_temp = yearly_temp.iloc[-1]["평균기온"]
    change = last_temp - first_temp

    st.metric(
        "처음과 마지막 연도의 차이",
        f"{change:+.1f} ℃"
    )

# 데이터 표
with st.expander("📋 연도별 평균기온 데이터 보기"):
    st.dataframe(
        yearly_temp,
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "자료: 서울 기상 관측 데이터(seoul.csv)"
)
