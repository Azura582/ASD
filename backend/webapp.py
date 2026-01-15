"""
webapp.py - Flask前端应用

提供Web界面用于:
  1. ASD问卷调查
  2. 图片上传检测
  
整合两种检测方式到统一界面
"""
from flask import Flask, render_template, request, jsonify, send_from_directory, session, redirect, url_for
import requests
import os
from pathlib import Path

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# API后端地址(FastAPI服务)
API_BASE = os.environ.get("API_BASE", "http://localhost:8000")

# 问卷问题列表(中文)
QUESTIONS = [
    {"id": "Q1", "text": "Will the child look into your eyes?"},
    {"id": "Q2", "text": "When you point to something on the other side of the room, does the child look over?"},
    {"id": "Q3", "text": "Does the child like to climb onto objects (such as stairs)?"},
    {"id": "Q4", "text": "Does the child like playing hide-and-seek?"},
    {"id": "Q5", "text": "Does the child pretend to play (for example, pretending to drink tea from a toy teacup)?"},
    {"id": "Q6", "text": "Does the child point to things they want with their index finger?"},
    {"id": "Q7", "text": "Does the child point to things they're interested in using their index finger?"},
    {"id": "Q8", "text": "Is the child interested in other children?"},
    {"id": "Q9", "text": "Does the child show things to you?"},
    {"id": "Q10", "text": "When you call your child's name, does he/she respond?"}
]


@app.route('/')
def index():
    """主页 - 显示功能选择"""
    return render_template('index.html')


@app.route('/survey')
@app.route('/survey/<int:step>')
def survey_page(step=0):
    """问卷页面 - 多步骤"""
    # 重置或初始化 session
    if step == 0 and request.args.get('reset') == '1':
        session.pop('survey_answers', None)
        session.pop('survey_basic', None)
    
    # 步骤0是基本信息
    if step == 0:
        return render_template('survey.html', step=0, total_steps=len(QUESTIONS))
    
    # 步骤1-10是问题
    if step < 1 or step > len(QUESTIONS):
        return redirect(url_for('survey_page', step=1))
    
    question = QUESTIONS[step - 1]
    return render_template('survey.html', 
                         question=question,
                         step=step,
                         total_steps=len(QUESTIONS))


@app.route('/survey/save_basic', methods=['POST'])
def save_basic_info():
    """保存基本信息"""
    try:
        data = request.json
        session['survey_basic'] = data
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/survey/save_answer', methods=['POST'])
def save_answer():
    """保存单个答案"""
    try:
        data = request.json
        if 'survey_answers' not in session:
            session['survey_answers'] = {}
        session['survey_answers'][data['question_id']] = data['answer']
        session.modified = True
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/image')
def image_page():
    """图片上传页面"""
    return render_template('image.html')


@app.route('/api/survey', methods=['POST'])
def submit_survey():
    """处理问卷提交"""
    try:
        # 从 session 获取基本信息和答案
        basic_info = session.get('survey_basic', {})
        answers = session.get('survey_answers', {})
        
        # 构建完整数据
        data = {
            "age": basic_info.get('age', 36),
            "sex": basic_info.get('sex', 'Male'),
            "ethnicity": basic_info.get('ethnicity', 'Others'),
            "jaundice": basic_info.get('jaundice', 'no'),
            "asd_history": basic_info.get('asd_history', 'no'),
            "respondent": basic_info.get('respondent', 'Parent')
        }
        
        # 添加问题答案
        for q_id, answer in answers.items():
            data[q_id] = {"answer": answer}
        
        # 调用FastAPI后端
        response = requests.post(f"{API_BASE}/predict/survey", json=data, timeout=10)
        response.raise_for_status()
        
        # 清除 session
        session.pop('survey_answers', None)
        session.pop('survey_basic', None)
        
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"backend failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"server wrong: {str(e)}"}), 500


@app.route('/api/image', methods=['POST'])
def submit_image():
    """处理图片上传"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "not upload file"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "file name is empty"}), 400
        
        # 调用FastAPI后端
        files = {'file': (file.filename, file.stream, file.content_type)}
        response = requests.post(f"{API_BASE}/predict/image", files=files, timeout=30)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"backend failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"server wrong: {str(e)}"}), 500


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
