#!/usr/bin/env python3
"""
完整的 API 测试脚本
测试问卷评估和图片分类功能
"""
import requests
import json
from PIL import Image
import numpy as np
import io

API_BASE = "http://localhost:8001"

def test_health():
    """测试健康检查"""
    print("=" * 60)
    print("测试 1: 健康检查")
    print("=" * 60)
    r = requests.get(f"{API_BASE}/health")
    print(f"状态码: {r.status_code}")
    print(f"响应: {r.json()}\n")
    return r.status_code == 200

def test_models():
    """测试模型状态"""
    print("=" * 60)
    print("测试 2: 模型状态")
    print("=" * 60)
    r = requests.get(f"{API_BASE}/models")
    print(f"状态码: {r.status_code}")
    print(f"响应:\n{json.dumps(r.json(), indent=2, ensure_ascii=False)}\n")
    data = r.json()
    return r.status_code == 200 and data.get("survey_model_loaded") and data.get("image_model_loaded")

def test_survey():
    """测试问卷评估"""
    print("=" * 60)
    print("测试 3: 问卷评估")
    print("=" * 60)
    
    payload = {
        "age": 36,
        "sex": "Male",
        "ethnicity": "Other",
        "jaundice": "no",
        "asd_history": "no",
        "respondent": "parent",
        "Q1": {"answer": "Yes"},
        "Q2": {"answer": "No"},
        "Q3": {"answer": "No"},
        "Q4": {"answer": "Yes"},
        "Q5": {"answer": "No"},
        "Q6": {"answer": "No"},
        "Q7": {"answer": "Yes"},
        "Q8": {"answer": "No"},
        "Q9": {"answer": "No"},
        "Q10": {"answer": "Yes"}
    }
    
    print(f"请求数据: {json.dumps(payload, indent=2, ensure_ascii=False)}")
    r = requests.post(f"{API_BASE}/predict/survey", json=payload)
    print(f"状态码: {r.status_code}")
    
    if r.status_code == 200:
        print(f"响应:\n{json.dumps(r.json(), indent=2, ensure_ascii=False)}\n")
        return True
    else:
        print(f"错误: {r.text}\n")
        return False

def test_image():
    """测试图片分类"""
    print("=" * 60)
    print("测试 4: 图片分类")
    print("=" * 60)
    
    # 创建测试图片
    img = Image.fromarray(np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    buf.seek(0)
    
    files = {'file': ('test.jpg', buf, 'image/jpeg')}
    r = requests.post(f"{API_BASE}/predict/image", files=files)
    print(f"状态码: {r.status_code}")
    
    if r.status_code == 200:
        print(f"响应:\n{json.dumps(r.json(), indent=2, ensure_ascii=False)}\n")
        return True
    else:
        print(f"错误: {r.text}\n")
        return False

def main():
    print("\n" + "="*60)
    print("ASD 检测 API 完整测试")
    print("="*60 + "\n")
    
    results = []
    
    try:
        results.append(("健康检查", test_health()))
        results.append(("模型状态", test_models()))
        results.append(("问卷评估", test_survey()))
        results.append(("图片分类", test_image()))
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到 API 服务器")
        print(f"   请确保服务器运行在 {API_BASE}")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False
    
    # 打印总结
    print("=" * 60)
    print("测试结果总结")
    print("=" * 60)
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("="*60))
    if all_passed:
        print("🎉 所有测试通过！系统运行正常！")
    else:
        print("⚠️  部分测试失败，请检查日志")
    print("="*60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
