import requests
import os

def main():
    print("🚀 开始请求数据 (明文模式)...")
    # 目标 Gist ID
    url = "https://api.github.com/gists/4a5958c12564fabe91effe236e4c103c"
    
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            print(f"❌ API 请求失败: {resp.status_code}")
            return
            
        files = resp.json().get('files', {})
        if not files:
            print("❌ 未发现任何文件块")
            return

        for name, info in files.items():
            content = info.get('content', '')
            if not content:
                continue
                
            # 处理文件名，确保没有空格和斜杠
            safe_name = name.replace(" ", "_").replace("/", "-")
            filename = f"{safe_name}.txt"
            
            # 直接写入明文内容
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 成功生成明文文件: {filename}")
            
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    main()
