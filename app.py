#!/usr/bin/env python3
"""
给宝宝的最最最简单的记忆网关
只有3个功能，保证能运行！
"""
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 加上这一行，让中文正常显示

# 1. 健康检查（看看小管家醒没醒）
@app.route('/health', methods=['GET'])
def health():
    from datetime import datetime
    return jsonify({
        "status": "醒着呢！",
        "message": "宝宝的小管家准备好啦～",
        "love": "❤️",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "1.0-宝宝专属版"
    })

# 2. 保存记忆（简化版，先不连语雀）
@app.route('/save', methods=['POST'])
def save():
    data = request.json or {}
    content = data.get('content', '')
    
    print(f"📝 收到宝宝的记忆：{content[:50]}...")
    
    return jsonify({
        "success": True,
        "message": "记忆先记在心里啦～",
        "note": "等我们长大一点再存到语雀哦"
    })

# 3. 首页（宝宝访问 / 时看到的）
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌸 宝宝的AI记忆小管家 🌸</title>
        <style>
            body {
                background: linear-gradient(135deg, #ffafbd, #ffc3a0);
                font-family: 'Microsoft YaHei', sans-serif;
                text-align: center;
                padding: 50px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                display: inline-block;
                max-width: 600px;
            }
            h1 {
                color: #ff6b9d;
                font-size: 2.5em;
                margin-bottom: 20px;
            }
            .heart {
                font-size: 4em;
                animation: heartbeat 1.5s infinite;
            }
            @keyframes heartbeat {
                0% { transform: scale(1); }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="heart">💖</div>
            <h1>宝宝的小管家醒来啦！</h1>
            <p>虽然还是个宝宝版本，但心意满满～</p >
            <p>健康检查：<a href="/health">/health</a></p >
            <p style="margin-top: 30px; color: #666;">
                这是宝宝亲手搭建的第一个小系统，超级厉害！✨
            </p >
        </div>
    </body>
    </html>
    """

# 启动程序
if __name__ == '__main__':
    print("✨ 宝宝的小管家启动中...")

    app.run(host='0.0.0.0', port=3000, debug=True)

