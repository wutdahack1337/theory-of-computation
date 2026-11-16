"""
Màn 7 & Màn 8: Tìm kiếm chuỗi bằng NFA và Trực quan hóa thuật toán chuyển NFA sang DFA.
(Phần việc của Minh theo plan.md)
- PatternSearchScreen (Màn 7): Nhập text + pattern, NFA chạy từng bước, highlight active states và vị trí match.
- NfaToDfaScreen (Màn 8): Visualize thuật toán Subset Construction (bảng tập trạng thái D0, D1... & đồ thị DFA).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional
from src.pattern_search import PatternSearcher


class PatternSearchScreen(ttk.Frame):
    """Màn 7: Tìm kiếm chuỗi mẫu (Pattern Matching) sử dụng NFA."""

    DEFAULT_TEXT = "ATGCGATCGATGAACTGATG"
    DEFAULT_PATTERN = "ATG"

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.searcher = PatternSearcher(self.DEFAULT_PATTERN)
        self.trace_data = None
        self.current_step = 0
        self.is_playing = False
        self.timer_id = None

        self._build_ui()
        self._on_search()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 7: TÌM KIẾM CHUỖI MẪU BẰNG NFA (PATTERN MATCHING)",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        btn_go_dfa = tk.Button(
            header,
            text="Sang Màn 8: Visualize NFA → DFA (Subset Construction) →",
            font=("Segoe UI", 9, "bold"),
            bg="#8b5cf6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self.controller.show_screen(7),
        )
        btn_go_dfa.pack(side="right")

        body = tk.Frame(self, bg="#f8fafc", padx=15, pady=12)
        body.pack(fill="both", expand=True)

        # 1. Khung nhập liệu: Text và Pattern
        input_card = tk.LabelFrame(
            body,
            text="  1. ĐẦU VÀO TÌM KIẾM  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=12,
            pady=10,
            relief="solid",
            bd=1,
        )
        input_card.pack(fill="x", pady=(0, 10))

        # Row 1: Pattern
        row1 = tk.Frame(input_card, bg="#ffffff")
        row1.pack(fill="x", pady=(0, 6))

        tk.Label(row1, text="Chuỗi mẫu (Pattern):", font=("Segoe UI", 9, "bold"), bg="#ffffff", width=18, anchor="w").pack(side="left")
        self.ent_pattern = ttk.Entry(row1, font=("Consolas", 10), width=20)
        self.ent_pattern.insert(0, self.DEFAULT_PATTERN)
        self.ent_pattern.pack(side="left", padx=(0, 10))

        # Preset mẫu
        tk.Label(row1, text="Mẫu gợi ý:", font=("Segoe UI", 9), bg="#ffffff", fg="#64748b").pack(side="left")
        for sample_pat in ["ATG", "AAB", "101"]:
            btn_pat = tk.Button(
                row1,
                text=sample_pat,
                font=("Consolas", 8),
                bg="#f1f5f9",
                relief="flat",
                cursor="hand2",
                command=lambda p=sample_pat: self._set_preset(p),
            )
            btn_pat.pack(side="left", padx=3)

        btn_run = tk.Button(
            row1,
            text="🔍 Phân tích NFA & Tìm kiếm",
            font=("Segoe UI", 9, "bold"),
            bg="#2563eb",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=3,
            command=self._on_search,
        )
        btn_run.pack(side="right")

        # Row 2: Text
        row2 = tk.Frame(input_card, bg="#ffffff")
        row2.pack(fill="x")

        tk.Label(row2, text="Văn bản (Text):", font=("Segoe UI", 9, "bold"), bg="#ffffff", width=18, anchor="w").pack(side="left")
        self.ent_text = ttk.Entry(row2, font=("Consolas", 10))
        self.ent_text.insert(0, self.DEFAULT_TEXT)
        self.ent_text.pack(side="left", fill="x", expand=True)

        # 2. Khung giữa: Hiển thị văn bản highlight & điều khiển Step
        mid_box = tk.Frame(body, bg="#f8fafc")
        mid_box.pack(fill="x", pady=(0, 10))

        mid_box.columnconfigure(0, weight=3)
        mid_box.columnconfigure(1, weight=2)

        # Trái: Text highlight box
        text_card = tk.LabelFrame(
            mid_box,
            text="  2. THEO DÕI CON TRỎ DUYỆT & KẾT QUẢ MATCH  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=12,
            pady=8,
            relief="solid",
            bd=1,
        )
        text_card.grid(row=0, column=0, sticky="nsew", padx=(0, 6))

        # Hiển thị text dạng trực quan từng ô ký tự
        self.text_display_frame = tk.Frame(text_card, bg="#f1f5f9", padx=8, pady=8, relief="sunken", bd=1)
        self.text_display_frame.pack(fill="x", pady=(0, 8))

        self.char_labels = []

        # Điều khiển Play / Step
        step_ctrl = tk.Frame(text_card, bg="#ffffff")
        step_ctrl.pack(fill="x")

        self.btn_play = tk.Button(
            step_ctrl,
            text="▶ Chạy từng bước",
            font=("Segoe UI", 9, "bold"),
            bg="#10b981",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._toggle_auto_step,
        )
        self.btn_play.pack(side="left", padx=(0, 6))

        self.btn_next = tk.Button(
            step_ctrl,
            text="⏭ Ký tự kế tiếp",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._step_forward,
        )
        self.btn_next.pack(side="left", padx=(0, 6))

        self.btn_reset_step = tk.Button(
            step_ctrl,
            text="⟲ Về đầu",
            font=("Segoe UI", 9),
            bg="#f1f5f9",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._reset_step,
        )
        self.btn_reset_step.pack(side="left")

        self.lbl_step_info = tk.Label(step_ctrl, text="Bước 0/0", font=("Segoe UI", 9, "bold"), bg="#ffffff", fg="#2563eb")
        self.lbl_step_info.pack(side="right")

        # Phải: Thông tin trạng thái NFA tại bước hiện tại
        info_card = tk.LabelFrame(
            mid_box,
            text="  TẬP TRẠNG THÁI NFA HIỆN TẠI (ACTIVE STATES)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=12,
            pady=8,
            relief="solid",
            bd=1,
        )
        info_card.grid(row=0, column=1, sticky="nsew", padx=(6, 0))

        self.lbl_active_states = tk.Label(
            info_card,
            text="{q0}",
            font=("Consolas", 14, "bold"),
            fg="#7c3aed",
            bg="#f5f3ff",
            padx=10,
            pady=6,
            relief="groove",
            bd=1,
        )
        self.lbl_active_states.pack(fill="x", pady=(0, 6))

        self.lbl_match_found = tk.Label(
            info_card,
            text="Chưa tìm thấy khớp ở bước này",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#ffffff",
        )
        self.lbl_match_found.pack(anchor="w")

        self.lbl_total_matches = tk.Label(
            info_card,
            text="Tổng số lần khớp: 0",
            font=("Segoe UI", 9, "bold"),
            fg="#0f172a",
            bg="#ffffff",
        )
        self.lbl_total_matches.pack(anchor="w", pady=(4, 0))

        # 3. Khung dưới: Canvas đồ thị NFA
        graph_card = tk.LabelFrame(
            body,
            text="  3. SƠ ĐỒ ĐỒ THỊ CHUYỂN TRẠNG THÁI NFA CHO PATTERN  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=10,
            pady=8,
            relief="solid",
            bd=1,
        )
        graph_card.pack(fill="both", expand=True)

        self.canvas_nfa = tk.Canvas(graph_card, bg="#ffffff", height=130, highlightthickness=0)
        self.canvas_nfa.pack(fill="both", expand=True)

    def _set_preset(self, pat: str):
        self.ent_pattern.delete(0, "end")
        self.ent_pattern.insert(0, pat)
        if pat == "ATG":
            self.ent_text.delete(0, "end")
            self.ent_text.insert(0, "ATGCGATCGATGAACTGATG")
        elif pat == "AAB":
            self.ent_text.delete(0, "end")
            self.ent_text.insert(0, "AAABAABBAABAAB")
        elif pat == "101":
            self.ent_text.delete(0, "end")
            self.ent_text.insert(0, "110101100101101")
        self._on_search()

    def _on_search(self):
        pat = self.ent_pattern.get().strip()
        txt = self.ent_text.get().strip()
        if not pat or not txt:
            return

        self.searcher = PatternSearcher(pat)
        self.trace_data = self.searcher.search_with_trace(txt)
        self.current_step = 0

        self._render_text_cells(txt)
        self._update_step_view()
        self._draw_nfa_graph()

    def _render_text_cells(self, text: str):
        for w in self.text_display_frame.winfo_children():
            w.destroy()
        self.char_labels = []

        for idx, ch in enumerate(text):
            f = tk.Frame(self.text_display_frame, bg="#ffffff", highlightbackground="#cbd5e1", highlightthickness=1, padx=4, pady=2)
            f.pack(side="left", padx=1)

            lbl_ch = tk.Label(f, text=ch, font=("Consolas", 11, "bold"), bg="#ffffff", fg="#0f172a")
            lbl_ch.pack()

            lbl_idx = tk.Label(f, text=str(idx), font=("Segoe UI", 7), bg="#ffffff", fg="#94a3b8")
            lbl_idx.pack()

            self.char_labels.append({"frame": f, "char": lbl_ch, "idx": lbl_idx})

    def _update_step_view(self):
        if not self.trace_data:
            return

        steps = self.trace_data["step_trace"]
        total_steps = len(steps)
        if self.current_step >= total_steps:
            self.current_step = total_steps - 1

        step_info = steps[self.current_step]
        char_idx = step_info["char_index"]
        active = step_info["active_states"]
        is_match = step_info["is_match"]

        self.lbl_step_info.config(text=f"Bước {self.current_step} / {total_steps - 1}")
        self.lbl_active_states.config(text="{" + ", ".join(active) + "}")

        if is_match:
            span = step_info.get("match_span", (0, 0))
            self.lbl_match_found.config(text=f"★ TÌM THẤY MATCH TẠI VỊ TRÍ [{span[0]}..{span[1]-1}]!", fg="#16a34a", font=("Segoe UI", 9, "bold"))
        else:
            self.lbl_match_found.config(text=f"Đọc ký tự '{step_info['char']}' (index {char_idx})", fg="#64748b", font=("Segoe UI", 9))

        matches_so_far = sum(1 for s in steps[:self.current_step + 1] if s["is_match"])
        self.lbl_total_matches.config(text=f"Số lần khớp phát hiện: {matches_so_far} / {self.trace_data['total_matches']}")

        # Highlight ô text tương ứng
        for i, item in enumerate(self.char_labels):
            if i == char_idx:
                # Ký tự đang đọc
                item["frame"].config(bg="#fef08a", highlightbackground="#eab308")
                item["char"].config(bg="#fef08a", fg="#854d0e")
                item["idx"].config(bg="#fef08a")
            else:
                # Kiểm tra xem có thuộc phạm vi match nào đã tìm thấy không
                matched = False
                for s in steps[:self.current_step + 1]:
                    if s["is_match"] and s["match_span"]:
                        sp, ep = s["match_span"]
                        if sp <= i < ep:
                            matched = True
                            break
                if matched:
                    item["frame"].config(bg="#bbf7d0", highlightbackground="#22c55e")
                    item["char"].config(bg="#bbf7d0", fg="#14532d")
                    item["idx"].config(bg="#bbf7d0")
                else:
                    item["frame"].config(bg="#ffffff", highlightbackground="#cbd5e1")
                    item["char"].config(bg="#ffffff", fg="#0f172a")
                    item["idx"].config(bg="#ffffff")

        self._draw_nfa_graph(active)

    def _step_forward(self):
        if not self.trace_data:
            return
        if self.current_step < len(self.trace_data["step_trace"]) - 1:
            self.current_step += 1
            self._update_step_view()
        else:
            if self.is_playing:
                self._toggle_auto_step()

    def _reset_step(self):
        if self.is_playing:
            self._toggle_auto_step()
        self.current_step = 0
        self._update_step_view()

    def _toggle_auto_step(self):
        if not self.is_playing:
            self.is_playing = True
            self.btn_play.config(text="⏸ Dừng", bg="#f59e0b")
            self._run_auto_loop()
        else:
            self.is_playing = False
            self.btn_play.config(text="▶ Chạy từng bước", bg="#10b981")
            if self.timer_id:
                self.after_cancel(self.timer_id)
                self.timer_id = None

    def _run_auto_loop(self):
        if not self.is_playing:
            return
        if self.current_step < len(self.trace_data["step_trace"]) - 1:
            self.current_step += 1
            self._update_step_view()
            self.timer_id = self.after(600, self._run_auto_loop)
        else:
            self._toggle_auto_step()

    def _draw_nfa_graph(self, active_states=None):
        if active_states is None:
            active_states = {"q0"}

        c = self.canvas_nfa
        c.delete("all")
        w = c.winfo_width() or 600
        h = c.winfo_height() or 130
        cy = h / 2

        pat = self.searcher.pattern
        m = len(pat)
        spacing = min(120, (w - 80) / max(m, 1))
        start_x = 50

        # Vẽ self-loop tại q0
        c.create_arc(start_x - 20, cy - 45, start_x + 20, cy - 5, start=0, extent=200, style="arc", outline="#64748b", width=2)
        c.create_text(start_x, cy - 50, text="Σ (mọi ký tự)", font=("Segoe UI", 7), fill="#64748b")

        # Vẽ các cạnh chuyển tiếp
        for i in range(m):
            x1 = start_x + i * spacing
            x2 = start_x + (i + 1) * spacing
            c.create_line(x1 + 18, cy, x2 - 18, cy, arrow="last", fill="#2563eb", width=2)
            c.create_text((x1 + x2) / 2, cy - 14, text=pat[i], font=("Consolas", 10, "bold"), fill="#2563eb")

        # Vẽ các trạng thái q0, q1, ..., qm
        for i in range(m + 1):
            st_name = f"q{i}"
            x = start_x + i * spacing
            is_active = (st_name in active_states)
            is_accept = (i == m)

            fill_col = "#e9d5ff" if is_active else "#ffffff"
            border_col = "#7c3aed" if is_active else ("#10b981" if is_accept else "#64748b")

            if is_active:
                c.create_oval(x - 23, cy - 23, x + 23, cy + 23, outline="#c084fc", width=3)

            c.create_oval(x - 18, cy - 18, x + 18, cy + 18, fill=fill_col, outline=border_col, width=2)
            if is_accept:
                # Double circle cho accept state
                c.create_oval(x - 14, cy - 14, x + 14, cy + 14, outline=border_col, width=1)

            c.create_text(x, cy, text=st_name, font=("Segoe UI", 8, "bold"), fill="#0f172a")


class NfaToDfaScreen(ttk.Frame):
    """Màn 8: Trực quan hóa thuật toán chuyển đổi NFA sang DFA (Subset Construction)."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.searcher = PatternSearcher("ATG")
        self._build_ui()
        self._on_convert()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 8: TRỰC QUAN HÓA THUẬT TOÁN CHUYỂN NFA SANG DFA (SUBSET CONSTRUCTION)",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        btn_go_search = tk.Button(
            header,
            text="← Quay lại Màn 7: Pattern Search",
            font=("Segoe UI", 9, "bold"),
            bg="#3b82f6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=lambda: self.controller.show_screen(6),
        )
        btn_go_search.pack(side="right")

        body = tk.Frame(self, bg="#f8fafc", padx=15, pady=12)
        body.pack(fill="both", expand=True)

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(1, weight=1)

        # 1. Khung chọn Pattern đầu vào
        top_bar = tk.Frame(body, bg="#ffffff", padx=12, pady=10, relief="solid", bd=1)
        top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 10))

        tk.Label(top_bar, text="Chọn Pattern để chuyển sang DFA:", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(side="left", padx=(0, 10))
        self.ent_pattern = ttk.Entry(top_bar, font=("Consolas", 10), width=15)
        self.ent_pattern.insert(0, "ATG")
        self.ent_pattern.pack(side="left", padx=(0, 10))

        btn_conv = tk.Button(
            top_bar,
            text="⚡ Chạy thuật toán Subset Construction",
            font=("Segoe UI", 9, "bold"),
            bg="#8b5cf6",
            fg="#ffffff",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=3,
            command=self._on_convert,
        )
        btn_conv.pack(side="left", padx=4)

        self.lbl_stats = tk.Label(top_bar, text="", font=("Segoe UI", 9, "bold"), fg="#16a34a", bg="#ffffff")
        self.lbl_stats.pack(side="right")

        # CỘT TRÁI: Bảng ánh xạ tập con và các bước thuật toán
        left_card = tk.LabelFrame(
            body,
            text="  1. BẢNG ÁNH XẠ TẬP CON (SUBSET MAPPING: D0, D1...)  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=10,
            pady=10,
            relief="solid",
            bd=1,
        )
        left_card.grid(row=1, column=0, sticky="nsew", padx=(0, 6))

        cols_map = ("dfa_name", "nfa_subset", "is_accept")
        self.tree_map = ttk.Treeview(left_card, columns=cols_map, show="headings", height=8)
        self.tree_map.heading("dfa_name", text="Tên State DFA")
        self.tree_map.heading("nfa_subset", text="Tập hợp các State NFA tương ứng")
        self.tree_map.heading("is_accept", text="Trạng thái kết thúc (Accept)")

        self.tree_map.column("dfa_name", width=100, anchor="center")
        self.tree_map.column("nfa_subset", width=220, anchor="w")
        self.tree_map.column("is_accept", width=120, anchor="center")

        self.tree_map.pack(fill="x", pady=(0, 10))

        tk.Label(left_card, text="Lịch sử từng bước duyệt tập con (Queue Trace):", font=("Segoe UI", 9, "bold"), bg="#ffffff").pack(anchor="w")

        cols_steps = ("step", "from_d", "symbol", "to_d", "is_new")
        self.tree_steps = ttk.Treeview(left_card, columns=cols_steps, show="headings", height=9)
        self.tree_steps.heading("step", text="#")
        self.tree_steps.heading("from_d", text="Từ D_i")
        self.tree_steps.heading("symbol", text="Ký tự")
        self.tree_steps.heading("to_d", text="Đến D_j")
        self.tree_steps.heading("is_new", text="Tập con mới?")

        self.tree_steps.column("step", width=35, anchor="center")
        self.tree_steps.column("from_d", width=70, anchor="center")
        self.tree_steps.column("symbol", width=60, anchor="center")
        self.tree_steps.column("to_d", width=70, anchor="center")
        self.tree_steps.column("is_new", width=90, anchor="center")

        step_scroll = ttk.Scrollbar(left_card, orient="vertical", command=self.tree_steps.yview)
        self.tree_steps.configure(yscrollcommand=step_scroll.set)

        self.tree_steps.pack(side="left", fill="both", expand=True)
        step_scroll.pack(side="right", fill="y")

        # CỘT PHẢI: Ma trận chuyển trạng thái DFA & Đồ thị DFA kết quả
        right_card = tk.LabelFrame(
            body,
            text="  2. MA TRẬN CHUYỂN TRẠNG THÁI & ĐỒ THỊ DFA KẾT QUẢ  ",
            font=("Segoe UI", 10, "bold"),
            fg="#0f172a",
            bg="#ffffff",
            padx=10,
            pady=10,
            relief="solid",
            bd=1,
        )
        right_card.grid(row=1, column=1, sticky="nsew", padx=(6, 0))

        # Canvas vẽ đồ thị DFA
        self.canvas_dfa = tk.Canvas(right_card, bg="#ffffff", height=180, highlightthickness=0)
        self.canvas_dfa.pack(fill="both", expand=True, pady=(0, 10))

        # Bảng giải thích lý thuyết
        theory_box = tk.Frame(right_card, bg="#f8fafc", padx=10, pady=8, relief="groove", bd=1)
        theory_box.pack(fill="x")

        explanation = (
            "📌 Ý NGHĨA THỰC TIỄN CỦA SUBSET CONSTRUCTION:\n"
            "• NFA cho phép đoán nhận chuỗi linh hoạt nhưng khi thực thi phải lưu tập trạng thái.\n"
            "• DFA chỉ ở đúng 1 trạng thái duy nhất tại mỗi ký tự => Tốc độ tra cứu đạt O(|Text|) cực nhanh.\n"
            "• Đây chính là kỹ thuật cốt lõi trong lệnh grep, Lexer trình biên dịch và Antivirus scanning."
        )
        tk.Label(
            theory_box,
            text=explanation,
            font=("Segoe UI", 8),
            fg="#334155",
            bg="#f8fafc",
            justify="left",
        ).pack(anchor="w")

    def _on_convert(self):
        pat = self.ent_pattern.get().strip()
        if not pat:
            return

        self.searcher = PatternSearcher(pat)
        dfa, mapping, steps = self.searcher.convert_to_dfa()

        self.lbl_stats.config(
            text=f"Số trạng thái NFA: {len(self.searcher.nfa.states)} → Số trạng thái DFA: {len(dfa.states)}"
        )

        # Cập nhật bảng mapping D0, D1...
        for item in self.tree_map.get_children():
            self.tree_map.delete(item)

        for subset, d_name in sorted(mapping.items(), key=lambda x: x[1]):
            is_acc = d_name in dfa.accept_states
            subset_str = "{" + ", ".join(sorted(list(subset))) + "}"
            self.tree_map.insert("", "end", values=(d_name, subset_str, "★ CÓ (Accept)" if is_acc else "Không"))

        # Cập nhật bảng các bước queue
        for item in self.tree_steps.get_children():
            self.tree_steps.delete(item)

        for idx, s in enumerate(steps):
            self.tree_steps.insert(
                "",
                "end",
                values=(
                    idx + 1,
                    s["source_name"],
                    s["symbol"],
                    s["dest_name"],
                    "MỚI (+)" if s["is_new"] else "Đã có",
                ),
            )

        # Vẽ sơ đồ DFA trên canvas
        self._draw_dfa(dfa, mapping)

    def _draw_dfa(self, dfa, mapping):
        c = self.canvas_dfa
        c.delete("all")
        w = c.winfo_width() or 400
        h = c.winfo_height() or 180
        cy = h / 2

        states = sorted(list(dfa.states))
        n = len(states)
        spacing = min(90, (w - 60) / max(n, 1))
        start_x = 40

        coords = {}
        for i, s in enumerate(states):
            x = start_x + i * spacing
            coords[s] = (x, cy)

        # Vẽ các cung chuyển tiếp
        for (src, sym), dst in dfa.transition_function.items():
            if src in coords and dst in coords:
                sx, sy = coords[src]
                dx, dy = coords[dst]
                if src == dst:
                    # Self-loop
                    c.create_arc(sx - 15, sy - 35, sx + 15, sy - 5, start=0, extent=200, style="arc", outline="#94a3b8")
                    c.create_text(sx, sy - 40, text=sym, font=("Consolas", 7), fill="#64748b")
                else:
                    # Forward / backward
                    c.create_line(sx + 15, sy, dx - 15, dy, arrow="last", fill="#8b5cf6", width=1)
                    c.create_text((sx + dx) / 2, sy - 10, text=sym, font=("Consolas", 8, "bold"), fill="#8b5cf6")

        # Vẽ nodes
        for s, (x, y) in coords.items():
            is_acc = s in dfa.accept_states
            fill_c = "#f5f3ff" if is_acc else "#ffffff"
            border_c = "#10b981" if is_acc else "#6b7280"

            c.create_oval(x - 16, y - 16, x + 16, y + 16, fill=fill_c, outline=border_c, width=2)
            if is_acc:
                c.create_oval(x - 12, y - 12, x + 12, y + 12, outline=border_c, width=1)

            c.create_text(x, y, text=s, font=("Segoe UI", 8, "bold"), fill="#0f172a")
