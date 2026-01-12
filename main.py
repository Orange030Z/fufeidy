import requests
import os

def main():
    print("🚀 正在执行暴力抓取...")
    
    # 强制写入日志
    with open("log.txt", "w") as f:
        f.write(f"Run at: {os.popen('date').read()}")

    # 目标链接字典：[文件名, Gist内的原始文件名]
    targets = {
        "nodes_health.txt": "健康中心618pro",
        "nodes_cheers1.txt": "干杯1",
        "nodes_cheers6.txt": "干杯6",
        "nodes_cheers12.txt": "干杯12"
    }

    base_url = "https://gist.githubusercontent.com/smile6-6/4a5958c12564fabe91effe236e4c103c/raw/"

    for local_name, remote_name in targets.items():
        try:
            url = f"{base_url}{remote_name}"
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and len(r.text) > 10:
                with open(local_name, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"✅ 写入成功: {local_name}")
            else:
                print(f"❌ 抓取失败: {remote_name}, 状态码: {r.status_code}")
        except Exception as e:
            print(f"💥 错误: {e}")

if __name__ == "__main__":
    main()
