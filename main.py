import streamlit as st
import pandas as pd


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
    "관측 자료가 없는 연도는 데이터를 임의로 만들지 않고 빈 값으로 표시합니다."
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

    df = pd.read_csv(DATA_URL)

    # 열 이름의 앞뒤 공백 제거
    df.columns = df.columns.str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 평균기온 숫자로 변환
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

# 소수점 둘째 자리까지
yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)


# ==============================
# 전체 연도 생성
# ==============================

min_year = int(yearly_temp["연도"].min())
max_year = int(yearly_temp["연도"].max())

all_years = pd.DataFrame({
    "연도": range(min_year, max_year + 1)
})


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

st.write(
    "연도가 연속되어 있어도 실제 관측 데이터가 없는 연도는 빈 값으로 남겨두었습니다."
)

# 연도를 인덱스로 설정
chart_data = yearly_temp.set_index("연도")

# Streamlit 기본 그래프
st.line_chart(
    chart_data,
    y="평균기온",
    use_container_width=True
)


# ==============================
# 실제 데이터만 따로 저장
# ==============================

valid_data = yearly_temp.dropna(
    subset=["평균기온"]
)


# ==============================
# 통계
# ==============================

st.subheader("📊 기온 변화 요약")

col1, col2, col3 = st.columns(3)


# 가장 높은 연평균 기온
highest = valid_data.loc[
    valid_data["평균기온"].idxmax()
]

with col1:
    st.metric(
        "가장 높은 연평균 기온",
        f"{highest['평균기온']:.2f} ℃"
    )

    st.write(
        f"{int(highest['연도'])}년"
    )


# 가장 낮은 연평균 기온
lowest = valid_data.loc[
    valid_data["평균기온"].idxmin()
]

with col2:
    st.metric(
        "가장 낮은 연평균 기온",
        f"{lowest['평균기온']:.2f} ℃"
    )

    st.write(
        f"{int(lowest['연도'])}년"
    )


# 첫 관측 연도와 마지막 관측 연도 비교
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

st.subheader("📌 데이터 기간")

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
