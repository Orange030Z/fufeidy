import requests
import os

def main():
    print("🚀 正在执行暴力抓取...")
    
    # 1. 强制写入日志（你之前能看到这个，说明权限没问题）
    with open("log.txt", "w") as f:
        f.write(f"Run at: {os.popen('date').read()}")

    # 2. 映射表：把 Gist 里的中文名 强行转为 仓库里的英文名
    # 这样可以彻底解决 git add 找不到文件的问题
    targets = {
        "nodes_health.txt": "健康中心618pro",
        "nodes_cheers1.txt": "干杯1",
        "nodes_cheers6.txt": "干杯6",
        "nodes_cheers12.txt": "干杯12"
    }

    base_url = "https://gist.githubusercontent.com/smile6-6/4a5958c12564fabe91effe236e4c103c/raw/"

    success_count = 0
    for local_name, remote_name in targets.items():
        try:
            url = f"{base_url}{remote_name}"
            print(f"📡 正在拉取: {remote_name} -> {local_name}")
            r = requests.get(url, timeout=15)
            
            if r.status_code == 200 and len(r.text) > 10:
                with open(local_name, "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"✅ 成功写入文件: {local_name}")
                success_count += 1
            else:
                print(f"❌ 抓取失败: {remote_name}, 状态码: {r.status_code}")
        except Exception as e:
            print(f"💥 错误: {e}")

    print(f"🏁 抓取结束，共生成 {success_count} 个节点文件。")

if __name__ == "__main__":
    main()
