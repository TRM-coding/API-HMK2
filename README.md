# API HMK2

## 系统架构
- Flask RESTful 服务  
- Celery 异步任务（Broker: Redis）  
- MySQL（开发/生产）做为数据库  
- 文件存储：`uploads/`（输入）和 `results/`（输出）

## 目录与文件说明
- `run.py`：启动 Flask 应用的入口  
- `celery_worker.py`：启动 Celery worker 的脚本  
- `requirements.txt`：项目依赖  
- `.env`：环境变量配置  
- `app/`：核心模块  
  - `config.py`：配置项（数据库、Celery、文件路径）  
  - `extensions.py`：初始化扩展（SQLAlchemy、Migrate、Celery）  
  - `models.py`：ORM 模型（Offer、ImportExportTask、StatsLog）  
  - `utils.py`：工具函数（`to_dict`）  
  - `tasks.py`：Celery 异步任务逻辑（文件导入/导出处理）  
  - `routes/`：Blueprint 路由  
    - `offers.py`：Offer CRUD  
    - `tasks.py`：导入/导出任务 API（上传、状态查询、下载）  
    - `stats_logs.py`：统计日志 CRUD  
- `tests/`：pytest 测试用例

## 项目文件结构
- **run.py**：启动 Flask 应用的入口文件。
- **celery_worker.py**：启动 Celery worker，处理异步任务。
- **app/config.py**：配置项设置，包括数据库、Celery、文件路径等。
- **app/extensions.py**：初始化并管理扩展（如 SQLAlchemy、Migrate、Celery）。
- **app/models.py**：ORM 模型定义，包含 Offer、ImportExportTask、StatsLog。
- **app/tasks.py**：实现 Celery 异步任务的逻辑（文件导入/导出及数据处理）。
- **app/routes/**：
  - **offers.py**：提供 Offer 的增删改查接口及搜索、分页支持。
  - **tasks.py**：处理文件上传、任务状态获取和结果下载的 API。
  - **stats_logs.py**：对统计日志的增、查、改、删接口。
- **app/utils.py**：辅助工具函数，如模型转字典的 `to_dict` 函数。
- **tests/**：单元测试目录，使用 pytest 编写，对各模块接口进行测试。
- **tmp_uploads/** 和 **tmp_results/**：测试时使用的临时文件夹。
- **demo_runner.py**：交互式演示脚本，按照步骤展示 API 操作（Offer、任务、StatsLog 等）。
- **use_system.py**：命令行客户端，提供一个菜单，直接调用 API 接口进行各项操作。
- **.env**：环境变量配置文件。
- **requirements.txt**：项目依赖的列表。
- **start_all.sh**：一键启动脚本，用于同时启动 Redis、Celery worker 与 Flask 应用。

## 环境准备
1. 安装依赖  
   ```bash
   pip install -r requirements.txt
   ```  
2. 启动 Redis  
   ```bash
   redis-server
   ```  
3. 配置环境变量（可在 `.env` 中设置）  
   ```bash
   FLASK_ENV=development
   DATABASE_URL=你的数据库连接字符串
   CELERY_BROKER_URL=redis://localhost:6379/0
   ```

## 数据库迁移
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## 启动服务
1. 启动 Celery worker  
   ```bash
   celery -A celery_worker worker --loglevel=info
   ```  
2. 启动 Flask 应用  
   ```bash
   python run.py
   ```  

## 运行整个系统

你可以使用下面的脚本同时启动 Redis、Celery worker 和 Flask 应用：

```bash
#!/bin/bash
# filepath: /root/api_hmk2/start_all.sh
# 启动 Redis (确保 redis-server 在系统 PATH 中)
redis-server &
# 启动 Celery worker
celery -A celery_worker worker --loglevel=info &
# 启动 Flask 应用
python run.py
```

给脚本执行权限并运行：
```bash
chmod +x start_all.sh
./start_all.sh
```

## 使用说明
- POST `/tasks` (multipart/form-data) 上传文件开始异步处理  
- GET `/tasks/<task_id>` 查看任务状态  
- GET `/tasks/<task_id>/download` 成功后下载处理结果  
- 其它 CRUD 接口：  
  - `/offers`  
  - `/stats_logs`

## 运行测试
在项目根目录下执行：
```bash
pytest
```

## 单元测试
单元测试位于 `tests/` 目录下，涵盖以下方面：
- **Offer 接口**：测试 Offer 的创建、查询、更新、删除以及搜索和分页功能。
- **任务接口**：包括文件导入任务的上传、状态检查和结果下载。
- **StatsLog 接口**：测试统计日志的创建、查询、更新和删除操作。
运行测试命令：
```bash
pytest
```

## use_system.py 说明及使用方法
`use_system.py` 提供了一个基于命令行的菜单接口，可直接调用后端 API。主要功能包括：
- 查询、创建、更新、删除 Offer；
- 上传文件触发导入任务以及下载任务处理结果；
- 查询和管理统计日志（StatsLog）。
使用方法：
```bash
python use_system.py
```
根据提示输入相应参数和选项即可操作。

## demo_runner.py 介绍及使用方法
`demo_runner.py` 是一个交互式演示脚本，通过按步骤执行展示 API 的各项功能：
- 演示 Offer 的创建、更新、查询与删除；
- 演示文件导入任务的创建、任务状态查询及结果下载；
- 演示统计日志（StatsLog）的创建、更新、查询与删除；
- 展示搜索功能和 Redis 队列状态检查。
使用方法：
```bash
python demo_runner.py
```
根据屏幕提示逐步执行各操作。

## 安装和启动方法
1. **安装依赖**  
   安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. **配置环境变量**  
   修改或创建 `.env` 文件，设置如下环境变量：
   ```bash
   FLASK_ENV=development
   DATABASE_URL=你的数据库连接字符串
   CELERY_BROKER_URL=redis://localhost:6379/0
   API_BASE_URL=http://127.0.0.1:5000
   ```
3. **数据库迁移**  
   进行数据库初始化与迁移：
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
4. **启动服务**
   - 启动 Celery worker：
     ```bash
     celery -A celery_worker worker --loglevel=info
     ```
   - 启动 Flask 应用：
     ```bash
     python run.py
     ```
   或者直接使用一键启动脚本：
   ```bash
   chmod +x start_all.sh
   ./start_all.sh
   ```
5. **运行测试**  
   执行单元测试验证系统：
   ```bash
   pytest
   ```
