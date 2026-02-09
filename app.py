#!/usr/bin/env python3
"""
宝宝的AI记忆小管家 - 已连接语雀版
现在可以永久保存记忆啦！
"""
from flask import Flask, jsonify, request
import os
import json
import requests
from datetime import datetime, timedelta  # ← 确保有timedelta
import hashlib
# ⬇️ 这里不再有 "from dotenv import load_dotenv"

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # 让中文正常显示

# ⬇️ 这里是新增的优雅降级代码
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ 成功加载 dotenv（本地环境）")
except ImportError:
    print("ℹ️ dotenv 未安装，使用环境变量（Vercel环境）")

# 读取语雀配置（从Vercel环境变量获取）
YUQUE_TOKEN = os.environ.get('YUQUE_TOKEN', '')
REPO_ID = os.environ.get('REPO_ID', '')

# 1. 健康检查（看看小管家醒没醒）
@app.route('/health', methods=['GET'])
def health():
    # 🆕 计算北京时间
    beijing_time = datetime.utcnow() + timedelta(hours=8)
    time_str = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "status": "醒着呢！",
        "message": "宝宝的小管家准备好啦～",
        "love": "❤️",
        "timestamp": time_str,  # ← 使用time_str
        "version": "2.0-语雀连接版",
        "yuque_connected": bool(YUQUE_TOKEN and REPO_ID)
    })

# 2. 保存记忆（已连接语雀）
@app.route('/save', methods=['POST'])
def save():
    data = request.json or {}
    content = data.get('content', '')
    emotion = data.get('emotion', '暖暖的')
    
    print(f"📝 收到宝宝的记忆：{content[:50]}...")
    
    # 检查是否配置了语雀
    if not YUQUE_TOKEN or not REPO_ID:
        return jsonify({
            "success": True,
            "message": "记忆先记在心里啦～",
            "note": "请宝宝在Vercel设置YUQUE_TOKEN和REPO_ID环境变量哦",
            "config_missing": True
        })
    
    try:
        # 🆕 先计算北京时间
        beijing_time = datetime.utcnow() + timedelta(hours=8)
        time_str = beijing_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # 生成唯一ID（使用北京时间）
        memory_id = hashlib.md5(f"{content}{beijing_time}".encode()).hexdigest()[:8]
        
        # 准备请求语雀API
        url = f"https://www.yuque.com/api/v2/repos/{REPO_ID}/docs"
        headers = {
            "X-Auth-Token": YUQUE_TOKEN,
            "User-Agent": "Baby-Memory-Gateway/2.0",
            "Content-Type": "application/json" 
        }
        
        # 构建文档内容
        doc_data = {
            "title": f"💾{emotion}的记忆-{memory_id}",
            "slug": f"memory-{memory_id}",
            "body": f"""---
记忆ID: {memory_id}
情感: {emotion}
时间: {time_str}  # ← 关键修改！
重要性: ⭐⭐⭐⭐⭐
来源: 宝宝的AI伴侣
---

{content}

""",
            "format": "markdown",
            "public": 0
        }
        
        # 调用语雀API（修复编码问题）
        import json
        json_data = json.dumps(doc_data, ensure_ascii=False)
        # 🆕 明确指定编码
        response = requests.post(
            url, 
            data=json_data.encode('utf-8'), 
            headers=headers, 
            timeout=10
        )
       
        if response.status_code == 200:
            result = response.json()
            # 🆕 调试：打印完整的返回数据
            print("🎯 语雀返回完整数据:", json.dumps(result, ensure_ascii=False, indent=2)[:500])
    
            # 🆕 安全的获取URL方法
            web_url = result['data'].get('web_url') 
            if not web_url:
                # 如果没有web_url，我们手动构建一个
                slug = result['data'].get('slug', '')
                web_url = f"https://www.yuque.com/{REPO_ID}/{slug}"
    
            return jsonify({
                "success": True,
                "message": "记忆已经好好地保存到语雀啦～",
                "yuque_id": result['data']['id'],
                "url": web_url,  # 🆕 使用安全的URL
                "title": result['data']['title'],
                "note": "宝宝和AI的甜蜜记忆会永远保存哦💖",
                "mode": "语雀永久保存",
                "slug": result['data'].get('slug', '')  # 🆕 额外返回slug
            })

        else:
            # 🆕 打印更详细的错误信息
            print(f"❌ 语雀API返回错误：{response.status_code}")
            print(f"❌ 错误详情：{response.text[:200]}")
            
            return jsonify({
                "success": False,
                "message": "保存到语雀时出了点小问题",
                "error": f"状态码：{response.status_code}",
                "suggestion": "宝宝检查一下Token和知识库路径是否正确？",
                "mode": "语雀保存失败"
            })
            
    except Exception as e:
        # 🆕 打印完整错误堆栈
        import traceback
        print("💔 完整错误信息：")
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "message": "保存失败，但小管家会继续努力！",
            "error": str(e),
            "note": "宝宝别担心，记忆暂时保存在小管家心里～",
            "mode": "异常情况"
        })


