import streamlit as st
import datetime

# 페이지 설정
st.set_page_config(page_title="트레이딩 수익 계산기", layout="centered")

st.title("🎯 트레이딩 수익 계산기")

# 1. 반영구 설정 섹션
with st.expander("⚙️ 반영구 설정 (설정 유지)", expanded=False): # 기본적으로 접어두기
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

# [NEW] 2. 사진 업로드 섹션
st.subheader("📸 증거 사진 첨부 (선택)")
uploaded_photo = st.file_uploader("MTS 캡처, 거래내역 스크린샷 등을 올려주세요", type=['png', 'jpg', 'jpeg'])

if uploaded_photo:
    st.success("✅ 사진이 정상적으로 첨부되었습니다!")
    with st.expander("첨부된 사진 미리보기"):
        st.image(uploaded_photo, use_container_width=True)

# 3. 거래 입력 섹션
st.subheader("📊 오늘의 거래 입력")
col_g1, col_g2 = st.columns(2)
game_type = col_g1.selectbox("게임 종류", [100, 300, 500], index=1)
fee_per_game = col_g2.number_input("게임당 수수료 ($)", value=0.0)

results_text = st.text_area("거래별 결과 (엔터로 구분하여 입력)", placeholder="예:\n367.5\n-2028\n380")

# 4. 계산 버튼 및 대시보드 출력
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
        
        # --- 결과 대시보드 ---
        st.divider()
        st.header("📊 수익 인증 대시보드")
        st.write(f"📅 **날짜:** {datetime.date.today().strftime('%Y년 %m월 %d일')}")
        
        color = "green" if net_profit >= 0 else "red"
        st.markdown(f"### 💰 오늘의 순손익: :{color}[{net_profit:+.1f}$]")
        st.markdown(f"**수익률: :{color}[{profit_rate:+.2f}%]**")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("총 거래", f"{count}회")
        m2.metric("수익 거래", f"{win_count}회")
        m3.metric("챌린지 성공", f"{loss_count}회")
        
        st.table([{"회차": f"{i+1}회차", "결과": f"{v:+.1f}$"} for i, v in enumerate(results)])
        
        # [NEW] 대시보드 하단에 첨부된 사진 표시
        if uploaded_photo:
            st.markdown("### 📸 거래 증빙 자료")
            st.image(uploaded_photo, use_container_width=True)
            
        st.info("💡 스마트폰의 [화면 캡처] 기능을 이용해 전체 결과를 저장하고 공유하세요!")
    else:
        st.error("입력된 결과가 없습니다. 숫자를 입력해주세요.")