"""
Màn 2 & Màn 3: Hệ thống điều khiển Đèn giao thông dựa trên DFA.
[PHẦN PHÂN CÔNG CỦA HÂN - THEO PLAN.MD]

Ghi chú cho Hân:
- Màn 2: Traffic Light — Animation ngã tư đèn giao thông + Sơ đồ đồ thị trạng thái DFA.
- Màn 3: Traffic Light — Step-by-step, bảng transition log chi tiết.
- Có thể kết nối trực tiếp với `src/controller.py: TrafficLightController`.
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from src.controller import TrafficLightController


class TrafficSimScreen(ttk.Frame):
    """Màn 2: Mô phỏng đèn giao thông ngã tư 4 pha và đồ thị DFA động."""

    def __init__(self, parent, controller, shared_tl: Optional[TrafficLightController] = None):
        super().__init__(parent)
        self.controller = controller
        self.tl = shared_tl if shared_tl else TrafficLightController()
        self.is_running = False
        self.timer_id = None
        self.delay_ms = 1000

        self._build_ui()
        self.update_display()

    def _build_ui(self):
        # Header bar
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 2: MÔ PHỎNG ĐÈN GIAO THÔNG & ĐỒ THỊ TRẠNG THÁI DFA",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        btn_go_log = tk.Button(
            header,
            text="Sang Màn 3: Bảng chuyển trạng thái & Log →",
            font=("Segoe UI", 9, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self.controller.show_screen(2),
        )
        btn_go_log.pack(side="right")

        # Khung nội dung chính chia 2 cột: Trái (Cột đèn + Ngã tư), Phải (Sơ đồ DFA)
        body = tk.Frame(self, bg="#f8fafc", padx=15, pady=15)
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        # CỘT TRÁI: Mô phỏng đèn ngã tư
        left_card = tk.LabelFrame(
            body,
            text="  MÔ PHỎNG TRỰC QUAN NGÃ TƯ  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=15,
            pady=10,
            relief="solid",
            bd=1,
        )
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Canvas vẽ ngã tư và đèn
        self.sim_canvas = tk.Canvas(left_card, bg="#334155", height=280, highlightthickness=0)
        self.sim_canvas.pack(fill="both", expand=True, pady=(0, 10))

        # Khung thông tin đếm lùi & trạng thái hiện tại
        status_bar = tk.Frame(left_card, bg="#f1f5f9", padx=10, pady=8, relief="groove", bd=1)
        status_bar.pack(fill="x", pady=(0, 10))

        self.lbl_status = tk.Label(
            status_bar,
            text="Pha hiện tại: KHỞI ĐỘNG",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#f1f5f9",
        )
        self.lbl_status.pack(side="left")

        self.lbl_countdown = tk.Label(
            status_bar,
            text="Đếm lùi: 15s",
            font=("Segoe UI", 12, "bold"),
            fg="#2563eb",
            bg="#f1f5f9",
        )
        self.lbl_countdown.pack(side="right")

        # Bộ điều khiển nút bấm
        ctrl_box = tk.Frame(left_card, bg="#ffffff")
        ctrl_box.pack(fill="x")

        self.btn_play = tk.Button(
            ctrl_box,
            text="▶ Bắt đầu (Play)",
            font=("Segoe UI", 9, "bold"),
            bg="#10b981",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.toggle_play,
        )
        self.btn_play.pack(side="left", padx=(0, 6))

        self.btn_step = tk.Button(
            ctrl_box,
            text="⏭ Bước kế (Step)",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#0f172a",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.step_once,
        )
        self.btn_step.pack(side="left", padx=(0, 6))

        self.btn_emergency = tk.Button(
            ctrl_box,
            text="🚨 Xe cứu thương (Khẩn cấp)",
            font=("Segoe UI", 9, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.toggle_emergency,
        )
        self.btn_emergency.pack(side="left", padx=(0, 6))

        self.btn_reset = tk.Button(
            ctrl_box,
            text="⟲ Reset",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#0f172a",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=6,
            command=self.reset_sim,
        )
        self.btn_reset.pack(side="right")

        # Tốc độ
        speed_box = tk.Frame(left_card, bg="#ffffff")
        speed_box.pack(fill="x", pady=(8, 0))
        tk.Label(speed_box, text="Tốc độ:", font=("Segoe UI", 8), bg="#ffffff", fg="#64748b").pack(side="left")
        
        for label, ms in [("0.5x (Chậm)", 2000), ("1.0x (Chuẩn)", 1000), ("2.0x (Nhanh)", 500)]:
            rb = tk.Radiobutton(
                speed_box,
                text=label,
                value=ms,
                font=("Segoe UI", 8),
                bg="#ffffff",
                variable=tk.IntVar(value=self.delay_ms),
                command=lambda val=ms: self.set_speed(val),
            )
            rb.pack(side="left", padx=5)

        # CỘT PHẢI: Sơ đồ đồ thị DFA
        right_card = tk.LabelFrame(
            body,
            text="  ĐỒ THỊ CHUYỂN TRẠNG THÁI DFA (ACTIVE STATE HIGHLIGHT)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=15,
            pady=10,
            relief="solid",
            bd=1,
        )
        right_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.dfa_canvas = tk.Canvas(right_card, bg="#ffffff", highlightthickness=0)
        self.dfa_canvas.pack(fill="both", expand=True)

        legend_box = tk.Frame(right_card, bg="#f8fafc", padx=8, pady=5)
        legend_box.pack(fill="x", pady=(6, 0))
        tk.Label(
            legend_box,
            text="● Vòng tròn xanh/vàng/đỏ: Trạng thái đang kích hoạt | Mũi tên: Chuyển trạng thái khi hết thời gian (TIMEOUT)",
            font=("Segoe UI", 8, "italic"),
            fg="#475569",
            bg="#f8fafc",
        ).pack(anchor="w")

    def set_speed(self, ms: int):
        self.delay_ms = ms

    def toggle_play(self):
        if not self.is_running:
            self.is_running = True
            self.btn_play.config(text="⏸ Tạm dừng", bg="#f59e0b")
            self._timer_loop()
        else:
            self.is_running = False
            self.btn_play.config(text="▶ Tiếp tục", bg="#10b981")
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

    def _timer_loop(self):
        if not self.is_running:
            return
        self.tl.tick_second()
        self.update_display()
        self.timer_id = self.after(self.delay_ms, self._timer_loop)

    def step_once(self):
        if self.is_running:
            self.toggle_play()
        self.tl.manual_step()
        self.update_display()

    def toggle_emergency(self):
        self.tl.toggle_emergency()
        if self.tl.is_emergency:
            self.btn_emergency.config(text="Tắt khẩn cấp (Hồi phục)", bg="#475569")
        else:
            self.btn_emergency.config(text="🚨 Xe cứu thương (Khẩn cấp)", bg="#ef4444")
        self.update_display()

    def reset_sim(self):
        if self.is_running:
            self.toggle_play()
        self.tl.reset()
        self.btn_emergency.config(text="🚨 Xe cứu thương (Khẩn cấp)", bg="#ef4444")
        self.update_display()

    def update_display(self):
        curr = self.tl.current_state
        time_left = self.tl.time_left
        signals = self.tl.get_light_signals()

        # Cập nhật nhãn trạng thái
        state_names = {
            "NS_GREEN": "PHA 1: BẮC - NAM XANH | ĐÔNG - TÂY ĐỎ",
            "NS_YELLOW": "PHA 2: BẮC - NAM VÀNG | ĐÔNG - TÂY ĐỎ",
            "EW_GREEN": "PHA 3: ĐÔNG - TÂY XANH | BẮC - NAM ĐỎ",
            "EW_YELLOW": "PHA 4: ĐÔNG - TÂY VÀNG | BẮC - NAM ĐỎ",
            "EMERGENCY_ALL_RED": "🚨 CHẾ ĐỘ ƯU TIÊN KHẨN CẤP: TẤT CẢ ĐÈN ĐỎ",
        }
        self.lbl_status.config(text=state_names.get(curr, curr))
        if curr == "EMERGENCY_ALL_RED":
            self.lbl_countdown.config(text="CỨU THƯƠNG ĐANG QUA", fg="#ef4444")
        else:
            self.lbl_countdown.config(text=f"Đếm lùi: {time_left:02d}s", fg="#2563eb")

        # Vẽ mô phỏng ngã tư
        self._draw_intersection(signals, curr, time_left)
        # Vẽ sơ đồ đồ thị DFA
        self._draw_dfa_graph(curr)

    def _draw_intersection(self, signals, curr_state, time_left):
        c = self.sim_canvas
        c.delete("all")
        w = c.winfo_width() or 380
        h = c.winfo_height() or 260
        cx, cy = w / 2, h / 2

        # 1. Mặt đường ngã tư
        rw = 110  # bề rộng lòng đường
        c.create_rectangle(0, cy - rw / 2, w, cy + rw / 2, fill="#1e293b", outline="")
        c.create_rectangle(cx - rw / 2, 0, cx + rw / 2, h, fill="#1e293b", outline="")
        # Vạch kẻ đường đứt nét
        c.create_line(0, cy, cx - rw / 2, cy, fill="#e2e8f0", dash=(6, 6), width=2)
        c.create_line(cx + rw / 2, cy, w, cy, fill="#e2e8f0", dash=(6, 6), width=2)
        c.create_line(cx, 0, cx, cy - rw / 2, fill="#e2e8f0", dash=(6, 6), width=2)
        c.create_line(cx, cy + rw / 2, cx, h, fill="#e2e8f0", dash=(6, 6), width=2)

        # 2. Cột đèn Bắc - Nam (Đặt ở góc Tây - Bắc)
        self._draw_traffic_box(c, cx - rw / 2 - 45, cy - rw / 2 - 75, signals["NS"], "BẮC - NAM", time_left if "NS" in curr_state else None)

        # 3. Cột đèn Đông - Tây (Đặt ở góc Đông - Nam)
        self._draw_traffic_box(c, cx + rw / 2 + 10, cy + rw / 2 + 10, signals["EW"], "ĐÔNG - TÂY", time_left if "EW" in curr_state else None)

    def _draw_traffic_box(self, c, x, y, light_sig, label, timer_val):
        box_w, box_h = 36, 80
        c.create_rectangle(x, y, x + box_w, y + box_h, fill="#0f172a", outline="#cbd5e1", width=2)

        # Đèn Đỏ
        r_color = "#ef4444" if light_sig["red"] else "#450a0a"
        c.create_oval(x + 8, y + 6, x + 28, y + 26, fill=r_color, outline="#1e293b")
        if light_sig["red"]:
            c.create_oval(x + 6, y + 4, x + 30, y + 28, outline="#fca5a5", width=2)

        # Đèn Vàng
        y_color = "#f59e0b" if light_sig["yellow"] else "#451a03"
        c.create_oval(x + 8, y + 30, x + 28, y + 50, fill=y_color, outline="#1e293b")
        if light_sig["yellow"]:
            c.create_oval(x + 6, y + 28, x + 30, y + 52, outline="#fde68a", width=2)

        # Đèn Xanh
        g_color = "#10b981" if light_sig["green"] else "#022c22"
        c.create_oval(x + 8, y + 54, x + 28, y + 74, fill=g_color, outline="#1e293b")
        if light_sig["green"]:
            c.create_oval(x + 6, y + 52, x + 30, y + 76, outline="#6ee7b7", width=2)

        # Nhãn tên hướng
        c.create_text(x + box_w / 2, y + box_h + 10, text=label, fill="#ffffff", font=("Segoe UI", 7, "bold"))
        if timer_val is not None:
            c.create_text(x + box_w / 2, y - 8, text=f"{timer_val}s", fill="#38bdf8", font=("Segoe UI", 9, "bold"))

    def _draw_dfa_graph(self, curr_state):
        c = self.dfa_canvas
        c.delete("all")
        w = c.winfo_width() or 380
        h = c.winfo_height() or 260
        cx, cy = w / 2, h / 2
        radius = min(w, h) * 0.35

        # 4 Trạng thái tạo thành vòng tròn
        nodes = {
            "NS_GREEN": {"label": "NS_GREEN\n(Xanh 15s)", "angle": -90, "base_col": "#10b981"},
            "NS_YELLOW": {"label": "NS_YELLOW\n(Vàng 3s)", "angle": 0, "base_col": "#f59e0b"},
            "EW_GREEN": {"label": "EW_GREEN\n(Xanh 15s)", "angle": 90, "base_col": "#10b981"},
            "EW_YELLOW": {"label": "EW_YELLOW\n(Vàng 3s)", "angle": 180, "base_col": "#f59e0b"},
        }

        node_coords = {}
        for st, info in nodes.items():
            rad = math.radians(info["angle"])
            nx = cx + radius * math.cos(rad)
            ny = cy + radius * math.sin(rad)
            node_coords[st] = (nx, ny)

        # Trạng thái khẩn cấp ở trung tâm
        em_coord = (cx, cy)
        node_coords["EMERGENCY_ALL_RED"] = em_coord

        # Vẽ mũi tên chu kỳ giữa các node
        cycle = [("NS_GREEN", "NS_YELLOW"), ("NS_YELLOW", "EW_GREEN"), ("EW_GREEN", "EW_YELLOW"), ("EW_YELLOW", "NS_GREEN")]
        for src, dst in cycle:
            sx, sy = node_coords[src]
            dx, dy = node_coords[dst]
            # Tính điểm cắt mép vòng tròn
            angle = math.atan2(dy - sy, dx - sx)
            p1x = sx + 28 * math.cos(angle)
            p1y = sy + 28 * math.sin(angle)
            p2x = dx - 28 * math.cos(angle)
            p2y = dy - 28 * math.sin(angle)

            is_active_edge = (curr_state == src)
            edge_col = "#2563eb" if is_active_edge else "#cbd5e1"
            edge_w = 3 if is_active_edge else 1
            c.create_line(p1x, p1y, p2x, p2y, arrow="last", fill=edge_col, width=edge_w, smooth=True)

        # Vẽ các node trạng thái
        for st, (nx, ny) in node_coords.items():
            is_active = (st == curr_state)
            r = 28 if st != "EMERGENCY_ALL_RED" else 24

            if st == "EMERGENCY_ALL_RED":
                fill_c = "#fee2e2" if is_active else "#f8fafc"
                border_c = "#ef4444" if is_active else "#94a3b8"
                txt_lbl = "EMERGENCY\n(ALL RED)"
                txt_col = "#dc2626"
            else:
                info = nodes[st]
                fill_c = "#dbeafe" if is_active else "#ffffff"
                border_c = info["base_col"] if not is_active else "#2563eb"
                txt_lbl = info["label"]
                txt_col = "#0f172a"

            if is_active:
                # Vòng hào quang sáng (Halo)
                c.create_oval(nx - r - 6, ny - r - 6, nx + r + 6, ny + r + 6, outline="#60a5fa", width=3)

            c.create_oval(nx - r, ny - r, nx + r, ny + r, fill=fill_c, outline=border_c, width=3 if is_active else 2)
            c.create_text(nx, ny, text=txt_lbl, font=("Segoe UI", 7, "bold" if is_active else "normal"), fill=txt_col, justify="center")


class TrafficLogScreen(ttk.Frame):
    """Màn 3: Bảng chuyển trạng thái DFA, phân tích toán học và Log sự kiện chi tiết."""

    def __init__(self, parent, controller, shared_tl: Optional[TrafficLightController] = None):
        super().__init__(parent)
        self.controller = controller
        self.tl = shared_tl if shared_tl else TrafficLightController()
        self._build_ui()
        self.refresh_log()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 3: BẢNG CHUYỂN TRẠNG THÁI DFA & TRANSITION LOG",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        btn_go_sim = tk.Button(
            header,
            text="← Quay lại Màn 2: Mô phỏng",
            font=("Segoe UI", 9, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self.controller.show_screen(1),
        )
        btn_go_sim.pack(side="right")

        body = tk.Frame(self, bg="#f8fafc", padx=15, pady=15)
        body.pack(fill="both", expand=True)

        # 1. Định nghĩa toán học DFA (M = Q, Sigma, delta, q0, F)
        math_card = tk.LabelFrame(
            body,
            text="  1. ĐỊNH NGHĨA HÌNH THỨC TOÁN HỌC DFA ĐÈN GIAO THÔNG  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=15,
            pady=10,
            relief="solid",
            bd=1,
        )
        math_card.pack(fill="x", pady=(0, 12))

        formula_text = (
            "M = (Q, Σ, δ, q₀, F)\n"
            "• Q = {NS_GREEN, NS_YELLOW, EW_GREEN, EW_YELLOW, EMERGENCY_ALL_RED}\n"
            "• Σ = {TIMEOUT, MANUAL_NEXT, EMERGENCY_ON, EMERGENCY_OFF, RESET}\n"
            "• q₀ = NS_GREEN (Pha xuất phát)\n"
            "• F = {NS_GREEN, EW_GREEN} (Các pha thông xe hợp lệ)\n"
            "• Hàm chuyển δ: δ(NS_G, TIMEOUT) = NS_Y;  δ(NS_Y, TIMEOUT) = EW_G;  δ(EW_G, TIMEOUT) = EW_Y;  δ(EW_Y, TIMEOUT) = NS_G"
        )
        tk.Label(
            math_card,
            text=formula_text,
            font=("Consolas", 9),
            fg="#1e293b",
            bg="#f8fafc",
            justify="left",
            padx=10,
            pady=6,
        ).pack(fill="x")

        # 2. Điều khiển Step thủ công & Tác vụ
        action_card = tk.Frame(body, bg="#ffffff", padx=12, pady=10, relief="solid", bd=1)
        action_card.pack(fill="x", pady=(0, 12))

        tk.Label(action_card, text="Thử nghiệm kích hoạt sự kiện đầu vào:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side="left", padx=(0, 10))

        btn_timeout = tk.Button(
            action_card,
            text="Gửi tín hiệu TIMEOUT",
            font=("Segoe UI", 9),
            bg="#2563eb",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._on_timeout,
        )
        btn_timeout.pack(side="left", padx=4)

        btn_em_on = tk.Button(
            action_card,
            text="🚨 EMERGENCY ON",
            font=("Segoe UI", 9, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._on_em_on,
        )
        btn_em_on.pack(side="left", padx=4)

        btn_em_off = tk.Button(
            action_card,
            text="EMERGENCY OFF",
            font=("Segoe UI", 9),
            bg="#475569",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._on_em_off,
        )
        btn_em_off.pack(side="left", padx=4)

        btn_clear = tk.Button(
            action_card,
            text="Xóa Log",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            fg="#0f172a",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._on_clear_log,
        )
        btn_clear.pack(side="right")

        # 3. Bảng Log Treeview
        log_card = tk.LabelFrame(
            body,
            text="  2. NHẬT KÝ CHUYỂN TRẠNG THÁI (TRANSITION LOG)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=10,
            pady=10,
            relief="solid",
            bd=1,
        )
        log_card.pack(fill="both", expand=True)

        cols = ("step", "prev", "input", "next", "time", "note")
        self.tree = ttk.Treeview(log_card, columns=cols, show="headings", height=10)
        self.tree.heading("step", text="Bước (#)")
        self.tree.heading("prev", text="Trạng thái trước (q_prev)")
        self.tree.heading("input", text="Sự kiện vào (σ)")
        self.tree.heading("next", text="Trạng thái sau (q_next)")
        self.tree.heading("time", text="Thời gian (s)")
        self.tree.heading("note", text="Chi tiết hành vi")

        self.tree.column("step", width=60, anchor="center")
        self.tree.column("prev", width=140, anchor="center")
        self.tree.column("input", width=130, anchor="center")
        self.tree.column("next", width=140, anchor="center")
        self.tree.column("time", width=80, anchor="center")
        self.tree.column("note", width=260, anchor="w")

        tree_scroll = ttk.Scrollbar(log_card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)

        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

    def _on_timeout(self):
        self.tl.trigger_input("TIMEOUT")
        self.refresh_log()

    def _on_em_on(self):
        self.tl.is_emergency = True
        self.tl.trigger_input("EMERGENCY_ON")
        self.refresh_log()

    def _on_em_off(self):
        self.tl.is_emergency = False
        self.tl.trigger_input("EMERGENCY_OFF")
        self.refresh_log()

    def _on_clear_log(self):
        self.tl.log = []
        self.refresh_log()

    def refresh_log(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for entry in self.tl.log:
            self.tree.insert(
                "",
                "end",
                values=(
                    entry.get("step", ""),
                    entry.get("prev_state", ""),
                    entry.get("input_event", ""),
                    entry.get("next_state", ""),
                    entry.get("time_left", ""),
                    entry.get("note", ""),
                ),
            )
        # Tự động cuộn xuống cuối
        children = self.tree.get_children()
        if children:
            self.tree.see(children[-1])
