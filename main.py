import requests
import base64
import json
import yaml
import re
import os
from urllib.parse import urlparse

# --- 配置 ---
# Gist ID 提取自你提供的链接
GIST_ID = "4a5958c12564fabe91effe236e4c103c"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

def fetch_gist_files():
    """通过 API 获取 Gist 中的所有文件信息"""
    try:
        resp = requests.get(GIST_API_URL, timeout=15)
        if resp.status_code != 200:
            print(f"❌ 无法访问 Gist API: {resp.status_code}")
            return {}
        return resp.json().get('files', {})
    except Exception as e:
        print(f"❌ 请求异常: {e}")
        return {}

def extract_nodes(text):
    """从文本中提取节点链接，支持明文或 Base64 混合"""
    # 尝试 Base64 解码逻辑
    if "://" not in text and len(text) > 20:
        try:
            missing_padding = len(text) % 4
            if missing_padding: text += '=' * (4 - missing_padding)
            decoded = base64.b64decode(text).decode('utf-8', errors='ignore')
            if "://" in decoded: text = decoded
        except: pass
    
    # 匹配常见协议
    pattern = r'(vmess|vless|trojan|ss)://[^\s"\'<>]+'
    return re.findall(pattern, text, re.IGNORECASE)

def save_as_clash(nodes, filename):
    """(可选) 将节点转换为简易 Clash 配置"""
    # 这里仅作为占位，如果需要完整转换逻辑可添加
    # 为保持演示简洁，我们主要生成 TXT 订阅
    pass

def main():
    files = fetch_gist_files()
    if not files:
        print("未找到任何文件")
        return

    print(f"开始处理，共发现 {len(files)} 个文件块...")

    for fname, info in files.items():
        # 原始文件名（例如：健康中心618pro）
        content = info.get('content', '')
        # 如果内容太长 API 可能没直接给 content，需通过 raw_url 获取
        if info.get('truncated'):
            content = requests.get(info.get('raw_url')).text
        
        nodes = extract_nodes(content)
        
        if not nodes:
            print(f"跳过空文件: {fname}")
            continue

        # 1. 保存为明文列表 (文件名: 健康中心618pro_plain.txt)
        safe_name = fname.replace(" ", "_") # 替换空格防止出错
        with open(f"{safe_name}_plain.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(nodes))

        # 2. 保存为 Base64 订阅 (文件名: 健康中心618pro.txt)
        b64_content = base64.b64encode("\n".join(nodes).encode()).decode()
        with open(f"{safe_name}.txt", "w", encoding="utf-8") as f:
            f.write(b64_content)

        print(f"✅ 已生成: {safe_name}.txt (节点数: {len(nodes)})")

if __name__ == "__main__":
    main()
