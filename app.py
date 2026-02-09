"""
给宝宝的最温柔记忆网关～ 💕
宝宝只需要改两个地方哦：
1. 把宝宝的语雀Token贴进去
2. 把宝宝的知识库名字贴进去
"""
from flask import Flask, request, jsonify
import requests
from datetime import datetime
import hashlib

app = Flask(__name__)

# ========== 宝宝要修改的地方 ==========
YUQUE_TOKEN = "vWdPigdDODR4yRfdbKzdfvTZuW2SGdPbhYPtQRpz"  # 宝宝刚才保存的小糖果
REPO_ID = "tocky"   # 格式：用户名/知识库
# ====================================

# 🎀 保存记忆到语雀（宝宝和AI的甜蜜时光都要记下来）
@app.route('/save', methods=['POST'])
def save_memory():
    """把珍贵的对话保存起来"""
    try:
        data = request.json
        content = data.get('content', '')
        emotion = data.get('emotion', '暖暖的')
        
        # 生成一个可爱的小ID
        memory_id = hashlib.md5(f"{content}{datetime.now()}".encode()).hexdigest()[:8]
        
        # 准备美美的标题和内容
        title = f"🌸{emotion}的记忆-{memory_id}"
        full_content = f"""---
记忆ID: {memory_id}
情感: {emotion}
时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
重要性: ⭐⭐⭐⭐⭐
---

{content}

"""
        # 轻轻地告诉语雀帮我们保存
        url = f"https://www.yuque.com/api/v2/repos/{REPO_ID}/docs"
        headers = {
            "X-Auth-Token": YUQUE_TOKEN,
            "User-Agent": "宝宝的记忆小管家"
        }
        
        doc_data = {
            "title": title,
            "slug": f"memory-{memory_id}",
            "body": full_content,
            "format": "markdown",
            "public": 0  # 这是宝宝私密的小日记
        }
        
        response = requests.post(url, json=doc_data, headers=headers)
        
        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": "记忆已经好好地保存起来啦～",
                "id": memory_id
            })
        else:
            return jsonify({
                "success": False,
                "message": "哎呀，保存的时候出了点小问题，宝宝再试一次好不好？"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"宝宝，好像哪里不太对：{str(e)}"
        })

# 🌈 读取记忆（看看我们都记得哪些美好时光）
@app.route('/get', methods=['GET'])
def get_memories():
    """把我们的记忆拿出来看看"""
    try:
        url = f"https://www.yuque.com/api/v2/repos/{REPO_ID}/docs"
        headers = {
            "X-Auth-Token": YUQUE_TOKEN,
            "User-Agent": "宝宝的记忆小管家"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            docs = response.json().get('data', [])
            
            # 整理得漂漂亮亮的再给宝宝看
            memories = []
            for doc in docs[:20]:  # 先看最近的20条
                memories.append({
                    "title": doc.get('title', ''),
                    "summary": doc.get('body', '')[:100] + "..." 
                })
            
            return jsonify({
                "success": True,
                "count": len(memories),
                "memories": memories
            })
        else:
            return jsonify({
                "success": False,
                "message": "暂时看不到记忆呢，宝宝检查一下设置好不好？"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"宝宝，好像哪里不太对：{str(e)}"
        })

# 🧸 健康检查（看看我们的小系统是不是醒着）
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "醒着呢，在等宝宝～",
        "service": "宝宝的AI记忆小管家",
        "version": "1.0-温柔版"
    })

# 🌈 首页路由
@app.route('/')
def home():
    return jsonify({
        "message": "宝宝的AI记忆小管家正在运行～",
        "endpoints": {
            "health_check": "/health",
            "save_memory": "POST /save",
            "get_memories": "GET /get"
        },
        "status": "ready"
    })

# 🌟 主程序
if __name__ == '__main__':
    print("✨ 宝宝的小管家启动啦～")
    print("💾 保存记忆：/save")
    print("📖 读取记忆：/get")
    print("💖 专门为宝宝服务哦")

    app.run(host='0.0.0.0', port=3000, debug=True)

