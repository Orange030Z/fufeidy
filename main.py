import requests
import base64
import json
import re
import os

# 配置：目标 Gist ID
GIST_ID = "4a5958c12564fabe91effe236e4c103c"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"

def extract_nodes(text):
    """多重增强提取逻辑，确保能从代码块中抠出链接"""
    if not text: return []
    
    # 匹配 vmess/vless/trojan/ss 的正则
    pattern = r'(vmess|vless|trojan|ss)://[^\s"\'<>]+'
    
    # 尝试1：直接匹配明文链接
    nodes = re.findall(pattern, text, re.IGNORECASE)
    
    # 尝试2：如果没找到，尝试整段 Base64 解码后再匹配
    if not nodes:
        try:
            clean_text = re.sub(r'\s+', '', text)
            missing_padding = len(clean_text) % 4
            if missing_padding: clean_text += '=' * (4 - missing_padding)
            decoded = base64.b64decode(clean_text).decode('utf-8', errors='ignore')
            nodes = re.findall(pattern, decoded, re.IGNORECASE)
        except: pass
        
    # 尝试3：按行扫描（处理每一行都是一个独立 Base64 的情况）
    if not nodes:
        for line in text.splitlines():
            line = line.strip()
            if len(line) > 20:
                try:
                    # 尝试解码单行
                    line_dec = base64.b64decode(line + '==').decode('utf-8', errors='ignore')
                    nodes.extend(re.findall(pattern, line_dec, re.IGNORECASE))
                except: pass
    
    return list(set(nodes)) # 去重

def main():
    print("🚀 正在请求 Gist API...")
    try:
        resp = requests.get(GIST_API_URL, timeout=15)
        if resp.status_code != 200:
            print(f"❌ 错误: 无法访问 API ({resp.status_code})")
            return
            
        files = resp.json().get('files', {})
        found_any = False
        
        for filename, info in files.items():
            # 获取内容
            content = info.get('content', '')
            if info.get('truncated'):
                content = requests.get(info.get('raw_url')).text
            
            # 提取节点
            nodes = extract_nodes(content)
            
            if not nodes:
                print(f"⏩ 跳过文件: {filename} (未发现节点)")
                continue
            
            found_any = True
            # 文件名处理：去掉空格，防止 Git 报错
            safe_filename = filename.replace(" ", "_").replace("/", "-")
            
            # 合并并转为 Base64 订阅格式
            node_text = "\n".join(nodes)
            b64_content = base64.b64encode(node_text.encode()).decode()
            
            # 写入本地文件
            with open(f"{safe_filename}.txt", "w", encoding="utf-8") as f:
                f.write(b64_content)
            print(f"✅ 已成功处理: {safe_filename}.txt (发现 {len(nodes)} 个节点)")
            
        if not found_any:
            print("❌ 警告：该 Gist 中没有任何代码块包含有效节点！")
            
    except Exception as e:
        print(f"❌ 运行异常: {e}")

if __name__ == "__main__":
    main()
