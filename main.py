import requests
import os

def main():
    print("🚀 强力抓取模式启动...")
    
    # 你的目标 Gist 地址对应的原始数据基础 URL
    base_url = "https://gist.githubusercontent.com/smile6-6/4a5958c12564fabe91effe236e4c103c/raw/"
    
    # 强制更新时间戳，证明脚本在跑
    with open("RUN_LOG.txt", "w", encoding="utf-8") as f:
        f.write(f"Last Attempt: {os.popen('date').read()}")

    # 定义我们要强抓的文件名列表（来自你提供的 Gist）
    target_files = [
        "健康中心618pro",
        "干杯1",
        "干杯6",
        "干杯12"
    ]

    success_count = 0
    for name in target_files:
        try:
            # 拼接原始文件的下载链接
            file_url = f"{base_url}{name}"
            print(f"📡 正在强抓: {name}...")
            
            resp = requests.get(file_url, timeout=20)
            if resp.status_code == 200 and len(resp.text) > 10:
                # 写入明文文件
                with open(f"{name}.txt", "w", encoding="utf-8") as f:
                    f.write(resp.text)
                print(f"✅ 成功生成: {name}.txt")
                success_count += 1
            else:
                print(f"❌ 抓取失败或内容过短: {name}")
        except Exception as e:
            print(f"💥 抓取 {name} 出错: {e}")

    print(f"🏁 任务结束，共抓取到 {success_count} 个节点文件。")

if __name__ == "__main__":
    main()
