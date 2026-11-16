"""
Màn 1: Trang chủ & Giới thiệu tổng quan về Finite Automata (FA) trong thực tiễn.
"""

import tkinter as tk
from tkinter import ttk


class HomeScreen(ttk.Frame):
    """Màn 1: Home - Giới thiệu tổng quan và điều hướng đến 4 ứng dụng."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Canvas có scrollbar cho trường hợp màn hình nhỏ
        canvas = tk.Canvas(self, bg="#f8fafc", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def _on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_configure)
        canvas.configure(xscrollcommand=None, yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Container chính bên trong scrollable_frame
        main_box = tk.Frame(scrollable_frame, bg="#f8fafc", padx=30, pady=25)
        main_box.pack(fill="both", expand=True)

        # 1. Hero Banner
        banner = tk.Frame(main_box, bg="#1e293b", padx=25, pady=20)
        banner.pack(fill="x", pady=(0, 20))

        title_lbl = tk.Label(
            banner,
            text="HỆ THỐNG MÔ PHỎNG ỨNG DỤNG FINITE AUTOMATA TRONG THỰC TIỄN",
            font=("Segoe UI", 16, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
            anchor="w",
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            banner,
            text="Bài tập nhóm Môn Lý thuyết tính toán — Chủ đề 1: Mô hình hóa hệ thống thực tế bằng DFA, NFA & Moore Machine",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#1e293b",
            anchor="w",
        )
        subtitle_lbl.pack(anchor="w", pady=(5, 10))

        info_bar = tk.Frame(banner, bg="#334155", padx=12, pady=6)
        info_bar.pack(anchor="w")
        tk.Label(
            info_bar,
            text="Sinh viên thực hiện: Trần Quang Minh (B2304069) & Hân  |  Python 3 & Tkinter GUI Engine",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#334155",
        ).pack(side="left")

        # 2. Card Lý thuyết tổng quan về FA
        theory_card = tk.LabelFrame(
            main_box,
            text="  1. TỔNG QUAN LÝ THUYẾT VỀ MÁY TRẠNG THÁI HỮU HẠN (FINITE AUTOMATA)  ",
            font=("Segoe UI", 11, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=20,
            pady=15,
            relief="solid",
            bd=1,
        )
        theory_card.pack(fill="x", pady=(0, 20))

        intro_text = (
            "Finite Automaton (FA) là mô hình toán học trừu tượng đại diện cho một hệ thống với số lượng trạng thái hữu hạn.\n"
            "Tại mỗi thời điểm, hệ thống chỉ ở một trạng thái duy nhất (hoặc tập hợp các trạng thái đối với NFA).\n"
            "Khi nhận được một tín hiệu đầu vào (input symbol), hệ thống chuyển sang trạng thái tiếp theo thông qua hàm chuyển δ."
        )
        tk.Label(
            theory_card,
            text=intro_text,
            font=("Segoe UI", 10),
            fg="#334155",
            bg="#ffffff",
            justify="left",
            anchor="w",
        ).pack(anchor="w", pady=(0, 10))

        # Khung so sánh 3 loại máy
        types_frame = tk.Frame(theory_card, bg="#ffffff")
        types_frame.pack(fill="x", pady=5)

        fa_types = [
            ("DFA (Deterministic FA)", "M = (Q, Σ, δ, q0, F)\nMỗi (trạng thái, ký tự) xác định duy nhất 1 trạng thái tiếp theo.\nỨng dụng: Điều khiển đèn giao thông, máy bán hàng.", "#e0f2fe", "#0284c7"),
            ("Moore Machine (FA có Output)", "M = (Q, Σ, Δ, δ, λ, q0)\nĐầu ra λ chỉ phụ thuộc vào trạng thái hiện tại λ: Q → Δ.\nỨng dụng: Giao thức ATM, hiển thị màn hình LCD vi xử lý.", "#fef3c7", "#d97706"),
            ("NFA & Subset Construction", "M = (Q, Σ, δ, q0, F)\nMỗi (trạng thái, ký tự) có thể dẫn tới nhiều trạng thái.\nĐược chuyển sang DFA tương đương bằng thuật toán tập con.", "#dcfce7", "#16a34a"),
        ]

        for i, (head, desc, bg_c, border_c) in enumerate(fa_types):
            c_box = tk.Frame(types_frame, bg=bg_c, highlightbackground=border_c, highlightthickness=1, padx=12, pady=10)
            c_box.pack(side="left", fill="both", expand=True, padx=5 if i != 0 else (0, 5))
            tk.Label(c_box, text=head, font=("Segoe UI", 10, "bold"), fg=border_c, bg=bg_c).pack(anchor="w")
            tk.Label(c_box, text=desc, font=("Segoe UI", 9), fg="#1e293b", bg=bg_c, justify="left").pack(anchor="w", pady=(4, 0))

        # 3. 4 Ứng dụng thực tế (Grid 2x2)
        apps_frame = tk.LabelFrame(
            main_box,
            text="  2. CÁC ỨNG DỤNG THỰC TIỄN & 8 MÀN HÌNH MINH HỌA  ",
            font=("Segoe UI", 11, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=20,
            pady=15,
            relief="solid",
            bd=1,
        )
        apps_frame.pack(fill="both", expand=True)

        apps_info = [
            {
                "title": "🚦 ỨNG DỤNG 1: ĐÈN GIAO THÔNG (TRAFFIC LIGHT)",
                "model": "DFA tuần tự 4 pha (Bắc-Nam & Đông-Tây) + Chế độ khẩn cấp",
                "screens": "• Màn 2: Mô phỏng đồ họa ngã tư & Canvas sơ đồ chuyển trạng thái DFA\n• Màn 3: Bảng chuyển trạng thái chi tiết, Step mode & Log sự kiện",
                "target_screen_1": 1,  # Index 1 = Màn 2
                "target_screen_2": 2,  # Index 2 = Màn 3
                "btn_label_1": "Mở Màn 2: Mô phỏng",
                "btn_label_2": "Mở Màn 3: Bảng Log",
                "color": "#eff6ff",
                "border": "#3b82f6",
            },
            {
                "title": "💳 ỨNG DỤNG 2: MÁY ATM (AUTOMATED TELLER MACHINE)",
                "model": "Moore Machine với hàm xuất Output theo trạng thái",
                "screens": "• Màn 4: Giả lập màn hình ATM, bàn phím PIN pad, khe cắm thẻ & nhả tiền\n• Màn 5: Sơ đồ Moore Machine & Bộ 4 Test Cases tự động (Khóa thẻ sai PIN 3 lần)",
                "target_screen_1": 3,  # Index 3 = Màn 4
                "target_screen_2": 4,  # Index 4 = Màn 5
                "btn_label_1": "Mở Màn 4: Giả lập ATM",
                "btn_label_2": "Mở Màn 5: Test Cases",
                "color": "#f0fdf4",
                "border": "#22c55e",
            },
            {
                "title": "🥤 ỨNG DỤNG 3: MÁY BÁN HÀNG TỰ ĐỘNG (VENDING MACHINE)",
                "model": "DFA quản lý số dư tích lũy, xuất hàng và thuật toán trả tiền thừa",
                "screens": "• Màn 6: Tủ bán nước tương tác (Aquafina, Coca, Red Bull, Highlands)\n• Nạp tiền mệnh giá 5k, 10k, 20k, khay nhận hàng và bảng theo dõi trạng thái DFA",
                "target_screen_1": 5,  # Index 5 = Màn 6
                "target_screen_2": None,
                "btn_label_1": "Mở Màn 6: Máy bán hàng",
                "btn_label_2": None,
                "color": "#fffbeb",
                "border": "#f59e0b",
            },
            {
                "title": "🔍 ỨNG DỤNG 4: TÌM KIẾM CHUỖI & NFA -> DFA CONVERSION",
                "model": "NFA Pattern Matching & Thuật toán Subset Construction",
                "screens": "• Màn 7: NFA tìm kiếm chuỗi mẫu trong văn bản, highlight kết quả theo bước\n• Màn 8: Trực quan hóa thuật toán chuyển NFA sang DFA (bảng tập hợp trạng thái)",
                "target_screen_1": 6,  # Index 6 = Màn 7
                "target_screen_2": 7,  # Index 7 = Màn 8
                "btn_label_1": "Mở Màn 7: Pattern Search",
                "btn_label_2": "Mở Màn 8: NFA -> DFA",
                "color": "#faf5ff",
                "border": "#a855f7",
            },
        ]

        grid_frame = tk.Frame(apps_frame, bg="#ffffff")
        grid_frame.pack(fill="both", expand=True)

        for idx, app in enumerate(apps_info):
            r = idx // 2
            c = idx % 2
            card = tk.Frame(
                grid_frame,
                bg=app["color"],
                highlightbackground=app["border"],
                highlightthickness=1,
                padx=15,
                pady=12,
            )
            card.grid(row=r, column=c, padx=8, pady=8, sticky="nsew")
            grid_frame.columnconfigure(c, weight=1)
            grid_frame.rowconfigure(r, weight=1)

            tk.Label(card, text=app["title"], font=("Segoe UI", 10, "bold"), fg="#0f172a", bg=app["color"]).pack(anchor="w")
            tk.Label(card, text=f"Mô hình: {app['model']}", font=("Segoe UI", 9, "italic"), fg="#475569", bg=app["color"]).pack(anchor="w", pady=(2, 6))
            tk.Label(card, text=app["screens"], font=("Segoe UI", 9), fg="#1e293b", bg=app["color"], justify="left").pack(anchor="w", pady=(0, 10))

            btn_box = tk.Frame(card, bg=app["color"])
            btn_box.pack(fill="x", side="bottom")

            btn1 = tk.Button(
                btn_box,
                text=app["btn_label_1"],
                font=("Segoe UI", 9, "bold"),
                bg=app["border"],
                fg="#ffffff",
                relief="flat",
                cursor="hand2",
                padx=8,
                pady=4,
                command=lambda s=app["target_screen_1"]: self.controller.show_screen(s),
            )
            btn1.pack(side="left", padx=(0, 6))

            if app["btn_label_2"] and app["target_screen_2"] is not None:
                btn2 = tk.Button(
                    btn_box,
                    text=app["btn_label_2"],
                    font=("Segoe UI", 9),
                    bg="#ffffff",
                    fg="#0f172a",
                    highlightbackground=app["border"],
                    highlightthickness=1,
                    relief="flat",
                    cursor="hand2",
                    padx=8,
                    pady=4,
                    command=lambda s=app["target_screen_2"]: self.controller.show_screen(s),
                )
                btn2.pack(side="left")
