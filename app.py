import streamlit as st
import datetime
import streamlit.components.v1 as components
import base64

# 페이지 설정
st.set_page_config(page_title="트레이딩 수익 계산기", layout="centered")

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

# [복구됨!] 2. 사진 첨부 섹션
st.subheader("📸 증거 사진 첨부 (선택)")
uploaded_photo = st.file_uploader("MTS 캡처, 거래내역 스크린샷 등을 올려주세요", type=['png', 'jpg', 'jpeg'])

# 3. 거래 입력 섹션
st.subheader("📊 오늘의 거래 입력")
col_g1, col_g2 = st.columns(2)
game_type = col_g1.selectbox("게임 종류", [100, 300, 500], index=1)
fee_per_game = col_g2.number_input("게임당 수수료 ($)", value=0.0)

results_text = st.text_area("거래별 결과 (엔터로 구분하여 입력)", placeholder="예:\n367.5\n-2028\n380")

# 4. 계산 및 대시보드
if st.button("🚀 수익 계산 및 대시보드 생성", use_container_width=True):
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
        
        # 색상 및 기호
        color_hex = "#00b894" if net_profit >= 0 else "#e17055"
        bg_hex = "linear-gradient(135deg, #00b894, #00cec9)" if net_profit >= 0 else "linear-gradient(135deg, #e17055, #fd79a8)"
        sign = "+" if net_profit >= 0 else ""
        
        # 테이블 내역 생성
        table_html = ""
        for i, v in enumerate(results):
            v_color = "#00b894" if v > 0 else "#e17055"
            v_text = "수익" if v > 0 else "챌린지 성공"
            table_html += f"<tr><td>{i+1}회차</td><td style='color:{v_color}; font-weight:bold;'>{v:+.1f}$</td><td>{v_text}</td></tr>"

        # [핵심 추가] 업로드된 사진을 다운로드 이미지 안에 넣기 위한 처리
        photo_html = ""
        extra_height = 0
        if uploaded_photo:
            # 파이썬으로 받은 이미지를 HTML이 읽을 수 있게 글자로 변환
            photo_b64 = base64.b64encode(uploaded_photo.getvalue()).decode()
            photo_html = f"""
            <div style="margin-top: 25px; padding-top: 20px; border-top: 2px dashed #bdc3c7; text-align: center;">
                <div style="font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 15px;">📸 증거 사진</div>
                <img src="data:image/jpeg;base64,{photo_b64}" style="max-width: 100%; max-height: 400px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            </div>
            """
            extra_height = 450 # 사진이 있으면 창 길이를 늘려줌

        # HTML 구조 (여기에 표와 사진이 모두 합쳐집니다)
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <style>
                body {{ font-family: -apple-system, sans-serif; margin: 0; padding: 10px; background: #f8f9fa; }}
                #captureArea {{ background: white; padding: 25px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .profit-banner {{ background: {bg_hex}; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }}
                .amount {{ font-size: 32px; font-weight: 900; margin: 5px 0; }}
                .stats {{ display: flex; justify-content: space-between; text-align: center; margin-bottom: 20px; }}
                .stat-box {{ background: #f1f2f6; padding: 10px; border-radius: 8px; width: 30%; font-weight: bold; }}
                .table {{ width: 100%; border-collapse: collapse; text-align: center; font-size: 14px; }}
                .table th {{ background: #2c3e50; color: white; padding: 10px; }}
                .table td {{ padding: 10px; border-bottom: 1px solid #eee; }}
                .btn-down {{ background: #e74c3c; color: white; border: none; padding: 15px; width: 100%; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; display: block; }}
            </style>
        </head>
        <body>
            <div id="captureArea">
                <div class="header">
                    <h2 style="margin:0;">📊 수익 인증 결과</h2>
                    <div style="color:#7f8c8d; font-size:14px; margin-top:5px;">{today_date}</div>
                </div>
                
                <div class="profit-banner">
                    <div style="font-size:14px;">💰 오늘의 순손익</div>
                    <div class="amount">{sign}{net_profit:.1f}$</div>
                    <div>수익률: {sign}{profit_rate:.2f}%</div>
                </div>

                <div class="stats">
                    <div class="stat-box">🎮 총 거래<br><span style="font-size:20px; color:#2c3e50;">{count}회</span></div>
                    <div class="stat-box">✅ 수익 거래<br><span style="font-size:20px; color:#00b894;">{win_count}회</span></div>
                    <div class="stat-box">🏆 챌린지 성공<br><span style="font-size:20px; color:#9b59b6;">{loss_count}회</span></div>
                </div>

                <table class="table">
                    <tr><th>회차</th><th>회수금액</th><th>결과</th></tr>
                    {table_html}
                </table>
                
                {photo_html}
            </div>

            <button class="btn-down" onclick="downloadImage()">📸 인증 이미지 원클릭 다운로드</button>

            <script>
                function downloadImage() {{
                    const btn = document.querySelector('.btn-down');
                    btn.innerText = '⏳ 이미지 생성 중...';
                    
                    html2canvas(document.getElementById('captureArea'), {{ scale: 2, useCORS: true }}).then(canvas => {{
                        let link = document.createElement('a');
                        let today = new Date().toISOString().slice(0, 10).replace(/-/g, '');
                        link.download = '수익인증_' + today + '.png';
                        link.href = canvas.toDataURL('image/png');
                        link.click();
                        btn.innerText = '📸 인증 이미지 원클릭 다운로드';
                    }});
                }}
            </script>
        </body>
        </html>
        """

        st.divider()
        st.success("✅ 계산 완료! 첨부하신 사진도 인증 이미지 가장 아래에 자동으로 합성됩니다.")
        
        # 화면에 표시되는 창 크기를 사진 유무에 따라 조절
        box_height = 500 + (count * 40) + extra_height
        components.html(html_code, height=box_height, scrolling=True)
        
    else:
        st.error("입력된 결과가 없습니다. 숫자를 입력해주세요.")