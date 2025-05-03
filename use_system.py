import requests
import json
import os

BASE_URL = os.environ.get('API_BASE_URL', 'http://127.0.0.1:5000')

# -- default payloads, feel free to change --
DEFAULT_OFFER = {
    "company_name": "TestCo",
    "position": "Engineer",
    "salary_min": None,
    "salary_max": None,
    "currency": "CNY",
    "location": None,
    "description": None,
    "tags": []
}

DEFAULT_TASK_JSON = {
    "task_id": "custom-task-1234",
    "type": "IMPORT",
    "status": "PENDING"
}

DEFAULT_STATS = {
    "date": "2025-01-01",
    "offer_count": 10,
    "avg_salary": "12345.67"
}

# -- offer endpoints --
def list_offers():
    # GET /offers
    # 用法：列出所有招聘信息
    try:
        r = requests.get(f"{BASE_URL}/offers")
        print(r.status_code, json.dumps(r.json(), indent=2))
    except requests.exceptions.ConnectionError as e:
        print("Connection error: ", e)

def create_offer():
    # POST /offers
    # 用法：创建一个新招聘信息
    r = requests.post(f"{BASE_URL}/offers", json=DEFAULT_OFFER)
    print(r.status_code, json.dumps(r.json(), indent=2))

def get_offer():
    # GET /offers/{offer_id}
    # 用法：根据提供的 OFFER ID 获取招聘信息详情
    oid = input("Offer ID: ")
    r = requests.get(f"{BASE_URL}/offers/{oid}")
    print(r.status_code, r.text)

def update_offer():
    # PUT /offers/{offer_id}
    # 用法：更新指定 OFFER 的信息（需传入 JSON 格式的数据）
    oid = input("Offer ID: ")
    payload = json.loads(input(f"JSON payload (default={DEFAULT_OFFER}): ") or json.dumps(DEFAULT_OFFER))
    r = requests.put(f"{BASE_URL}/offers/{oid}", json=payload)
    print(r.status_code, r.text)

def delete_offer():
    # DELETE /offers/{offer_id}
    # 用法：删除指定 OFFER
    oid = input("Offer ID: ")
    r = requests.delete(f"{BASE_URL}/offers/{oid}")
    print(r.status_code)

def search_offers():
    # GET /offers?q=<query>
    # 用法：根据输入关键词搜索招聘信息
    query = input("Enter search query: ")
    params = {'q': query}
    r = requests.get(f"{BASE_URL}/offers", params=params)
    print(r.status_code, json.dumps(r.json(), indent=2))

# -- task endpoints --
def list_tasks():
    # GET /tasks
    # 用法：列出所有任务（包括文件导入/导出任务）
    r = requests.get(f"{BASE_URL}/tasks")
    print(r.status_code, json.dumps(r.json(), indent=2))


def import_file():
    # POST /tasks (multipart/form-data)
    # 用法：上传文件触发文件导入任务，type 参数指定任务类型（如 "IMPORT"）
    path = input("Local file path to import: ")
    if not os.path.exists(path):
        print("File not found")
        return
    with open(path, 'rb') as f:
        # 使用 secure 的文件名封装上传的文件
        files = {'file': (os.path.basename(path), f)}
        data = {'type': 'IMPORT'}
        r = requests.post(f"{BASE_URL}/tasks", files=files, data=data)
    print(r.status_code, json.dumps(r.json(), indent=2))

def get_task():
    # GET /tasks/{task_id}
    # 用法：获取指定任务的状态及详情
    tid = input("Task ID: ")
    r = requests.get(f"{BASE_URL}/tasks/{tid}")
    print(r.status_code, r.text)



def delete_task():
    # DELETE /tasks/{task_id}
    # 用法：删除指定任务
    tid = input("Task ID to delete: ")
    r = requests.delete(f"{BASE_URL}/tasks/{tid}")
    print(r.status_code)

def download_task():
    # GET /tasks/{task_id}/download
    # 用法：下载指定任务处理完成后的结果文件
    tid = input("Task ID for download: ")
    r = requests.get(f"{BASE_URL}/tasks/{tid}/download")
    if r.status_code == 200:
        fname = input("Save as filename: ")
        with open(fname, 'wb') as f:
            f.write(r.content)
        print(f"Saved to {fname}")
    else:
        print(r.status_code, r.text)

# -- stats_logs endpoints --
def list_stats():
    # GET /stats_logs
    # 用法：列出所有统计日志
    r = requests.get(f"{BASE_URL}/stats_logs")
    print(r.status_code, json.dumps(r.json(), indent=2))

def create_stats():
    # POST /stats_logs
    # 用法：创建一条新的统计日志
    r = requests.post(f"{BASE_URL}/stats_logs", json=DEFAULT_STATS)
    print(r.status_code, json.dumps(r.json(), indent=2))

def get_stats():
    # GET /stats_logs/{log_id}
    # 用法：获取指定统计日志详情
    lid = input("StatsLog ID: ")
    r = requests.get(f"{BASE_URL}/stats_logs/{lid}")
    print(r.status_code, r.text)

def update_stats():
    # PUT /stats_logs/{log_id}
    # 用法：更新指定统计日志数据
    lid = input("StatsLog ID: ")
    payload = json.loads(input(f"JSON payload (default={DEFAULT_STATS}): ") or json.dumps(DEFAULT_STATS))
    r = requests.put(f"{BASE_URL}/stats_logs/{lid}", json=payload)
    print(r.status_code, r.text)

def delete_stats():
    # DELETE /stats_logs/{log_id}
    # 用法：删除指定统计日志
    lid = input("StatsLog ID: ")
    r = requests.delete(f"{BASE_URL}/stats_logs/{lid}")
    print(r.status_code)

# -- CLI menu --
def main():
    menu = {
        '1': ("List offers", list_offers),
        '2': ("Create offer", create_offer),
        '3': ("Get offer", get_offer),
        '4': ("Update offer", update_offer),
        '5': ("Delete offer", delete_offer),
        '6': ("List tasks", list_tasks),
        '7': ("Import file task", import_file),
        '8': ("Get task", get_task),
        '9': ("Download task result", download_task),
        '10':("List stats_logs", list_stats),
        '11':("Create stats_log", create_stats),
        '12':("Get stats_log", get_stats),
        '13':("Update stats_log", update_stats),
        '14':("Delete stats_log", delete_stats),
        '15':("Search offers", search_offers),  # 新增：搜索招聘信息功能
        'q':("Quit", None)
    }
    while True:
        print("\n--- API Usage Menu ---")
        for k, (desc, _) in menu.items():
            print(f"{k}. {desc}")
        choice = input("Select option: ").strip()
        if choice == 'q':
            break
        action = menu.get(choice)
        if action:
            action[1]()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