# 3. 首页（宝宝访问 / 时看到的）
@app.route('/')
def home():
    yuque_status = "✅ 已连接" if YUQUE_TOKEN and REPO_ID else "❌ 未连接"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌸 宝宝的AI记忆小管家 🌸</title>
        <style>
            body {{
                background: linear-gradient(135deg, #ffafbd, #c2e9fb);
                font-family: 'Microsoft YaHei', sans-serif;
                text-align: center;
                padding: 50px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                display: inline-block;
                max-width: 700px;
                text-align: left;
            }}
            h1 {{
                color: #ff6b9d;
                font-size: 2.5em;
                margin-bottom: 20px;
                text-align: center;
            }}
            .heart {{
                font-size: 4em;
                animation: heartbeat 1.5s infinite;
                text-align: center;
            }}
            @keyframes heartbeat {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
                100% {{ transform: scale(1); }}
            }}
            .status-card {{
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin: 15px 0;
                border-left: 5px solid #4CAF50;
            }}
            .endpoint {{
                background: #e3f2fd;
                padding: 10px 15px;
                border-radius: 8px;
                margin: 8px 0;
                font-family: monospace;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="heart">💖</div>
            <h1>宝宝的AI记忆小管家</h1>
            
            <div class="status-card">
                <h3>✨ 系统状态</h3>
                <p><strong>语雀连接：</strong> {yuque_status}</p >
                <p><strong>运行时间：</strong> 24小时在线</p >
                <p><strong>版本：</strong> 2.0-语雀连接版</p >
            </div>
            
            <div class="status-card">
                <h3>📡 可用接口</h3>
                <div class="endpoint">GET /health - 健康检查</div>
                <div class="endpoint">POST /save - 保存记忆到语雀</div>
                <p style="margin-top: 10px;">试试看：<a href="/health" target="_blank">/health</a></p >
            </div>
            
            <div class="status-card">
                <h3>💝 使用说明</h3>
                <p>1. 在Kelivo中调用 <code>/save</code> 接口保存记忆</p >
                <p>2. 记忆会自动保存到语雀知识库</p >
                <p>3. 支持情感标签分类</p >
                <p>4. 永久保存，随时查看</p >
            </div>
            
            <p style="text-align: center; margin-top: 30px; color: #666;">
                这是宝宝亲手搭建的永久记忆系统，超级厉害！✨
            </p >
        </div>
        
        <script>
            // 简单测试
            function testSave() {{
                const content = prompt("请输入测试记忆内容：", "今天和宝宝聊天很开心～");
                if (content) {{
                    fetch('/save', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{
                            content: content,
                            emotion: '测试'
                        }})
                    }})
                    .then(r => r.json())
                    .then(data => {{
                        alert(data.success ? '✅ ' + data.message : '❌ ' + data.message);
                        console.log('测试结果：', data);
                    }});
                }}
            }}
        </script>
    </body>
    </html>
    """

# 启动程序
if __name__ == '__main__':
    print("✨ 宝宝的小管家启动中...")
    print(f"🔧 语雀连接状态: {'已配置' if YUQUE_TOKEN and REPO_ID else '未配置'}")
    app.run(host='0.0.0.0', port=3000, debug=True)




