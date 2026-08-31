import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="서울의 100년간 연평균 기온 변화",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울의 100년간 연평균 기온 변화")

st.write(
    "서울의 일별 기온 데이터를 이용하여 연도별 평균기온을 계산했습니다. "
    "관측 자료가 없는 연도는 임의로 연결하지 않고 그래프를 끊어서 표시합니다."
)

# 데이터 주소
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/seoul.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 날짜 변환
    df["날짜"] = pd.to_datetime(df["날짜"], errors="coerce")

    # 평균기온 숫자로 변환
    df["평균기온"] = pd.to_numeric(
        df["평균기온"],
        errors="coerce"
    )

    # 날짜와 평균기온이 없는 행 제거
    df = df.dropna(
        subset=["날짜", "평균기온"]
    )

    # 연도 추출
    df["연도"] = df["날짜"].dt.year

    return df


# 데이터 불러오기
df = load_data()


# =========================
# 연도별 평균기온 계산
# =========================

yearly_temp = (
    df.groupby("연도")["평균기온"]
    .mean()
    .reset_index()
)

yearly_temp["평균기온"] = yearly_temp["평균기온"].round(2)


# =========================
# 전체 연도 만들기
# =========================

min_year = int(yearly_temp["연도"].min())
max_year = int(yearly_temp["연도"].max())

all_years = pd.DataFrame({
    "연도": range(min_year, max_year + 1)
})

# 실제 데이터와 전체 연도를 합침
yearly_temp = all_years.merge(
    yearly_temp,
    on="연도",
    how="left"
)


# =========================
# 그래프
# =========================

st.subheader("📈 연도별 평균기온")

fig, ax = plt.subplots(figsize=(14, 6))

ax.plot(
    yearly_temp["연도"],
    yearly_temp["평균기온"],
    marker="o",
    markersize=3,
    linewidth=1.2
)

ax.set_title(
    "서울 연평균 기온 변화",
    fontsize=18
)

ax.set_xlabel(
    "연도",
    fontsize=12
)

ax.set_ylabel(
    "연평균 기온 (℃)",
    fontsize=12
)

# 격자
ax.grid(
    True,
    alpha=0.3
)

# x축 범위
ax.set_xlim(
    min_year,
    max_year
)

# 레이아웃 정리
plt.tight_layout()

st.pyplot(fig)


# =========================
# 데이터 정보
# =========================

st.subheader("📊 데이터 정보")

col1, col2, col3 = st.columns(3)

valid_data = yearly_temp.dropna(
    subset=["평균기온"]
)

with col1:
    st.metric(
        "첫 관측 연도",
        f"{int(valid_data.iloc[0]['연도'])}년"
    )

with col2:
    st.metric(
        "마지막 관측 연도",
        f"{int(valid_data.iloc[-1]['연도'])}년"
    )

with col3:
    st.metric(
        "관측된 연도 수",
        f"{len(valid_data):,}년"
    )


# =========================
# 연도별 평균기온 표
# =========================

with st.expander("📋 연도별 평균기온 데이터 보기"):

    st.dataframe(
        yearly_temp,
        use_container_width=True,
        hide_index=True
    )


st.caption(
    "자료: 서울 기상 관측 데이터(seoul.csv)"
)
