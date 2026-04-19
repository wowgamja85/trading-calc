import streamlit as st
import datetime
import streamlit.components.v1 as components
import base64

# 1. 페이지 설정
st.set_page_config(page_title="XAUUSD 수익 계산기", layout="centered")

# [디자인] 앱 메인 제목 (크기를 줄여 모바일 한 줄 출력)
st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🎯 트레이딩 수익 계산기</h3>", unsafe_allow_html=True)

# 2. 설정 섹션
with st.expander("⚙️ 기본 설정 (이미지에 포함됨)", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛡️ 보험금 설정")
        insLot = st.number_input("보험금 랏수", value=0.7, step=0.1)
        insTP = st.number_input("보험금 TP (틱)", value=540, step=10)
        insSL = st.number_input("보험금 SL (틱)", value=2800, step=100)
    with col2:
        st.subheader("⚔️ 챌린지 설정")
        chaLot = st.number_input("챌린지 랏수", value=5.3, step=0.1)
        chaTP = st.number_input("챌린지 TP (틱)", value=2720, step=100)
        chaSL = st.number_input("챌린지 SL (틱)", value=580, step=10)

# 3. 사진 첨부 섹션
st.subheader("📸 거래기록 화면 첨부 (선택)")
# 도움말 제공: 인앱 브라우저 권한 문제 방지
st.info("💡 **팁:** 버튼을 누르면 앨범 선택이나 카메라 촬영이 가능합니다. 카메라가 안 뜨면 크롬/사파리 브라우저로 접속해 주세요.")
uploaded_photo = st.file_uploader("거래 내역을 캡처하거나 직접 찍어서 올려주세요", type=['png', 'jpg', 'jpeg'])

# 4. 거래 입력 섹션
st.subheader("📊 오늘의 거래 입력")
col_g1, col_g2 = st.columns(2)
game_type = col_g1.selectbox("게임 종류 ($)", [100, 300, 500], index=1)

# [자동 계산] 수수료 = 보험금 랏수 * 20
fee_per_game = insLot * 20
col_g2.text_input("게임당 수수료 ($) - 자동계산", value=f"{fee_per_game:.1f}", disabled=True)

results_text = st.text_area("거래별 결과 입력 (엔터로 구분)", placeholder="예:\n367.5\n-2028\n380")

# 5. 계산 및 대시보드 생성
if st.button("🚀 수익 인증 이미지 생성하기", use_container_width=True):
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
        
        # 순수익 및 수익률 계산
        net_profit = total_earned + total_loss - (count * game_type) - (count * fee_per_game)
        profit_rate = (net_profit / (count * game_type)) * 100 if count > 0 else 0
        
        today_date = datetime.date.today().strftime('%Y년 %m월 %d일')
        bg_hex = "linear-gradient(135deg, #00b894, #00cec9)" if net_profit >= 0 else "linear-gradient(135deg, #e17055, #fd79a8)"
        sign = "+" if net_profit >= 0 else ""
        
        # 거래 내역 테이블 HTML 생성
        table_html = ""
        for i, v in enumerate(results):
            v_color = "#00b894" if v > 0 else "#e17055"
            v_label = "수익" if v > 0 else "성공"
            table_html += f"<tr><td>{i+1}회차</td><td style='color:{v_color}; font-weight:bold;'>{v:+.1f}$</td><td>{v_label}</td></tr>"

        # 사진 데이터 처리 (Base64 인코딩)
        photo_html = ""
        extra_height = 0
        if uploaded_photo:
            photo_b64 = base64.b64encode(uploaded_photo.getvalue()).decode()
            photo_html = f"""
            <div style="margin-top: 20px; text-align: center;">
                <img src="data:image/jpeg;base64,{photo_b64}" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            </div>
            """
            extra_height = 350

        # [HTML/CSS/JS] 9:16 비율 대시보드 및 다운로드 기능
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <style>
                body {{ margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; background: #f0f2f5; font-family: 'Apple SD Gothic Neo', sans-serif; }}
                #captureArea {{ 
                    width: 360px; min-height: 640px; background: white; padding: 25px 20px; 
                    border-radius: 20px; box-sizing: border-box; display: flex; flex-direction: column; 
                }}
                .header {{ text-align: center; margin-bottom: 20px; border-bottom: 2px solid #f1f2f6; padding-bottom: 10px; }}
                .date {{ color:#b2bec3; font-size:12px; font-weight:bold; }}
                .profit-banner {{ 
                    background: {bg_hex}; color: white; padding: 20px 10px; 
                    border-radius: 15px; text-align: center; margin-bottom: 20px; 
                }}
                .amount {{ font-size: 34px; font-weight: 900; margin: 5px 0; }}
                
                .settings-grid {{ 
                    display: grid; grid-template-columns: 1fr 1fr; gap: 10px; 
                    background: #f8f9fa; padding: 12px; border-radius: 12px; margin-bottom: 20px; font-size: 11px;
                }}
                .set-title {{ font-weight: bold; margin-bottom: 5px; color: #2d3436; text-align: center; border-bottom: 1px solid #dfe6e9; }}
                .set-item {{ display: flex; justify-content: space-between; padding: 2px 0; }}
                .set-label {{ color: #636e72; }}
                .set-val {{ font-weight: bold; color: #2d3436; }}

                .stats {{ display: flex; justify-content: space-around; margin-bottom: 20px; }}
                .stat-box {{ text-align: center; font-size: 12px; font-weight: bold; color: #636e72; }}
                .stat-box span {{ display: block; font-size: 16px; color: #2d3436; margin-top: 3px; }}
                
                .table-container {{ flex-grow: 1; }}
                .table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
                .table th {{ background: #f1f2f6; padding: 8px; font-size: 11px; color: #636e72; }}
                .table td {{ padding: 7px; border-bottom: 1px solid #f1f2f6; text-align: center; }}
                
                .btn-down {{ 
                    background: #2d3436; color: white; border: none; padding: 15px; 
                    width: 360px; border-radius: 12px; font-size: 16px; font-weight: bold; 
                    cursor: pointer; margin-top: 15px;
                }}
            </style>
        </head>
        <body>
            <div id="captureArea">
                <div class="header">
                    <h2 style="margin:0; font-size: 17px; color: #2d3436; letter-spacing: -0.5px;">트레이딩 수익 인증</h2>
                    <div class="date">{today_date}</div>
                </div>
                
                <div class="profit-banner">
                    <div style="font-size:12px; font-weight:bold; opacity:0.9;">오늘의 순손익 (NET PROFIT)</div>
                    <div class="amount">{sign}{net_profit:.1f}$</div>
                    <div style="font-weight:bold; font-size: 14px;">수익률: {sign}{profit_rate:.2f}%</div>
                </div>

                <div class="settings-grid">
                    <div>
                        <div class="set-title">🛡️ 보험금 설정</div>
                        <div class="set-item"><span class="set-label">랏수</span><span class="set-val">{insLot}</span></div>
                        <div class="set-item"><span class="set-label">TP</span><span class="set-val">{insTP}</span></div>
                        <div class="set-item"><span class="set-label">SL</span><span class="set-val">{insSL}</span></div>
                    </div>
                    <div>
                        <div class="set-title">⚔️ 챌린지 설정</div>
                        <div class="set-item"><span class="set-label">랏수</span><span class="set-val">{chaLot}</span></div>
                        <div class="set-item"><span class="set-label">TP</span><span class="set-val">{chaTP}</span></div>
                        <div class="set-item"><span class="set-label">SL</span><span class="set-val">{chaSL}</span></div>
                    </div>
                </div>

                <div class="stats">
                    <div class="stat-box">총 거래<span>{count}회</span></div>
                    <div class="stat-box">수익<span>{win_count}회</span></div>
                    <div class="stat-box">성공<span>{loss_count}회</span></div>
                </div>

                <div class="table-container">
                    <table class="table">
                        <thead><tr><th>회차</th><th>금액</th><th>결과</th></tr></thead>
                        {table_html}
                    </table>
                </div>
                
                {photo_html}
            </div>

            <button class="btn-down" onclick="downloadImage()">📸 이미지 다운로드 (9:16)</button>

            <script>
                function downloadImage() {{
                    const btn = document.querySelector('.btn-down');
                    btn.innerText = '⏳ 이미지 생성 중...';
                    html2canvas(document.getElementById('captureArea'), {{ scale: 3, useCORS: true }}).then(canvas => {{
                        let link = document.createElement('a');
                        let today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
                        link.download = '수익인증_' + today + '.png';
                        link.href = canvas.toDataURL('image/png');
                        link.click();
                        btn.innerText = '📸 이미지 다운로드 (9:16)';
                    }});
                }}
            </script>
        </body>
        </html>
        """

        st.divider()
        st.success("✅ 대시보드가 생성되었습니다. 아래 버튼을 눌러 이미지를 저장하세요.")
        # 화면 출력 창 높이 자동 조절
        box_height = 650 + (count * 40) + extra_height
        components.html(html_code, height=box_height, scrolling=True)
    else:
        st.error("입력값이 없습니다. 숫자를 입력해주세요.")