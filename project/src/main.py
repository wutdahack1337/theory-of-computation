"""
Main Application - Điểm khởi động ứng dụng Tkinter cho Đồ án Lý thuyết tính toán.
Chủ đề 1: Ứng dụng Finite Automata trong thực tiễn.
Nhóm sinh viên thực hiện: Trần Quang Minh (B2304069) & Hân.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk

# Đảm bảo đường dẫn import luôn chính xác dù chạy từ thư mục gốc hay thư mục project
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from screens.home import HomeScreen
from screens.traffic_screen import TrafficSimScreen, TrafficLogScreen
from screens.atm_screen import ATMSimScreen, ATMGraphScreen
from screens.vending_screen import VendingScreen
from screens.pattern_screen import PatternSearchScreen, NfaToDfaScreen


class MainApp(tk.Tk):
    """Cửa sổ chính điều hướng toàn bộ 8 màn hình của ứng dụng."""

    def __init__(self):
        super().__init__()

        self.title("Ứng dụng Finite Automata trong thực tiễn — Minh & Hân")
        self.geometry("1180x740")
        self.minsize(980, 640)

        # Cấu hình icon / màu sắc nền chính
        self.configure(bg="#f8fafc")

        self.screens = []
        self.nav_buttons = []
        self.current_screen_index = 0

        self._init_layout()
        self._init_screens()
        self.show_screen(0)  # Mặc định mở Màn 1 (Home)

    def _init_layout(self):
        # 1. Thanh Sidebar điều hướng bên trái
        self.sidebar = tk.Frame(self, bg="#0f172a", width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Header Sidebar
        brand_box = tk.Frame(self.sidebar, bg="#0f172a", padx=16, pady=18)
        brand_box.pack(fill="x")

        tk.Label(
            brand_box,
            text="⚡ FA SIMULATOR",
            font=("Segoe UI", 13, "bold"),
            fg="#38bdf8",
            bg="#0f172a",
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            brand_box,
            text="Lý thuyết tính toán • Đề tài 1",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f172a",
            anchor="w",
        ).pack(fill="x", pady=(2, 0))

        # Đường phân cách
        sep = tk.Frame(self.sidebar, bg="#334155", height=1)
        sep.pack(fill="x", padx=12, pady=(0, 10))

        # Danh sách các nút chuyển màn hình
        self.menu_frame = tk.Frame(self.sidebar, bg="#0f172a")
        self.menu_frame.pack(fill="both", expand=True)

        menu_items = [
            ("🏠 Màn 1: Trang chủ & Lý thuyết", "Minh"),
            ("🚦 Màn 2: Đèn giao thông (Mô phỏng)", "Hân"),
            ("📋 Màn 3: Đèn giao thông (Bảng Log)", "Hân"),
            ("💳 Màn 4: Máy ATM (Giả lập GD)", "Minh"),
            ("🔐 Màn 5: Máy ATM (Moore Machine)", "Minh"),
            ("🥤 Màn 6: Máy bán hàng tự động", "Hân"),
            ("🔍 Màn 7: Pattern Search (NFA)", "Minh"),
            ("🔄 Màn 8: NFA → DFA (Subset Const.)", "Minh"),
        ]

        for idx, (label, author) in enumerate(menu_items):
            btn_frame = tk.Frame(self.menu_frame, bg="#0f172a")
            btn_frame.pack(fill="x", pady=2, padx=8)

            btn = tk.Button(
                btn_frame,
                text=label,
                font=("Segoe UI", 9),
                fg="#cbd5e1",
                bg="#0f172a",
                activebackground="#1e293b",
                activeforeground="#38bdf8",
                relief="flat",
                anchor="w",
                padx=10,
                pady=7,
                cursor="hand2",
                command=lambda i=idx: self.show_screen(i),
            )
            btn.pack(side="left", fill="x", expand=True)

            # Badge tác giả (Minh / Hân)
            badge_color = "#0284c7" if author == "Minh" else "#d97706"
            badge = tk.Label(
                btn_frame,
                text=author,
                font=("Segoe UI", 7, "bold"),
                fg="#ffffff",
                bg=badge_color,
                padx=5,
                pady=1,
            )
            badge.pack(side="right", padx=(0, 6))

            self.nav_buttons.append((btn, btn_frame))

        # Footer Sidebar
        footer_box = tk.Frame(self.sidebar, bg="#1e293b", padx=14, pady=12)
        footer_box.pack(fill="x", side="bottom")

        tk.Label(
            footer_box,
            text="Nhóm: Minh (B2304069) & Hân",
            font=("Segoe UI", 8, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
            anchor="w",
        ).pack(fill="x")
        tk.Label(
            footer_box,
            text="Học kỳ 1 • 2026-2027",
            font=("Segoe UI", 7),
            fg="#94a3b8",
            bg="#1e293b",
            anchor="w",
        ).pack(fill="x")

        # 2. Khung chứa nội dung chính các màn hình bên phải
        self.content_container = tk.Frame(self, bg="#f8fafc")
        self.content_container.pack(side="right", fill="both", expand=True)

    def _init_screens(self):
        """Khởi tạo tất cả 8 màn hình trong container."""
        # Màn 1: Home (Minh)
        s1 = HomeScreen(self.content_container, self)
        # Màn 2: Traffic Light Sim (Hân)
        s2 = TrafficSimScreen(self.content_container, self)
        # Màn 3: Traffic Light Log (Hân)
        s3 = TrafficLogScreen(self.content_container, self, shared_tl=s2.tl)
        # Màn 4: ATM Sim (Minh)
        s4 = ATMSimScreen(self.content_container, self)
        # Màn 5: ATM Graph & Tests (Minh)
        s5 = ATMGraphScreen(self.content_container, self, shared_atm=s4.atm)
        # Màn 6: Vending Machine (Hân)
        s6 = VendingScreen(self.content_container, self)
        # Màn 7: Pattern Search (Minh)
        s7 = PatternSearchScreen(self.content_container, self)
        # Màn 8: NFA -> DFA (Minh)
        s8 = NfaToDfaScreen(self.content_container, self)

        self.screens = [s1, s2, s3, s4, s5, s6, s7, s8]

    def show_screen(self, screen_index: int):
        """Chuyển đổi hiển thị màn hình theo chỉ mục (0 -> 7)."""
        if 0 <= screen_index < len(self.screens):
            # Ẩn tất cả màn hình
            for s in self.screens:
                s.pack_forget()

            # Hiển thị màn hình được chọn
            self.screens[screen_index].pack(fill="both", expand=True)
            self.current_screen_index = screen_index

            # Cập nhật style nút điều hướng active trên sidebar
            for idx, (btn, btn_frame) in enumerate(self.nav_buttons):
                if idx == screen_index:
                    btn.config(bg="#1e293b", fg="#38bdf8", font=("Segoe UI", 9, "bold"))
                    btn_frame.config(bg="#1e293b")
                else:
                    btn.config(bg="#0f172a", fg="#cbd5e1", font=("Segoe UI", 9))
                    btn_frame.config(bg="#0f172a")


def main():
    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    main()
