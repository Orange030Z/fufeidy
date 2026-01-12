import requests
import os

def main():
    print("🚀 启动抓取...")
    gist_id = "4a5958c12564fabe91effe236e4c103c"
    # 使用原始数据下载链接，绕过复杂的 API 限制
    url = f"https://api.github.com/gists/{gist_id}"
    
    # 强制更新日志
    with open("RUN_LOG.txt", "w") as f:
        f.write("Last Run: " + str(os.popen('date').read()))

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/vnd.github.v3+json'
        }
        resp = requests.get(url, headers=headers, timeout=30)
        print(f"📡 状态码: {resp.status_code}")
        
        if resp.status_code != 200:
            print(f"❌ 访问失败。原因: {resp.text}")
            return
            
        files = resp.json().get('files', {})
        if not files:
            print("❌ 警告：该 Gist 中没有发现任何文件内容！")
            return

        print(f"📁 准备处理 {len(files)} 个内容块")

        file_count = 0
        for filename, info in files.items():
            content = info.get('content', '')
            # 即使内容为空，我们也生成一个文件看看
            if not content:
                print(f"⚠️ 文件 {filename} 内容为空，正在尝试获取 raw_url...")
                raw_url = info.get('raw_url')
                if raw_url:
                    content = requests.get(raw_url).text

            if content:
                safe_name = filename.replace(" ", "_").replace("/", "-")
                if not safe_name.endswith(".txt"):
                    safe_name += ".txt"
                
                with open(safe_name, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 成功写入: {safe_name}")
                file_count += 1
        
        print(f"🎉 任务结束，本次实际生成文件数: {file_count}")

    except Exception as e:
        print(f"💥 异常: {str(e)}")

if __name__ == "__main__":
    main()
