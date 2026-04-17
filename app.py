import streamlit as st
import datetime

# 페이지 설정
st.set_page_config(page_title="트레이딩 수익 계산기", layout="centered")

st.title("🎯 트레이딩 수익 계산기")

# 1. 반영구 설정 섹션
with st.expander("⚙️ 반영구 설정 (설정 유지)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛡️ 보험금")
        insLot = st.number_input("보험금 랏수", value=0.7, step=0.1)
        insTP = st.number_input("보험금 TP", value=540, step=10)
        insSL = st.number_input("보험금 SL", value=2800, step=100)
    with col2:
        st.subheader("⚔️ 챌린지")
        chaLot = st.number_input("챌린지 랏수", value=5.3, step=0.1)
        chaTP = st.number_input("챌린지 TP", value=2720, step=100)
        chaSL = st.number_input("챌린지 SL", value=580, step=10)

# 2. 거래 입력 섹션
st.subheader("📊 오늘의 거래 입력")
col_g1, col_g2 = st.columns(2)
game_type = col_g1.selectbox("게임 종류", [100, 300, 500], index=1)
fee_per_game = col_g2.number_input("게임당 수수료 ($)", value=0.0)

results_text = st.text_area("거래별 결과 (엔터로 구분하여 입력)", placeholder="예:\n367.5\n-2028\n380")

# 3. 계산 버튼
if st.button("🚀 수익 계산 및 대시보드 생성"):
    lines = results_text.strip().split('\n')
    results = []
    for line in lines:
        try:
            val = float(line.strip().replace(',', ''))
            results.append(val)
        except: continue
    
    if results:
        count = len(results)
        total_earned = sum(x for x in results if x > 0)
        total_loss = sum(x for x in results if x < 0)
        win_count = len([x for x in results if x > 0])
        loss_count = len([x for x in results if x < 0])
        
        net_profit = total_earned + total_loss - (count * game_type) - (count * fee_per_game)
        profit_rate = (net_profit / (count * game_type)) * 100 if count > 0 else 0
        
        # 결과 화면 출력
        st.divider()
        st.header("📊 수익 인증 결과")
        st.write(f"날짜: {datetime.date.today().strftime('%Y년 %m월 %d일')}")
        
        # 수익 금액 강조
        color = "green" if net_profit >= 0 else "red"
        st.markdown(f"### 💰 오늘의 순손익: :{color}[{net_profit:+.1f}$]")
        st.markdown(f"**수익률: :{color}[{profit_rate:+.2f}%]**")
        
        # 주요 지표
        m1, m2, m3 = st.columns(3)
        m1.metric("총 거래", f"{count}회")
        m2.metric("수익 거래", f"{win_count}회")
        m3.metric("챌린지 성공", f"{loss_count}회")
        
        # 상세 내역 테이블
        st.table([{"회차": f"{i+1}회차", "결과": f"{v:+.1f}$"} for i, v in enumerate(results)])
        
        st.info("💡 위 화면을 스크린샷하여 인증 이미지로 사용하세요!")
    else:
        st.error("입력된 결과가 없습니다. 숫자를 입력해주세요.")