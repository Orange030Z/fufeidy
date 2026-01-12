import requests
import os

def main():
    print("🚀 强制抓取流程启动...")
    
    # 目标 Gist 地址
    gist_id = "4a5958c12564fabe91effe236e4c103c"
    url = f"https://api.github.com/gists/{gist_id}"
    
    # 强制创建一个标记文件，证明脚本运行了
    with open("RUN_LOG.txt", "w") as f:
        f.write("Last Run: " + str(os.popen('date').read()))

    try:
        # 使用特定的 User-Agent 模拟浏览器请求，防止被 GitHub 拦截
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        resp = requests.get(url, headers=headers, timeout=30)
        print(f"📡 接口响应码: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"❌ 无法读取 Gist 数据，错误代码: {resp.status_code}")
            return
            
        files = resp.json().get('files', {})
        if not files:
            print("❌ Gist 内没有发现任何文件块")
            return

        print(f"📁 准备处理 {len(files)} 个文件块")

        for filename, info in files.items():
            content = info.get('content', '')
            if content:
                # 强行处理文件名：去掉空格和特殊字符
                clean_name = filename.replace(" ", "_").replace("/", "-")
                if not clean_name.endswith(".txt"):
                    clean_name += ".txt"
                
                # 写入明文
                with open(clean_name, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 已强制写入本地文件: {clean_name}")
            else:
                print(f"⏩ 跳过空内容块: {filename}")

    except Exception as e:
        print(f"💥 发生严重错误: {str(e)}")

if __name__ == "__main__":
    main()
