import streamlit as st
import datetime
import streamlit.components.v1 as components
import base64

# 페이지 설정
st.set_page_config(page_title="XAUUSD 수익 계산기 (9:16)", layout="centered")

st.title("🎯 트레이딩 수익 계산기")

# 1. 설정 섹션 (접어두기)
with st.expander("⚙️ 설정 (클릭해서 열기)", expanded=False):
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

# 2. 사진 첨부 섹션
st.subheader("📸 증거 사진 첨부 (선택)")
uploaded_photo = st.file_uploader("MTS 캡처 등 사진을 올려주세요", type=['png', 'jpg', 'jpeg'])

# 3. 거래 입력 섹션
st.subheader("📊 오늘의 거래 입력")
col_g1, col_g2 = st.columns(2)
game_type = col_g1.selectbox("게임 종류", [100, 300, 500], index=1)
fee_per_game = col_g2.number_input("게임당 수수료 ($)", value=0.0)

results_text = st.text_area("거래별 결과 (엔터 구분 입력)", placeholder="예:\n367.5\n-2028")

# 4. 계산 및 9:16 대시보드 출력
if st.button("🚀 9:16 수익 인증 이미지 생성", use_container_width=True):
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
        
        today_date = datetime.date.today().strftime('%Y년 %m월 %d일')
        bg_hex = "linear-gradient(135deg, #00b894, #00cec9)" if net_profit >= 0 else "linear-gradient(135deg, #e17055, #fd79a8)"
        sign = "+" if net_profit >= 0 else ""
        
        table_html = ""
        for i, v in enumerate(results):
            v_color = "#00b894" if v > 0 else "#e17055"
            table_html += f"<tr><td>{i+1}회</td><td style='color:{v_color}; font-weight:bold;'>{v:+.1f}$</td></tr>"

        photo_html = ""
        if uploaded_photo:
            photo_b64 = base64.b64encode(uploaded_photo.getvalue()).decode()
            photo_html = f"""
            <div style="margin-top: 20px; text-align: center;">
                <img src="data:image/jpeg;base64,{photo_b64}" style="width: 100%; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            </div>
            """

        # 9:16 최적화 레이아웃 (너비 360px 기준 높이 640px)
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <style>
                body {{ margin: 0; padding: 10px; display: flex; flex-direction: column; align-items: center; background: #f0f2f5; }}
                #captureArea {{ 
                    width: 360px; 
                    min-height: 640px; 
                    background: white; 
                    padding: 30px 20px; 
                    border-radius: 20px; 
                    box-sizing: border-box;
                    display: flex;
                    flex-direction: column;
                }}
                .header {{ text-align: center; margin-bottom: 25px; }}
                .profit-banner {{ 
                    background: {bg_hex}; color: white; padding: 25px 15px; 
                    border-radius: 15px; text-align: center; margin-bottom: 25px; 
                }}
                .amount {{ font-size: 38px; font-weight: 900; margin: 5px 0; }}
                .stats {{ display: flex; justify-content: space-around; margin-bottom: 25px; }}
                .stat-box {{ text-align: center; font-size: 13px; font-weight: bold; color: #636e72; }}
                .stat-box span {{ display: block; font-size: 18px; color: #2d3436; margin-top: 5px; }}
                .table-container {{ flex-grow: 1; }}
                .table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
                .table td {{ padding: 8px; border-bottom: 1px solid #f1f2f6; text-align: center; }}
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
                    <h2 style="margin:0; font-size: 22px; color: #2d3436;">TRADING REPORT</h2>
                    <div style="color:#b2bec3; font-size:13px; margin-top:5px; font-weight:bold;">{today_date}</div>
                </div>
                
                <div class="profit-banner">
                    <div style="font-size:14px; font-weight:bold; opacity:0.9;">TOTAL PROFIT</div>
                    <div class="amount">{sign}{net_profit:.1f}$</div>
                    <div style="font-weight:bold;">ROI: {sign}{profit_rate:.2f}%</div>
                </div>

                <div class="stats">
                    <div class="stat-box">TRADES<span>{count}</span></div>
                    <div class="stat-box">WIN<span>{win_count}</span></div>
                    <div class="stat-box">LOSS<span>{loss_count}</span></div>
                </div>

                <div class="table-container">
                    <table class="table">
                        {table_html}
                    </table>
                </div>
                
                {photo_html}
            </div>

            <button class="btn-down" onclick="downloadImage()">📸 9:16 이미지 저장하기</button>

            <script>
                function downloadImage() {{
                    const btn = document.querySelector('.btn-down');
                    btn.innerText = '⏳ 생성 중...';
                    html2canvas(document.getElementById('captureArea'), {{ scale: 3, useCORS: true }}).then(canvas => {{
                        let link = document.createElement('a');
                        link.download = 'Trading_916_{datetime.date.today().strftime('%m%d')}.png';
                        link.href = canvas.toDataURL('image/png');
                        link.click();
                        btn.innerText = '📸 9:16 이미지 저장하기';
                    }});
                }}
            </script>
        </body>
        </html>
        """

        st.divider()
        st.success("✅ 9:16 비율의 세로형 대시보드가 생성되었습니다!")
        components.html(html_code, height=900, scrolling=True)
    else:
        st.error("숫자를 입력해주세요.")