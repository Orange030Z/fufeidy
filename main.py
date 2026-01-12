import requests
import os

def main():
    print("🚀 启动强制抓取程序...")
    gist_id = "4a5958c12564fabe91effe236e4c103c"
    url = f"https://api.github.com/gists/{gist_id}"
    
    # 强制创建一个测试文件，证明脚本有写权限
    with open("test_connection.txt", "w") as f:
        f.write("Connection Success")

    try:
        print(f"📡 正在连接 Gist: {gist_id}")
        resp = requests.get(url, timeout=15)
        
        if resp.status_code != 200:
            print(f"❌ 访问失败，状态码: {resp.status_code}")
            return
            
        files = resp.json().get('files', {})
        print(f"📁 成功获取到 {len(files)} 个文件块")

        for filename, info in files.items():
            content = info.get('content', '')
            if content:
                # 强制格式化文件名
                safe_name = filename.replace(" ", "_").replace("/", "-")
                if not safe_name.endswith(".txt"):
                    safe_name += ".txt"
                
                # 执行明文写入
                with open(safe_name, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 强制生成: {safe_name} ({len(content)} 字符)")
        
        print("🎉 所有文件处理完毕！")

    except Exception as e:
        print(f"💥 运行崩溃: {str(e)}")

# 必须保留这两行，否则脚本永远不会执行
if __name__ == "__main__":
    main()
