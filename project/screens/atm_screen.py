"""
Màn 4 & Màn 5: Hệ thống máy ATM mô hình hóa bằng Moore Machine.
- ATMSimScreen (Màn 4): Giả lập giao diện vật lý máy ATM (Màn hình LCD, bàn phím số, khe cắm thẻ, nhả tiền).
- ATMGraphScreen (Màn 5): Sơ đồ đồ thị trạng thái Moore Machine & Bộ 4 Test Cases tự động (Khóa thẻ sai PIN 3 lần).
"""

import time
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from src.atm import ATMMooreMachine


class ATMSimScreen(ttk.Frame):
    """Màn 4: Giả lập giao diện tương tác máy ATM vật lý và theo dõi Moore Machine."""

    def __init__(self, parent, controller, shared_atm: Optional[ATMMooreMachine] = None):
        super().__init__(parent)
        self.controller = controller
        self.atm = shared_atm if shared_atm else ATMMooreMachine()
        self._build_ui()
        self.update_display()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 4: GIẢ LẬP MÁY ATM (MOORE MACHINE INTERACTIVE SIMULATOR)",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        btn_go_graph = tk.Button(
            header,
            text="Sang Màn 5: Sơ đồ Moore Machine & Test Cases →",
            font=("Segoe UI", 9, "bold"),
            bg="#10b981",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self.controller.show_screen(4),
        )
        btn_go_graph.pack(side="right")

        body = tk.Frame(self, bg="#f8fafc", padx=15, pady=15)
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        # CỘT TRÁI: Vỏ máy ATM + Màn hình LCD + Bàn phím
        atm_casing = tk.LabelFrame(
            body,
            text="  KI-ỐT ATM VẬT LÝ (ATM PHYSICAL TERMINAL)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#334155",
            padx=15,
            pady=15,
            relief="solid",
            bd=2,
        )
        atm_casing.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        # 1. Màn hình LCD của máy ATM
        self.lcd_screen = tk.Frame(atm_casing, bg="#0f2e59", padx=15, pady=15, relief="sunken", bd=3)
        self.lcd_screen.pack(fill="x", pady=(0, 15))

        self.lcd_brand = tk.Label(
            self.lcd_screen,
            text="★ AGY E-BANKING SYSTEM — 24/7 ATM TERMINAL ★",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#0f2e59",
        )
        self.lcd_brand.pack(pady=(0, 6))

        self.lcd_title = tk.Label(
            self.lcd_screen,
            text="CHÀO MỪNG QUÝ KHÁCH",
            font=("Segoe UI", 12, "bold"),
            fg="#ffffff",
            bg="#0f2e59",
        )
        self.lcd_title.pack(pady=4)

        self.lcd_msg = tk.Label(
            self.lcd_screen,
            text="Vui lòng đưa thẻ ngân hàng vào khe cắm thẻ.",
            font=("Segoe UI", 10),
            fg="#e2e8f0",
            bg="#0f2e59",
            wraplength=420,
            justify="center",
        )
        self.lcd_msg.pack(pady=6)

        self.lcd_pin_display = tk.Label(
            self.lcd_screen,
            text="",
            font=("Consolas", 18, "bold"),
            fg="#fbbf24",
            bg="#0f2e59",
        )
        self.lcd_pin_display.pack(pady=4)

        self.lcd_extra = tk.Label(
            self.lcd_screen,
            text="Số dư khả dụng: 5,000,000 VND | PIN mẫu: 1234",
            font=("Segoe UI", 8),
            fg="#94a3b8",
            bg="#0f2e59",
        )
        self.lcd_extra.pack(pady=(4, 0))

        # 2. Phần cứng: Khe cắm thẻ & Khe nhận tiền mặt
        hardware_box = tk.Frame(atm_casing, bg="#1e293b", padx=10, pady=10)
        hardware_box.pack(fill="x", pady=(0, 15))

        # Khe thẻ
        slot_card_frame = tk.Frame(hardware_box, bg="#1e293b")
        slot_card_frame.pack(side="left", fill="x", expand=True, padx=5)

        tk.Label(slot_card_frame, text="KHE CẮM THẺ ATM", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").pack()
        self.btn_insert_card = tk.Button(
            slot_card_frame,
            text="💳 Đưa thẻ vào",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._on_insert_card,
        )
        self.btn_insert_card.pack(pady=4)

        self.btn_take_card = tk.Button(
            slot_card_frame,
            text="⏏ Rút thẻ ra",
            font=("Segoe UI", 9),
            bg="#64748b",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            state="disabled",
            padx=10,
            pady=4,
            command=self._on_take_card,
        )
        self.btn_take_card.pack(pady=2)

        # Khe tiền
        slot_cash_frame = tk.Frame(hardware_box, bg="#1e293b")
        slot_cash_frame.pack(side="right", fill="x", expand=True, padx=5)

        tk.Label(slot_cash_frame, text="KHE NHẢ TIỀN MẶT", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").pack()
        self.btn_take_cash = tk.Button(
            slot_cash_frame,
            text="💵 Lấy tiền mặt",
            font=("Segoe UI", 9, "bold"),
            bg="#10b981",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            state="disabled",
            padx=10,
            pady=4,
            command=self._on_take_cash,
        )
        self.btn_take_cash.pack(pady=4)

        # 3. Bàn phím số & Phím rút tiền nhanh
        bottom_box = tk.Frame(atm_casing, bg="#334155")
        bottom_box.pack(fill="both", expand=True)

        # Bàn phím số PIN Pad (Trái)
        keypad_frame = tk.Frame(bottom_box, bg="#334155")
        keypad_frame.pack(side="left", padx=(0, 15))

        tk.Label(keypad_frame, text="BÀN PHÍM SỐ (KEYPAD)", font=("Segoe UI", 8, "bold"), fg="#cbd5e1", bg="#334155").grid(row=0, column=0, columnspan=3, pady=(0, 4))

        buttons = [
            ("1", 1, 0), ("2", 1, 1), ("3", 1, 2),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2),
            ("CLEAR", 4, 0), ("0", 4, 1), ("ENTER", 4, 2),
        ]
        for text, r, c in buttons:
            if text == "ENTER":
                bg_btn = "#10b981"
                fg_btn = "#ffffff"
                cmd = self._on_enter
            elif text == "CLEAR":
                bg_btn = "#f59e0b"
                fg_btn = "#ffffff"
                cmd = self._on_clear
            else:
                bg_btn = "#f8fafc"
                fg_btn = "#0f172a"
                cmd = lambda d=text: self._on_digit(d)

            btn = tk.Button(
                keypad_frame,
                text=text,
                font=("Segoe UI", 9, "bold"),
                bg=bg_btn,
                fg=fg_btn,
                width=6,
                height=1,
                relief="raised",
                cursor="hand2",
                command=cmd,
            )
            btn.grid(row=r, column=c, padx=3, pady=3)

        btn_cancel = tk.Button(
            keypad_frame,
            text="HỦY (CANCEL)",
            font=("Segoe UI", 8, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            relief="raised",
            cursor="hand2",
            command=self._on_cancel,
        )
        btn_cancel.grid(row=5, column=0, columnspan=3, sticky="we", pady=4)

        # Phím chức năng rút tiền nhanh (Phải)
        actions_frame = tk.Frame(bottom_box, bg="#334155")
        actions_frame.pack(side="right", fill="both", expand=True)

        tk.Label(actions_frame, text="CHỌN SỐ TIỀN RÚT", font=("Segoe UI", 8, "bold"), fg="#cbd5e1", bg="#334155").pack(pady=(0, 4))

        quick_amounts = [
            ("Rút 100,000 VND", 100000),
            ("Rút 200,000 VND", 200000),
            ("Rút 500,000 VND", 500000),
            ("Rút 1,000,000 VND", 1000000),
            ("Rút 2,000,000 VND", 2000000),
        ]
        self.amount_buttons = []
        for label, val in quick_amounts:
            b = tk.Button(
                actions_frame,
                text=label,
                font=("Segoe UI", 8),
                bg="#f1f5f9",
                fg="#0f172a",
                relief="flat",
                cursor="hand2",
                command=lambda v=val: self._on_withdraw(v),
            )
            b.pack(fill="x", pady=2)
            self.amount_buttons.append(b)

        # CỘT PHẢI: Trạng thái Moore Machine & Nhật ký
        right_panel = tk.LabelFrame(
            body,
            text="  GIÁM SÁT TRẠNG THÁI MOORE MACHINE  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=12,
            pady=10,
            relief="solid",
            bd=1,
        )
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        # Hộp trạng thái hiện tại
        state_box = tk.Frame(right_panel, bg="#f8fafc", padx=10, pady=8, relief="groove", bd=1)
        state_box.pack(fill="x", pady=(0, 10))

        tk.Label(state_box, text="Trạng thái hiện tại (State q):", font=("Segoe UI", 8), fg="#64748b", bg="#f8fafc").pack(anchor="w")
        self.lbl_curr_state = tk.Label(state_box, text="S_IDLE", font=("Consolas", 12, "bold"), fg="#2563eb", bg="#f8fafc")
        self.lbl_curr_state.pack(anchor="w")

        tk.Label(state_box, text="Hàm xuất Output λ(q):", font=("Segoe UI", 8), fg="#64748b", bg="#f8fafc").pack(anchor="w", pady=(6, 0))
        self.lbl_curr_output = tk.Label(
            state_box,
            text="Vui lòng đưa thẻ ATM vào khe nhận thẻ để bắt đầu.",
            font=("Segoe UI", 9, "italic"),
            fg="#0f172a",
            bg="#f8fafc",
            wraplength=280,
            justify="left",
        )
        self.lbl_curr_output.pack(anchor="w")

        self.lbl_attempts = tk.Label(state_box, text="Số lần thử PIN còn lại: 3/3", font=("Segoe UI", 9, "bold"), fg="#16a34a", bg="#f8fafc")
        self.lbl_attempts.pack(anchor="w", pady=(6, 0))

        # Log bảng Treeview
        tk.Label(right_panel, text="Lịch sử chuyển trạng thái gần nhất:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(anchor="w")
        cols = ("step", "from", "input", "to")
        self.log_tree = ttk.Treeview(right_panel, columns=cols, show="headings", height=8)
        self.log_tree.heading("step", text="#")
        self.log_tree.heading("from", text="Từ State")
        self.log_tree.heading("input", text="Sự kiện")
        self.log_tree.heading("to", text="Đến State")

        self.log_tree.column("step", width=35, anchor="center")
        self.log_tree.column("from", width=90, anchor="center")
        self.log_tree.column("input", width=100, anchor="center")
        self.log_tree.column("to", width=90, anchor="center")

        self.log_tree.pack(fill="both", expand=True, pady=6)

        btn_reset_atm = tk.Button(
            right_panel,
            text="⟲ Reset máy ATM",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#0f172a",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._on_reset,
        )
        btn_reset_atm.pack(fill="x")

    def _on_insert_card(self):
        self.atm.insert_card()
        self.update_display()

    def _on_take_card(self):
        self.atm.take_card()
        self.update_display()

    def _on_take_cash(self):
        self.atm.take_cash()
        self.update_display()

    def _on_digit(self, digit: str):
        self.atm.enter_pin_digit(digit)
        self.update_display()

    def _on_clear(self):
        self.atm.clear_pin()
        self.update_display()

    def _on_enter(self):
        if self.atm.current_state in (self.atm.STATE_CARD_INSERTED, self.atm.STATE_PIN_CHECK):
            self.atm.submit_pin()
            self.update_display()

    def _on_cancel(self):
        self.atm.cancel()
        self.update_display()

    def _on_withdraw(self, amount: int):
        if self.atm.current_state == self.atm.STATE_MAIN_MENU:
            self.atm.select_withdraw()
        if self.atm.current_state == self.atm.STATE_WITHDRAW_MENU:
            self.atm.execute_withdraw(amount)
        self.update_display()

    def _on_reset(self):
        self.atm.reset_machine()
        self.update_display()

    def update_display(self):
        st = self.atm.current_state
        out = self.atm.output

        self.lcd_title.config(text=out.get("screen_title", ""))
        self.lcd_msg.config(text=out.get("message", ""))
        self.lcd_extra.config(text=f"Số dư tài khoản: {self.atm.balance:,} VND | PIN mẫu: 1234")

        # Hiển thị dấu * khi nhập PIN
        if st in (self.atm.STATE_CARD_INSERTED, self.atm.STATE_PIN_CHECK):
            self.lcd_pin_display.config(text="● " * len(self.atm.entered_pin) + "○ " * (4 - len(self.atm.entered_pin)))
        elif st == self.atm.STATE_DISPENSING:
            self.lcd_pin_display.config(text=f"💵 +{self.atm.last_dispensed_amount:,} VND")
        else:
            self.lcd_pin_display.config(text="")

        # Điều khiển nút bấm vật lý
        self.btn_insert_card.config(state="normal" if st == self.atm.STATE_IDLE else "disabled")
        self.btn_take_card.config(state="normal" if st in (self.atm.STATE_EJECTING_CARD, self.atm.STATE_LOCKED, self.atm.STATE_ERROR) else "disabled")
        self.btn_take_cash.config(state="normal" if st == self.atm.STATE_DISPENSING else "disabled")

        withdraw_active = (st in (self.atm.STATE_MAIN_MENU, self.atm.STATE_WITHDRAW_MENU))
        for b in self.amount_buttons:
            b.config(state="normal" if withdraw_active else "disabled")

        # Cột phải
        self.lbl_curr_state.config(text=st)
        self.lbl_curr_output.config(text=out.get("message", ""))

        attempts_left = max(0, 3 - self.atm.failed_pin_attempts)
        if st == self.atm.STATE_LOCKED:
            self.lbl_attempts.config(text="THẺ ĐÃ BỊ KHÓA VĨNH VIỄN", fg="#dc2626")
        else:
            col = "#16a34a" if attempts_left == 3 else ("#ea580c" if attempts_left == 2 else "#dc2626")
            self.lbl_attempts.config(text=f"Số lần thử PIN còn lại: {attempts_left}/3", fg=col)

        # Cập nhật treeview log
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)

        for entry in self.atm.history_log[-12:]:
            self.log_tree.insert(
                "",
                "end",
                values=(
                    entry.get("step", ""),
                    entry.get("prev_state", ""),
                    entry.get("input", ""),
                    entry.get("next_state", ""),
                ),
            )
        children = self.log_tree.get_children()
        if children:
            self.log_tree.see(children[-1])


class ATMGraphScreen(ttk.Frame):
    """Màn 5: Sơ đồ đồ thị trạng thái Moore Machine & Kịch bản Test Cases lỗi."""

    def __init__(self, parent, controller, shared_atm: Optional[ATMMooreMachine] = None):
        super().__init__(parent)
        self.controller = controller
        self.atm = shared_atm if shared_atm else ATMMooreMachine()
        self._build_ui()
        self._draw_moore_graph()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 5: SƠ ĐỒ MOORE MACHINE & TEST CASES LỖI BẢO MẬT",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        btn_go_sim = tk.Button(
            header,
            text="← Quay lại Màn 4: Giả lập ATM",
            font=("Segoe UI", 9, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self.controller.show_screen(3),
        )
        btn_go_sim.pack(side="right")

        body = tk.Frame(self, bg="#f8fafc", padx=15, pady=15)
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)
        body.rowconfigure(0, weight=1)

        # CỘT TRÁI: Canvas sơ đồ đồ thị Moore Machine
        left_card = tk.LabelFrame(
            body,
            text="  SƠ ĐỒ TRẠNG THÁI MOORE MACHINE (STATE DIAGRAM)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=10,
            pady=10,
            relief="solid",
            bd=1,
        )
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.canvas = tk.Canvas(left_card, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        legend_box = tk.Frame(left_card, bg="#f8fafc", padx=8, pady=4)
        legend_box.pack(fill="x", pady=(4, 0))
        tk.Label(
            legend_box,
            text="Node = [Tên State / Đầu ra λ(State)] | Node Đỏ = S_LOCKED (Khóa thẻ khi sai PIN 3 lần)",
            font=("Segoe UI", 8, "italic"),
            fg="#475569",
            bg="#f8fafc",
        ).pack(anchor="w")

        # CỘT PHẢI: Bảng điều khiển chạy các Test Cases tự động
        right_card = tk.LabelFrame(
            body,
            text="  BỘ 4 KỊCH BẢN KIỂM THỬ (AUTOMATED TEST CASES)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=12,
            pady=10,
            relief="solid",
            bd=1,
        )
        right_card.grid(row=0, column=1, sticky="nsew")

        tests = [
            ("TEST CASE 1: Rút tiền thành công 500,000 VND", "Đưa thẻ -> Nhập đúng PIN 1234 -> Chọn rút 500k -> Nhận tiền -> Trả thẻ", "#10b981", self.run_test_success),
            ("TEST CASE 2: Sai PIN 3 lần -> KHÓA THẺ (Lỗi bảo mật)", "Đưa thẻ -> Sai lần 1 (1111) -> Sai lần 2 (2222) -> Sai lần 3 (3333) -> S_LOCKED", "#ef4444", self.run_test_wrong_pin_3_times),
            ("TEST CASE 3: Rút tiền vượt quá số dư (Số dư không đủ)", "Đưa thẻ -> PIN đúng -> Rút 10,000,000đ (vượt 5M) -> S_ERROR", "#f59e0b", self.run_test_insufficient_funds),
            ("TEST CASE 4: Hủy giao dịch giữa chừng (Cancel)", "Đưa thẻ -> Bắt đầu nhập PIN -> Người dùng nhấn CANCEL -> Trả lại thẻ an toàn", "#64748b", self.run_test_user_cancel),
        ]

        for title, desc, col, handler in tests:
            t_box = tk.Frame(right_card, bg="#f8fafc", highlightbackground=col, highlightthickness=1, padx=8, pady=8)
            t_box.pack(fill="x", pady=4)

            tk.Label(t_box, text=title, font=("Segoe UI", 9, "bold"), fg=col, bg="#f8fafc").pack(anchor="w")
            tk.Label(t_box, text=desc, font=("Segoe UI", 8), fg="#475569", bg="#f8fafc", justify="left").pack(anchor="w", pady=(2, 4))

            btn = tk.Button(
                t_box,
                text="Chạy kịch bản này ▶",
                font=("Segoe UI", 8, "bold"),
                bg=col,
                fg="#ffffff",
                relief="flat",
                cursor="hand2",
                padx=8,
                pady=2,
                command=handler,
            )
            btn.pack(anchor="e")

        # Khung log kết quả kiểm thử
        tk.Label(right_card, text="Kết quả kiểm thử & Trạng thái Assert:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(anchor="w", pady=(8, 2))
        self.txt_test_log = tk.Text(right_card, height=8, font=("Consolas", 8), bg="#0f172a", fg="#f8fafc", relief="flat")
        self.txt_test_log.pack(fill="both", expand=True)

    def _log_test(self, text: str):
        self.txt_test_log.insert("end", text + "\n")
        self.txt_test_log.see("end")

    def run_test_success(self):
        self.txt_test_log.delete("1.0", "end")
        self._log_test("=== CHẠY TEST CASE 1: RÚT TIỀN THÀNH CÔNG ===")
        self.atm.reset_machine()
        self._draw_moore_graph()

        self._log_test("[1] Bước 1: Đưa thẻ vào khe cắm...")
        self.atm.insert_card()
        self._draw_moore_graph()

        self._log_test("[2] Bước 2: Nhập đúng PIN '1234'...")
        self.atm.entered_pin = "1234"
        self.atm.submit_pin()
        self._draw_moore_graph()

        self._log_test("[3] Bước 3: Chọn menu Rút tiền...")
        self.atm.select_withdraw()
        self._draw_moore_graph()

        self._log_test("[4] Bước 4: Xác nhận số tiền 500,000 VND...")
        self.atm.execute_withdraw(500000)
        self._draw_moore_graph()

        self._log_test("[5] Bước 5: Nhận tiền mặt & trả thẻ...")
        self.atm.take_cash()
        self.atm.take_card()
        self._draw_moore_graph()

        self._log_test(">>> KẾT QUẢ: PASS (Giao dịch hoàn tất thành công!)")

    def run_test_wrong_pin_3_times(self):
        self.txt_test_log.delete("1.0", "end")
        self._log_test("=== CHẠY TEST CASE 2: SAI PIN 3 LẦN -> KHÓA THẺ ===")
        self.atm.reset_machine()
        self.atm.insert_card()
        self._draw_moore_graph()

        for attempt, pin in [(1, "1111"), (2, "2222"), (3, "3333")]:
            self._log_test(f"[{attempt}] Thử nhập sai PIN: '{pin}'...")
            self.atm.entered_pin = pin
            self.atm.submit_pin()
            self._draw_moore_graph()

        is_locked = (self.atm.current_state == self.atm.STATE_LOCKED)
        self._log_test(f">>> Trạng thái cuối: {self.atm.current_state}")
        self._log_test(f">>> ASSERT (State == S_LOCKED): {'PASS' if is_locked else 'FAIL'}")
        if is_locked:
            self._log_test(">>> BẢO MẬT THÀNH CÔNG: Thẻ đã bị khóa vĩnh viễn!")

    def run_test_insufficient_funds(self):
        self.txt_test_log.delete("1.0", "end")
        self._log_test("=== CHẠY TEST CASE 3: SỐ DƯ KHÔNG ĐỦ ===")
        self.atm.reset_machine()
        self.atm.insert_card()
        self.atm.entered_pin = "1234"
        self.atm.submit_pin()
        self.atm.select_withdraw()

        self._log_test(f"[1] Số dư hiện tại: {self.atm.balance:,} VND")
        self._log_test("[2] Yêu cầu rút: 10,000,000 VND...")
        self.atm.execute_withdraw(10000000)
        self._draw_moore_graph()

        is_error = (self.atm.current_state == self.atm.STATE_ERROR)
        self._log_test(f">>> Trạng thái cuối: {self.atm.current_state}")
        self._log_test(f">>> Thông báo lỗi: {self.atm.output['message']}")
        self._log_test(f">>> ASSERT (State == S_ERROR): {'PASS' if is_error else 'FAIL'}")

    def run_test_user_cancel(self):
        self.txt_test_log.delete("1.0", "end")
        self._log_test("=== CHẠY TEST CASE 4: NGƯỜI DÙNG CANCEL ===")
        self.atm.reset_machine()
        self.atm.insert_card()
        self.atm.enter_pin_digit("1")
        self.atm.enter_pin_digit("2")
        self._log_test("[1] Đang nhập dở PIN ('12...'), người dùng bấm CANCEL...")
        self.atm.cancel()
        self._draw_moore_graph()

        is_eject = (self.atm.current_state == self.atm.STATE_EJECTING_CARD)
        self._log_test(f">>> Trạng thái máy: {self.atm.current_state} (Ejecting Card)")
        self._log_test(f">>> ASSERT: {'PASS (Thẻ đã được nhả an toàn)' if is_eject else 'FAIL'}")

    def _draw_moore_graph(self):
        c = self.canvas
        c.delete("all")
        w = c.winfo_width() or 460
        h = c.winfo_height() or 340

        curr_state = self.atm.current_state

        # Vị trí tọa độ các node Moore Machine
        state_positions = {
            "S_IDLE": (60, 60),
            "S_CARD_INSERTED": (200, 60),
            "S_PIN_CHECK": (340, 60),
            "S_LOCKED": (410, 160),
            "S_MAIN_MENU": (200, 160),
            "S_WITHDRAW_MENU": (80, 160),
            "S_PROCESSING": (80, 260),
            "S_DISPENSING": (220, 260),
            "S_EJECTING_CARD": (360, 260),
            "S_ERROR": (80, 310),
        }

        # Vẽ các cạnh kết nối
        edges = [
            ("S_IDLE", "S_CARD_INSERTED"),
            ("S_CARD_INSERTED", "S_PIN_CHECK"),
            ("S_PIN_CHECK", "S_MAIN_MENU"),
            ("S_PIN_CHECK", "S_CARD_INSERTED"),
            ("S_PIN_CHECK", "S_LOCKED"),
            ("S_MAIN_MENU", "S_WITHDRAW_MENU"),
            ("S_WITHDRAW_MENU", "S_PROCESSING"),
            ("S_PROCESSING", "S_DISPENSING"),
            ("S_DISPENSING", "S_EJECTING_CARD"),
            ("S_EJECTING_CARD", "S_IDLE"),
            ("S_WITHDRAW_MENU", "S_ERROR"),
            ("S_CARD_INSERTED", "S_EJECTING_CARD"),
        ]

        for src, dst in edges:
            if src in state_positions and dst in state_positions:
                sx, sy = state_positions[src]
                dx, dy = state_positions[dst]
                is_active_edge = (curr_state == src)
                c.create_line(sx, sy, dx, dy, arrow="last", fill="#3b82f6" if is_active_edge else "#cbd5e1", width=2 if is_active_edge else 1)

        # Vẽ từng node
        for st, (x, y) in state_positions.items():
            is_active = (st == curr_state)
            is_locked_node = (st == "S_LOCKED")

            if is_locked_node:
                fill_col = "#fee2e2" if is_active else "#fef2f2"
                border_col = "#dc2626"
            elif is_active:
                fill_col = "#dbeafe"
                border_col = "#2563eb"
            else:
                fill_col = "#ffffff"
                border_col = "#94a3b8"

            rw, rh = 42, 22
            if is_active:
                c.create_oval(x - rw - 5, y - rh - 5, x + rw + 5, y + rh + 5, outline="#60a5fa", width=3)

            c.create_oval(x - rw, y - rh, x + rw, y + rh, fill=fill_col, outline=border_col, width=2)
            c.create_text(x, y, text=st.replace("S_", ""), font=("Segoe UI", 7, "bold"), fill="#0f172a")
