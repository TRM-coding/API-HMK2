#!/usr/bin/env python3
import os
import json
import requests
import time

# Base URL for the API (can be overridden by setting API_BASE_URL environment variable)
BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:5000')

def wait_enter(message="请按 Enter 继续..."):
    input(f"\n{message}\n")

# --- Offer operations ---
def demo_create_offer():
    print("\nTask: Create Offer")
    url = f"{BASE_URL}/offers"
    offer_data = {
        "company_name": "TestCo",
        "position": "Engineer",
        "salary_min": None,
        "salary_max": None,
        "currency": "CNY",
        "location": None,
        "description": None,
        "tags": []
    }
    r = requests.post(url, json=offer_data)
    print("Create offer response:", r.status_code, r.text)
    data = r.json()
    offer_id = data.get("id")
    print("Created Offer ID:", offer_id)
    return offer_id


def demo_get_offer(offer_id):
    print("\nTask: Get Offer")
    url = f"{BASE_URL}/offers/{offer_id}"
    r = requests.get(url)
    print("Get offer response:", r.status_code, r.text)


def demo_update_offer(offer_id):
    print("\nTask: Update Offer")
    url = f"{BASE_URL}/offers/{offer_id}"
    r_before = requests.get(url)
    print("Offer before update:", r_before.json())
    update_payload = {
        "position": "Updated Engineer",
        "company_name": "TestCo"
    }
    r_update = requests.put(url, json=update_payload)
    print("Update offer response:", r_update.status_code, r_update.text)
    r_after = requests.get(url)
    print("Offer after update:", r_after.json())


def demo_delete_offer(offer_id):
    print("\nTask: Delete Offer")
    url = f"{BASE_URL}/offers/{offer_id}"
    r = requests.delete(url)
    print("Delete offer response:", r.status_code)

# --- Task operations ---
def demo_list_tasks():
    print("\nTask: List Tasks")
    url = f"{BASE_URL}/tasks"
    r = requests.get(url)
    print("List tasks response:", r.status_code, r.text)
    return r.json()


def demo_import_file():
    print("\nTask: Import File Task")
    sample_file = 'sample_offers.csv'
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write("company_name,position,salary_min,salary_max,currency,location,description,tags\n")
        f.write('DemoCorp,DemoDev,1000,2000,CNY,Beijing,"Demo description","[\"DemoTag\"]"\n')
    url = f"{BASE_URL}/tasks"
    files = {'file': (os.path.basename(sample_file), open(sample_file, 'rb'))}
    data = {'type': 'IMPORT'}
    r = requests.post(url, files=files, data=data)
    print("Import file response:", r.status_code, r.text)
    task_data = r.json()
    task_id = task_data.get("task_id")
    print("Created Task ID:", task_id)
    return task_id


def demo_get_task(task_id):
    print("\nTask: Get Task")
    url = f"{BASE_URL}/tasks/{task_id}"
    r = requests.get(url)
    print("Get task response:", r.status_code, r.text)


def demo_download_task(task_id):
    print("\nTask: Download Task Result")
    url = f"{BASE_URL}/tasks/{task_id}/download"
    r = requests.get(url)
    if r.status_code == 200:
        filename = "downloaded_result.csv"
        with open(filename, 'wb') as f:
            f.write(r.content)
        print("Downloaded file saved as:", filename)
    else:
        print("Download task response:", r.status_code, r.text)

# --- StatsLog operations ---
def demo_list_stats():
    print("\nTask: List StatsLogs")
    url = f"{BASE_URL}/stats_logs"
    r = requests.get(url)
    print("List stats_logs response:", r.status_code, r.text)


def demo_create_stats():
    print("\nTask: Create StatsLog")
    url = f"{BASE_URL}/stats_logs"
    stats_payload = {
        "date": "2025-01-01",
        "offer_count": 10,
        "avg_salary": "12345.67"
    }
    r = requests.post(url, json=stats_payload)
    print("Create stats_log response:", r.status_code, r.text)
    try:
        data = r.json()
    except json.decoder.JSONDecodeError:
        print("Failed to decode JSON response")
        return None
    log_id = data.get("log_id")
    print("Created StatsLog ID:", log_id)
    return log_id


def demo_get_stats(log_id):
    print("\nTask: Get StatsLog")
    url = f"{BASE_URL}/stats_logs/{log_id}"
    r = requests.get(url)
    print("Get stats_log response:", r.status_code, r.text)


