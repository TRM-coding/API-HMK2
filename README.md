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
