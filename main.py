import requests
import os

def main():
    print("🚀 脚本启动：准备抓取 Gist 数据...")
    gist_id = "4a5958c12564fabe91effe236e4c103c"
    url = f"https://api.github.com/gists/{gist_id}"
    
    try:
        resp = requests.get(url, timeout=15)
        print(f"📡 API 响应状态码: {resp.status_code}")
        
        if resp.status_code != 200:
            print("❌ 无法连接到 GitHub API")
            return
            
        files = resp.json().get('files', {})
        print(f"📁 发现 {len(files)} 个文件块")

        for filename, info in files.items():
            content = info.get('content', '')
            if not content:
                print(f"⏩ 跳过空文件: {filename}")
                continue
            
            # 格式化文件名：去掉空格，确保合法
            safe_filename = filename.replace(" ", "_").replace("/", "-")
            if not safe_filename.endswith(".txt"):
                safe_filename += ".txt"
            
            # 强制写入明文内容
            with open(safe_filename, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ 成功写入文件: {safe_filename} (大小: {len(content)} 字符)")
            
    except Exception as e:
        print(f"💥 运行发生异常: {str(e)}")

if __name__ == "__main__":
    main()