def demo_update_stats(log_id):
    print("\nTask: Update StatsLog")
    url = f"{BASE_URL}/stats_logs/{log_id}"
    update_payload = {
        "offer_count": 20,
        "avg_salary": "20000.00"
    }
    r = requests.put(url, json=update_payload)
    print("Update stats_log response:", r.status_code, r.text)
    print("Updated fields: offer_count, avg_salary")


def demo_delete_stats(log_id):
    print("\nTask: Delete StatsLog")
    url = f"{BASE_URL}/stats_logs/{log_id}"
    r = requests.delete(url)
    print("Delete stats_log response:", r.status_code)

# --- Search operations ---
def demo_search_offers(query):
    print("\nTask: Search Offers")
    url = f"{BASE_URL}/offers"
    params = {"q": query}
    r = requests.get(url, params=params)
    print("Search offers response:", r.status_code, r.text)

# Add a new function to demonstrate that the Redis queue is processed
def demo_check_redis_queue():
    try:
        import redis
    except ImportError:
        print("redis module not installed, skipping Redis queue demonstration")
        return
    client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    queue_len = client.llen('task_queue')
    print(f"Redis queue 'task_queue' length: {queue_len}")
    if queue_len == 0:
        print("All tasks in Redis queue processed successfully.")
    else:
        print("There are pending tasks in Redis queue.")

# Utility functions for printing headers and footers
def print_header(operation):
    print("\n" + "="*60)
    print(f"本次操作：{operation}")
    print("="*60)
    


def print_footer(next_operation):
    print("\n" + "-"*60)
    print(f"下次操作：{next_operation}")
    print("-"*60)
    wait_enter("请按 Enter 继续...")

# --- Main flow ---
def main():
    print("Demo Runner starting...")
    wait_enter("请按 Enter 开始...")

    # --- Offer flow ---
    print_header("创建 Offer")
    offer_id = demo_create_offer()
    print("本次操作结果已显示。")
    print_footer("获取刚创建的 Offer")

    if offer_id:
        demo_get_offer(offer_id)
    else:
        print("No offer id found!")
    print_footer("更新 Offer 并展示更新结果")

    if offer_id:
        demo_update_offer(offer_id)
    print_footer("删除 Offer 并验证删除结果")

    if offer_id:
        demo_delete_offer(offer_id)
        demo_get_offer(offer_id)
    print_footer("创建多个导入任务")

    # --- Task flow ---
    task_ids = []
    for i in range(3):
        task_id = demo_import_file()
        task_ids.append(task_id)
    time.sleep(3)
    print_footer("查看所有任务列表")

    tasks = demo_list_tasks()
    print_footer("查看并下载第一个任务的结果")

    if task_ids and task_ids[0]:
        demo_get_task(task_ids[0])
        demo_download_task(task_ids[0])
    else:
        print("No task id captured!")
    print_footer("检查 StatsLogs 列表")

    # --- StatsLogs flow ---
    demo_list_stats()
    print_footer("创建新的 StatsLog")

    log_id = demo_create_stats()
    print_footer("查看刚创建的 StatsLog")

    if log_id:
        demo_get_stats(log_id)
    else:
        print("No stats_log id captured!")
    print_footer("更新 StatsLog 并展示修改结果")

    if log_id:
        demo_update_stats(log_id)
        demo_get_stats(log_id)
    print_footer("删除 StatsLog 并验证删除")

    if log_id:
        demo_delete_stats(log_id)
        demo_get_stats(log_id)
    # New step: Check Redis queue status
    print_footer("Redis 队列任务检查")
    demo_check_redis_queue()
    print_footer("搜索 Offer (预期无相关结果)")

    # --- New Search Demonstration ---
    demo_search_offers("NonExistentOffer")
    print("搜索失败原因: 未找到符合条件的offer")
    print_footer("创建可搜索的 Offer")

    print_header("创建可搜索的 Offer")
    search_offer_data = {
        "company_name": "SearchableOffer",
        "position": "Designer",
        "salary_min": None,
        "salary_max": None,        "currency": "USD",        "location": "Remote",        "description": "Offer for search demonstration",        "tags": []
    }
    url = f"{BASE_URL}/offers"
    r = requests.post(url, json=search_offer_data)
    if r.status_code in (200, 201):
        print("创建搜索Offer成功:", r.text)
    else:
        print("创建搜索Offer失败:", r.status_code, r.text)

    print_footer("搜索 Offer (预期成功)")
    demo_search_offers("SearchableOffer")

    wait_enter("所有操作执行完毕，按 Enter 退出 demo.")

if __name__ == "__main__":
    main()
