import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QScrollArea, QFrame, QSplitter
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from data.project_info import PROJECT_NAME, PROJECT_SLOGAN, REPOSITORY_STATUS
from data.members import MEMBERS
from data.features import FEATURES
from data.progress import ISSUES, PULL_REQUESTS
from data.changelog import CHANGELOG


class ProjectBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("班级项目协作看板")
        self.setMinimumSize(1000, 680)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)
        root_layout.setContentsMargins(16, 16, 16, 16)
        root_layout.setSpacing(12)

        # ── 顶部：项目名称 & 口号 ──────────────────────────────────────
        header = QFrame()
        header.setStyleSheet("background:#2c3e50; border-radius:8px;")
        h_layout = QVBoxLayout(header)
        h_layout.setContentsMargins(20, 16, 20, 16)

        title_lbl = QLabel(PROJECT_NAME)
        title_lbl.setFont(QFont("Microsoft YaHei", 20, QFont.Bold))
        title_lbl.setStyleSheet("color:#ecf0f1;")
        title_lbl.setAlignment(Qt.AlignCenter)

        slogan_lbl = QLabel(PROJECT_SLOGAN)
        slogan_lbl.setFont(QFont("Microsoft YaHei", 11))
        slogan_lbl.setStyleSheet("color:#bdc3c7;")
        slogan_lbl.setAlignment(Qt.AlignCenter)
        slogan_lbl.setWordWrap(True)

        status_lbl = QLabel(f"状态：{REPOSITORY_STATUS}")
        status_lbl.setFont(QFont("Microsoft YaHei", 10))
        status_lbl.setStyleSheet("color:#27ae60;")
        status_lbl.setAlignment(Qt.AlignCenter)

        h_layout.addWidget(title_lbl)
        h_layout.addWidget(slogan_lbl)
        h_layout.addWidget(status_lbl)
        root_layout.addWidget(header)

        # ── 主体三栏 ──────────────────────────────────────────────────
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        # 左栏：成员卡片
        splitter.addWidget(self._make_members_panel())
        # 中栏：功能清单
        splitter.addWidget(self._make_features_panel())
        # 右栏：Issue / PR 进度
        splitter.addWidget(self._make_progress_panel())

        splitter.setSizes([300, 300, 300])
        root_layout.addWidget(splitter, stretch=1)

        # ── 底部：版本日志 ─────────────────────────────────────────────
        root_layout.addWidget(self._make_changelog_panel())

    # ── 面板构建方法 ──────────────────────────────────────────────────

    def _section_frame(self, title: str, bg: str = "#ecf0f1") -> tuple:
        frame = QFrame()
        frame.setStyleSheet(f"background:{bg}; border-radius:8px;")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        lbl = QLabel(title)
        lbl.setFont(QFont("Microsoft YaHei", 12, QFont.Bold))
        lbl.setStyleSheet("color:#2c3e50;")
        layout.addWidget(lbl)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color:#bdc3c7;")
        layout.addWidget(sep)

        return frame, layout

    def _make_members_panel(self):
        frame, layout = self._section_frame("👥 小组成员", "#fdfefe")
        for m in MEMBERS:
            card = QFrame()
            card.setStyleSheet(
                "background:#d6eaf8; border-radius:6px; padding:4px;"
            )
            cl = QVBoxLayout(card)
            cl.setContentsMargins(8, 6, 8, 6)
            cl.setSpacing(2)

            name_lbl = QLabel(f"{m.get('role', '')}  {m.get('name', '')}")
            name_lbl.setFont(QFont("Microsoft YaHei", 10, QFont.Bold))
            name_lbl.setStyleSheet("color:#1a5276;")

            task_lbl = QLabel(m.get("task", ""))
            task_lbl.setFont(QFont("Microsoft YaHei", 9))
            task_lbl.setStyleSheet("color:#2e4057;")
            task_lbl.setWordWrap(True)

            cl.addWidget(name_lbl)
            cl.addWidget(task_lbl)
            layout.addWidget(card)

        layout.addStretch()
        return self._wrap_scroll(frame)

    def _make_features_panel(self):
        frame, layout = self._section_frame("✅ 项目功能清单", "#fdfefe")
        for i, feat in enumerate(FEATURES, 1):
            lbl = QLabel(f"{i}. {feat}")
            lbl.setFont(QFont("Microsoft YaHei", 10))
            lbl.setStyleSheet(
                "background:#d5f5e3; border-radius:4px; padding:6px;"
                "color:#1e8449;"
            )
            lbl.setWordWrap(True)
            layout.addWidget(lbl)
        layout.addStretch()
        return self._wrap_scroll(frame)

    def _make_progress_panel(self):
        frame, layout = self._section_frame("📋 Issue / PR 进度", "#fdfefe")

        layout.addWidget(QLabel("── Issues ──"))
        for iss in ISSUES:
            lbl = QLabel(
                f"#{iss.get('id')}  {iss.get('title', '')}  [{iss.get('status', '')}]"
            )
            lbl.setFont(QFont("Microsoft YaHei", 9))
            lbl.setStyleSheet(
                "background:#fdebd0; border-radius:4px; padding:5px; color:#784212;"
            )
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

        layout.addWidget(QLabel("── Pull Requests ──"))
        for pr in PULL_REQUESTS:
            lbl = QLabel(
                f"PR#{pr.get('id')}  {pr.get('title', '')}  [{pr.get('status', '')}]"
            )
            lbl.setFont(QFont("Microsoft YaHei", 9))
            lbl.setStyleSheet(
                "background:#e8daef; border-radius:4px; padding:5px; color:#4a235a;"
            )
            lbl.setWordWrap(True)
            layout.addWidget(lbl)

        layout.addStretch()
        return self._wrap_scroll(frame)

    def _make_changelog_panel(self):
        frame, layout = self._section_frame("📝 版本日志", "#fdfefe")
        layout.parent().setMaximumHeight(160)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QWidget()
        il = QVBoxLayout(inner)
        il.setSpacing(4)
        for entry in CHANGELOG:
            lbl = QLabel(f"[{entry.get('version', '')}] {entry.get('date', '')}  {entry.get('note', '')}")
            lbl.setFont(QFont("Microsoft YaHei", 9))
            lbl.setStyleSheet("color:#555;")
            il.addWidget(lbl)
        il.addStretch()
        scroll.setWidget(inner)
        layout.addWidget(scroll)
        return frame

    @staticmethod
    def _wrap_scroll(widget: QWidget) -> QScrollArea:
        sa = QScrollArea()
        sa.setWidgetResizable(True)
        sa.setWidget(widget)
        return sa


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = ProjectBoard()
    win.show()
    sys.exit(app.exec())
