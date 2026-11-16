"""
Màn 6: Máy bán hàng tự động (Vending Machine DFA).
[PHẦN PHÂN CÔNG CỦA HÂN - THEO PLAN.MD]

Ghi chú cho Hân:
- Màn này do Hân phụ trách thiết kế UI và logic nạp coin (5k, 10k, 20k), hiển thị tủ nước và khay trả tiền thừa.
- Có thể import và tái sử dụng bộ điều khiển `VendingMachineController` từ `src.controller`.
"""

import tkinter as tk
from tkinter import ttk


class VendingScreen(ttk.Frame):
    """Màn 6: Máy bán hàng tự động — Placeholder cho Hân thực hiện."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg="#1e293b", padx=20, pady=12)
        header.pack(fill="x")

        tk.Label(
            header,
            text="MÀN 6: MÁY BÁN HÀNG TỰ ĐỘNG (VENDING MACHINE DFA)",
            font=("Segoe UI", 13, "bold"),
            fg="#f8fafc",
            bg="#1e293b",
        ).pack(side="left")

        # Khung Placeholder cho Hân
        body = tk.Frame(self, bg="#f8fafc", padx=30, pady=40)
        body.pack(fill="both", expand=True)

        card = tk.Frame(
            body,
            bg="#ffffff",
            highlightbackground="#f59e0b",
            highlightthickness=2,
            padx=30,
            pady=30,
            relief="solid",
            bd=1,
        )
        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="🥤 [MÀN 6: PHẦN PHÂN CÔNG CỦA HÂN]",
            font=("Segoe UI", 14, "bold"),
            fg="#d97706",
            bg="#ffffff",
        ).pack(pady=(0, 10))

        desc = (
            "Kế hoạch Stage 2 của Hân:\n"
            "• Thiết kế giao diện tủ bán nước (Aquafina 5k, Coca 10k, Red Bull 15k, Cà phê 20k)\n"
            "• Các nút nạp coin/tiền giấy: 5.000đ, 10.000đ, 20.000đ\n"
            "• Khay nhận nước (ra hàng) & Khay thối tiền thừa\n"
            "• Bảng hiển thị DFA: Trạng thái hiện tại = Tổng tiền đã nạp (0k, 5k, 10k, ...)\n"
            "• Gợi ý: Có thể dùng trực tiếp `src/controller.py: VendingMachineController` đã chuẩn bị sẵn!"
        )
        tk.Label(
            card,
            text=desc,
            font=("Segoe UI", 11),
            fg="#334155",
            bg="#ffffff",
            justify="left",
        ).pack(pady=10)

        info_box = tk.Frame(card, bg="#fffbeb", padx=15, pady=10, relief="groove", bd=1)
        info_box.pack(fill="x", pady=15)
        tk.Label(
            info_box,
            text="Trạng thái: Đang chờ Hân hoàn thiện giao diện (Minh đã dựng sẵn khung sườn và controller)",
            font=("Segoe UI", 10, "italic"),
            fg="#b45309",
            bg="#fffbeb",
        ).pack()
