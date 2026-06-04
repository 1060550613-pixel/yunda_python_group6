# team_project_board

班级项目协作看板 —— GitHub 五人协作实践项目（第 14 周）

## 项目说明

本项目是 PySide6 桌面 GUI 应用，用于展示小组协作看板，包含：

- 项目名称、口号和仓库状态
- 5 人成员卡片
- 项目功能清单
- Issue / PR 进度追踪
- 版本日志

## 运行方式

```powershell
pip install -r requirements.txt
python main.py
```

## 目录结构

```
team_project_board/
├── main.py              # GUI 主程序
├── requirements.txt     # 依赖
├── README.md            # 说明文档
├── data/
│   ├── project_info.py  # 项目名称、口号、状态（组员A负责修改）
│   ├── members.py       # 成员列表（组员B负责修改）
│   ├── features.py      # 功能清单（组员C负责修改）
│   ├── progress.py      # Issue/PR进度（组员D负责修改）
│   └── changelog.py     # 版本日志（组员D负责修改）
└── ui/                  # 界面资源（预留）
```

## 分工说明

| 角色 | 任务 | 文件 |
|------|------|------|
| 组长 | 建仓库、建Issue、审核PR、合并代码 | README.md |
| 组员A | 更新项目名称、口号、仓库状态 | data/project_info.py |
| 组员B | 补全5人成员卡片 | data/members.py |
| 组员C | 补充项目功能清单 | data/features.py |
| 组员D | 补充Issue/PR进度和版本日志 | data/progress.py, data/changelog.py |
