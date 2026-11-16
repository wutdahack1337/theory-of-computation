"""
ATM Moore Machine - Mô hình hóa máy rút tiền tự động (ATM) bằng Moore Machine.
Trong Moore Machine, đầu ra (Output) phụ thuộc duy nhất vào trạng thái hiện tại (State),
thể hiện đặc trưng qua ánh xạ lambda: Q -> Delta.
"""

from typing import Any, Dict, List, Optional, Tuple


class ATMMooreMachine:
    """Mô hình Moore Machine cho hệ thống máy ATM."""

    CORRECT_PIN = "1234"
    INITIAL_BALANCE = 5000000  # 5,000,000 VND

    # Tập trạng thái Q
    STATE_IDLE = "S_IDLE"
    STATE_CARD_INSERTED = "S_CARD_INSERTED"
    STATE_PIN_CHECK = "S_PIN_CHECK"
    STATE_MAIN_MENU = "S_MAIN_MENU"
    STATE_WITHDRAW_MENU = "S_WITHDRAW_MENU"
    STATE_PROCESSING = "S_PROCESSING"
    STATE_DISPENSING = "S_DISPENSING"
    STATE_EJECTING_CARD = "S_EJECTING_CARD"
    STATE_LOCKED = "S_LOCKED"
    STATE_ERROR = "S_ERROR"

    # Hàm đầu ra Lambda: Q -> Output
    OUTPUT_MAP = {
        STATE_IDLE: {
            "screen_title": "CHÀO MỪNG QUÝ KHÁCH",
            "message": "Vui lòng đưa thẻ ATM vào khe nhận thẻ để bắt đầu.",
            "status_code": "READY_INSERT_CARD",
            "indicator": "green",
        },
        STATE_CARD_INSERTED: {
            "screen_title": "XÁC THỰC BẢO MẬT",
            "message": "Thẻ đã được nhận. Vui lòng nhập mã PIN (4 chữ số) và bấm ENTER.",
            "status_code": "WAIT_PIN_INPUT",
            "indicator": "blue",
        },
        STATE_PIN_CHECK: {
            "screen_title": "ĐANG KIỂM TRA",
            "message": "Đang giải mã và kiểm tra mã PIN với máy chủ ngân hàng...",
            "status_code": "VERIFYING_PIN",
            "indicator": "yellow",
        },
        STATE_MAIN_MENU: {
            "screen_title": "DANH MỤC GIAO DỊCH",
            "message": "Đăng nhập thành công! Vui lòng chọn chức năng bạn muốn thực hiện.",
            "status_code": "MENU_SELECTION",
            "indicator": "green",
        },
        STATE_WITHDRAW_MENU: {
            "screen_title": "RÚT TIỀN MẶT",
            "message": "Chọn số tiền muốn rút từ các phím chức năng hoặc nhập số khác.",
            "status_code": "CHOOSE_AMOUNT",
            "indicator": "blue",
        },
        STATE_PROCESSING: {
            "screen_title": "ĐANG XỬ LÝ GIAO DỊCH",
            "message": "Hệ thống đang đếm tiền mặt trong két... Xin vui lòng chờ.",
            "status_code": "COUNTING_CASH",
            "indicator": "yellow",
        },
        STATE_DISPENSING: {
            "screen_title": "TRẢ TIỀN & HÓA ĐƠN",
            "message": "Giao dịch thành công! Vui lòng nhận tiền mặt tại khe bên dưới.",
            "status_code": "DISPENSING_CASH",
            "indicator": "green",
        },
        STATE_EJECTING_CARD: {
            "screen_title": "TRẢ THẺ",
            "message": "Cảm ơn quý khách đã sử dụng dịch vụ. Xin vui lòng nhận lại thẻ!",
            "status_code": "EJECTING_CARD",
            "indicator": "blue",
        },
        STATE_LOCKED: {
            "screen_title": "CẢNH BÁO BẢO MẬT: KHÓA THẺ",
            "message": "Mã PIN đã nhập sai 3 lần liên tiếp! Thẻ đã bị khóa vì lý do an toàn.",
            "status_code": "CARD_LOCKED_FATAL",
            "indicator": "red",
        },
        STATE_ERROR: {
            "screen_title": "GIAO DỊCH KHÔNG THÀNH CÔNG",
            "message": "Số dư tài khoản không đủ hoặc vượt hạn mức rút trong ngày.",
            "status_code": "TRANSACTION_ERROR",
            "indicator": "red",
        },
    }

    def __init__(self):
        self.current_state = self.STATE_IDLE
        self.balance = self.INITIAL_BALANCE
        self.entered_pin = ""
        self.failed_pin_attempts = 0
        self.last_dispensed_amount = 0
        self.error_message = ""
        self.history_log: List[Dict[str, Any]] = []

        self._record_transition("INIT", self.STATE_IDLE, "Khởi động máy ATM")

    @property
    def output(self) -> Dict[str, Any]:
        """Hàm đầu ra Moore Lambda: Q -> Output."""
        out = dict(self.OUTPUT_MAP.get(self.current_state, {}))
        if self.current_state == self.STATE_ERROR and self.error_message:
            out["message"] = self.error_message
        return out

    def _record_transition(self, input_sym: str, next_state: str, note: str = ""):
        self.history_log.append({
            "step": len(self.history_log) + 1,
            "prev_state": getattr(self, "current_state", "NONE"),
            "input": input_sym,
            "next_state": next_state,
            "output_msg": self.OUTPUT_MAP.get(next_state, {}).get("message", ""),
            "attempts_left": max(0, 3 - self.failed_pin_attempts),
            "balance": self.balance,
            "note": note,
        })

    def transition_to(self, next_state: str, input_sym: str, note: str = ""):
        prev = self.current_state
        self.current_state = next_state
        self._record_transition(input_sym, next_state, note)
        return self.output

    def insert_card(self) -> Tuple[bool, Dict[str, Any]]:
        """Sự kiện đưa thẻ ATM vào máy."""
        if self.current_state != self.STATE_IDLE:
            return False, self.output
        self.entered_pin = ""
        self.failed_pin_attempts = 0
        self.transition_to(self.STATE_CARD_INSERTED, "INSERT_CARD", "Người dùng đưa thẻ vào")
        return True, self.output

    def enter_pin_digit(self, digit: str):
        """Nhập 1 chữ số PIN."""
        if self.current_state in (self.STATE_CARD_INSERTED, self.STATE_PIN_CHECK):
            if len(self.entered_pin) < 4 and digit.isdigit():
                self.entered_pin += digit

    def clear_pin(self):
        """Xóa mã PIN đang nhập."""
        self.entered_pin = ""

    def submit_pin(self) -> Tuple[bool, Dict[str, Any]]:
        """Bấm phím ENTER xác nhận PIN."""
        if self.current_state not in (self.STATE_CARD_INSERTED, self.STATE_PIN_CHECK):
            return False, self.output

        if len(self.entered_pin) != 4:
            self.error_message = "Mã PIN phải gồm đúng 4 chữ số!"
            return False, self.output

        self.transition_to(self.STATE_PIN_CHECK, "SUBMIT_PIN", "Kiểm tra mã PIN")

        if self.entered_pin == self.CORRECT_PIN:
            self.failed_pin_attempts = 0
            self.entered_pin = ""
            self.transition_to(self.STATE_MAIN_MENU, "PIN_CORRECT", "Mã PIN chính xác")
            return True, self.output
        else:
            self.failed_pin_attempts += 1
            attempts_left = 3 - self.failed_pin_attempts
            self.entered_pin = ""

            if self.failed_pin_attempts >= 3:
                self.transition_to(self.STATE_LOCKED, "PIN_WRONG_3_TIMES", "Sai PIN 3 lần -> KHÓA THẺ")
                return False, self.output
            else:
                self.error_message = f"Sai mã PIN! Quý khách còn {attempts_left} lần thử."
                self.transition_to(self.STATE_CARD_INSERTED, "PIN_WRONG", f"Sai PIN lần {self.failed_pin_attempts}")
                return False, self.output

    def select_withdraw(self) -> Tuple[bool, Dict[str, Any]]:
        """Người dùng chọn chức năng Rút tiền từ Menu."""
        if self.current_state != self.STATE_MAIN_MENU:
            return False, self.output
        self.transition_to(self.STATE_WITHDRAW_MENU, "SELECT_WITHDRAW", "Chọn menu Rút tiền")
        return True, self.output

    def execute_withdraw(self, amount: int) -> Tuple[bool, Dict[str, Any]]:
        """Người dùng xác nhận số tiền muốn rút."""
        if self.current_state != self.STATE_WITHDRAW_MENU:
            return False, self.output

        if amount <= 0 or amount % 50000 != 0:
            self.error_message = "Số tiền phải là bội số của 50,000 VND!"
            self.transition_to(self.STATE_ERROR, "INVALID_AMOUNT", self.error_message)
            return False, self.output

        if amount > self.balance:
            self.error_message = f"Số dư không đủ! Số dư hiện tại: {self.balance:,} VND"
            self.transition_to(self.STATE_ERROR, "INSUFFICIENT_FUNDS", self.error_message)
            return False, self.output

        # Trừ tiền
        self.balance -= amount
        self.last_dispensed_amount = amount
        self.transition_to(self.STATE_PROCESSING, f"REQ_{amount//1000}K", f"Xử lý rút {amount:,} VND")
        self.transition_to(self.STATE_DISPENSING, "DISPENSE_READY", f"Nhả tiền {amount:,} VND")
        return True, self.output

    def take_cash(self) -> Tuple[bool, Dict[str, Any]]:
        """Người dùng đã lấy tiền mặt từ khe."""
        if self.current_state != self.STATE_DISPENSING:
            return False, self.output
        self.transition_to(self.STATE_EJECTING_CARD, "CASH_TAKEN", "Đã lấy tiền -> Trả lại thẻ")
        return True, self.output

    def take_card(self) -> Tuple[bool, Dict[str, Any]]:
        """Người dùng nhận lại thẻ -> ATM quay về IDLE."""
        if self.current_state not in (self.STATE_EJECTING_CARD, self.STATE_LOCKED, self.STATE_ERROR):
            return False, self.output
        self.entered_pin = ""
        self.transition_to(self.STATE_IDLE, "CARD_TAKEN", "Thẻ đã được rút ra -> Chờ phiên mới")
        return True, self.output

    def cancel(self) -> Tuple[bool, Dict[str, Any]]:
        """Người dùng nhấn phím HỦY (Cancel)."""
        if self.current_state in (self.STATE_CARD_INSERTED, self.STATE_MAIN_MENU, self.STATE_WITHDRAW_MENU, self.STATE_ERROR):
            self.entered_pin = ""
            self.transition_to(self.STATE_EJECTING_CARD, "CANCEL_PRESSED", "Người dùng hủy bỏ thao tác")
            return True, self.output
        return False, self.output

    def reset_machine(self):
        """Khởi động lại toàn bộ máy."""
        self.current_state = self.STATE_IDLE
        self.balance = self.INITIAL_BALANCE
        self.entered_pin = ""
        self.failed_pin_attempts = 0
        self.last_dispensed_amount = 0
        self.error_message = ""
        self.history_log = []
        self._record_transition("RESET", self.STATE_IDLE, "Reset máy ATM")
