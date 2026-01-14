"""
webapp.py - Flask前端应用

提供Web界面用于:
  1. ASD问卷调查
  2. 图片上传检测
  
整合两种检测方式到统一界面
"""
from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
from pathlib import Path

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# API后端地址(FastAPI服务)
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

# 问卷问题列表(中文)
QUESTIONS = [
    {"id": "Q1", "text": "孩子是否会看着你的眼睛?"},
    {"id": "Q2", "text": "当你指向房间另一侧的东西时,孩子是否会看过去?"},
    {"id": "Q3", "text": "孩子是否喜欢爬到物体上(如楼梯)?"},
    {"id": "Q4", "text": "孩子是否喜欢玩躲猫猫游戏?"},
    {"id": "Q5", "text": "孩子是否会假装玩耍(例如假装用玩具茶杯喝茶)?"},
    {"id": "Q6", "text": "孩子是否会用食指指向想要的东西?"},
    {"id": "Q7", "text": "孩子是否会用食指指向感兴趣的东西?"},
    {"id": "Q8", "text": "孩子是否对其他孩子感兴趣?"},
    {"id": "Q9", "text": "孩子是否会把东西拿给你看?"},
    {"id": "Q10", "text": "当你叫孩子名字时,他/她是否会回应?"}
]


@app.route('/')
def index():
    """主页 - 显示功能选择"""
    return render_template('index.html')


@app.route('/survey')
def survey_page():
    """问卷页面"""
    return render_template('survey.html', questions=QUESTIONS)


@app.route('/image')
def image_page():
    """图片上传页面"""
    return render_template('image.html')


@app.route('/api/survey', methods=['POST'])
def submit_survey():
    """处理问卷提交"""
    try:
        data = request.json
        # 调用FastAPI后端
        response = requests.post(f"{API_BASE}/predict/survey", json=data, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"后端调用失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@app.route('/api/image', methods=['POST'])
def submit_image():
    """处理图片上传"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "未上传文件"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "文件名为空"}), 400
        
        # 调用FastAPI后端
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(f"{API_BASE}/predict/image", files=files, timeout=30)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"后端调用失败: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"服务器错误: {str(e)}"}), 500


@app.route('/api/health')
def health():
    """健康检查"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        backend_status = response.json() if response.status_code == 200 else {"status": "error"}
        return jsonify({
            "frontend": "ok",
            "backend": backend_status
        })
    except Exception as e:
        return jsonify({
            "frontend": "ok",
            "backend": {"status": "error", "detail": str(e)}
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
