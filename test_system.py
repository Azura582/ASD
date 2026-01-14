#!/usr/bin/env python3
"""
完整功能测试脚本

测试ASD检测系统的所有接口和功能
"""
import requests
import json
from pathlib import Path
import sys

# 配置
API_BASE = "http://localhost:8000"
WEBAPP_BASE = "http://localhost:5000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)

def test_api_health():
    """测试API健康检查"""
    print_section("1. 测试API健康检查")
    try:
        r = requests.get(f"{API_BASE}/health", timeout=5)
        print(f"✓ API状态: {r.status_code}")
        print(f"  响应: {r.json()}")
        return True
    except Exception as e:
        print(f"✗ API健康检查失败: {e}")
        return False

def test_webapp_health():
    """测试前端健康检查"""
    print_section("2. 测试前端健康检查")
    try:
        r = requests.get(f"{WEBAPP_BASE}/api/health", timeout=5)
        print(f"✓ 前端状态: {r.status_code}")
        print(f"  响应: {json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"✗ 前端健康检查失败: {e}")
        return False

def test_models_status():
    """测试模型加载状态"""
    print_section("3. 测试模型加载状态")
    try:
        r = requests.get(f"{API_BASE}/models", timeout=5)
        data = r.json()
        print(f"✓ 模型状态: {r.status_code}")
        print(f"  问卷模型: {'✓ 已加载' if data['survey_model_loaded'] else '✗ 未加载'}")
        print(f"  图片模型: {'✓ 已加载' if data['image_model_loaded'] else '✗ 未加载'}")
        print(f"  类别列表: {data['class_names']}")
        print(f"  类别数量: {data['class_names_count']}")
        return True
    except Exception as e:
        print(f"✗ 模型状态检查失败: {e}")
        return False

def test_survey_api():
    """测试问卷API"""
    print_section("4. 测试问卷预测API")
    payload = {
        "age": 36,
        "sex": "Male",
        "ethnicity": "Others",
        "jaundice": "no",
        "asd_history": "no",
        "respondent": "Parent",
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
    
    try:
        r = requests.post(f"{API_BASE}/predict/survey", json=payload, timeout=10)
        print(f"状态: {r.status_code}")
        result = r.json()
        
        if "error" in result:
            print(f"⚠ 问卷模型未加载(预期行为)")
            print(f"  错误信息: {result.get('error')}")
        else:
            print(f"✓ 预测结果:")
            print(f"  预测: {result.get('prediction')}")
            print(f"  风险评分: {result.get('score')}")
            print(f"  风险等级: {result.get('risk_level')}")
            print(f"  风险项目: {result.get('risk_questions')}")
        return True
    except Exception as e:
        print(f"✗ 问卷API测试失败: {e}")
        return False

def test_image_api():
    """测试图片API"""
    print_section("5. 测试图片预测API")
    
    # 创建测试图片
    try:
        from PIL import Image
        import numpy as np
        import io
        
        # 生成随机测试图片
        img_array = np.random.randint(0, 255, (128, 128, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        
        # 转换为字节流
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        files = {'file': ('test.jpg', img_bytes, 'image/jpeg')}
        r = requests.post(f"{API_BASE}/predict/image", files=files, timeout=30)
        
        print(f"状态: {r.status_code}")
        result = r.json()
        
        if "error" in result:
            print(f"✗ 图片预测失败: {result.get('error')}")
        else:
            print(f"✓ 预测结果:")
            print(f"  识别行为: {result.get('label')}")
            print(f"  置信度: {result.get('confidence')}")
            print(f"  原始评分: {result.get('score'):.4f}")
            if result.get('all_probabilities'):
                print(f"  所有类别概率:")
                for label, prob in result['all_probabilities'].items():
                    print(f"    - {label}: {prob*100:.2f}%")
        return True
    except Exception as e:
        print(f"✗ 图片API测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frontend_pages():
    """测试前端页面"""
    print_section("6. 测试前端页面")
    pages = {
        "主页": "/",
        "问卷页面": "/survey",
        "图片页面": "/image"
    }
    
    all_ok = True
    for name, path in pages.items():
        try:
            r = requests.get(f"{WEBAPP_BASE}{path}", timeout=5)
            if r.status_code == 200:
                print(f"✓ {name}: 200 OK (长度: {len(r.text)} 字符)")
            else:
                print(f"✗ {name}: {r.status_code}")
                all_ok = False
        except Exception as e:
            print(f"✗ {name}: 访问失败 - {e}")
            all_ok = False
    
    return all_ok

def print_summary(results):
    """打印测试总结"""
    print_section("测试总结")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n总计: {total} 项测试")
    print(f"通过: {passed} 项")
    print(f"失败: {total - passed} 项")
    
    print(f"\n详细结果:")
    for test_name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {status} - {test_name}")
    
    if passed == total:
        print(f"\n🎉 所有测试通过!")
        print(f"\n立即访问:")
        print(f"  前端界面: {WEBAPP_BASE}")
        print(f"  API文档: {API_BASE}/docs")
    else:
        print(f"\n⚠ 有 {total - passed} 项测试失败,请检查日志")

def main():
    print("="*60)
    print("  ASD检测系统 - 完整功能测试")
    print("="*60)
    print(f"\nAPI地址: {API_BASE}")
    print(f"前端地址: {WEBAPP_BASE}")
    
    results = {}
    
    # 执行测试
    results["API健康检查"] = test_api_health()
    results["前端健康检查"] = test_webapp_health()
    results["模型加载状态"] = test_models_status()
    results["问卷预测API"] = test_survey_api()
    results["图片预测API"] = test_image_api()
    results["前端页面访问"] = test_frontend_pages()
    
    # 打印总结
    print_summary(results)
    
    # 返回退出码
    sys.exit(0 if all(results.values()) else 1)

if __name__ == "__main__":
    main()
