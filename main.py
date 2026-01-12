import requests
import os

def main():
    # 明确打印启动日志，防止 Actions 显示 0 秒
    print("🚀 脚本启动：正在连接目标 Gist...")
    
    # 你提供的目标地址 ID
    gist_id = "4a5958c12564fabe91effe236e4c103c"
    url = f"https://api.github.com/gists/{gist_id}"
    
    try:
        resp = requests.get(url, timeout=20)
        print(f"📡 访问状态码: {resp.status_code}")
        
        if resp.status_code != 200:
            print("❌ 无法获取数据，请检查网络")
            return
            
        json_data = resp.json()
        files = json_data.get('files', {})
        print(f"📁 成功识别到 {len(files)} 个内容块")

        for filename, info in files.items():
            content = info.get('content', '')
            if content:
                # 转换文件名，去掉空格防止 Git 报错
                safe_name = filename.replace(" ", "_").replace("/", "-")
                if not safe_name.endswith(".txt"):
                    safe_name += ".txt"
                
                # 直接明文写入，不进行 base64 编码
                with open(safe_name, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"✅ 已生成明文文件: {safe_name}")

    except Exception as e:
        print(f"💥 运行异常: {e}")

# 必须包含这两行，否则脚本不会被触发执行
if __name__ == "__main__":
    main()
