import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="서울 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 기온 변화")
st.write("서울의 원본 기온 데이터를 그대로 나타낸 그래프입니다.")

# 원본 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온 숫자 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 날짜와 평균기온이 없는 데이터 제거
    df = df.dropna(subset=["날짜", "평균기온"])

    # 날짜 순서대로 정렬
    df = df.sort_values("날짜")

    return df


df = load_data()

# -------------------------
# 원본 데이터 그대로 그래프
# -------------------------

st.subheader("📈 서울 일별 평균기온")

chart_data = df[["날짜", "평균기온"]].copy()
chart_data = chart_data.set_index("날짜")

st.line_chart(
    chart_data,
    y="평균기온",
    x_label="날짜",
    y_label="평균기온 (℃)"
)

# -------------------------
# 데이터 정보
# -------------------------

st.subheader("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "데이터 시작",
        df["날짜"].min().strftime("%Y-%m-%d")
    )

with col2:
    st.metric(
        "데이터 마지막",
        df["날짜"].max().strftime("%Y-%m-%d")
    )

with col3:
    st.metric(
        "데이터 개수",
        f"{len(df):,}개"
    )

# -------------------------
# 원본 데이터 확인
# -------------------------

with st.expander("📋 원본 데이터 보기"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

st.caption("자료: 서울 기상 관측 데이터(seoul.csv)")
