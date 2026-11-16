"""
Controller - Chứa bộ điều khiển Finite Automata cho:
1. TrafficLightController: Bộ điều khiển đèn giao thông dựa trên DFA.
2. VendingMachineController: Bộ điều khiển máy bán hàng tự động dựa trên DFA.
"""

from typing import Any, Dict, List, Optional, Tuple
from .fa_engine import DFA


class TrafficLightController:
    """Điều khiển hệ thống đèn giao thông 4 pha tại ngã tư bằng DFA.
    
    Các trạng thái:
    - NS_GREEN: Bắc - Nam đèn Xanh (15s), Đông - Tây đèn Đỏ
    - NS_YELLOW: Bắc - Nam đèn Vàng (3s), Đông - Tây đèn Đỏ
    - EW_GREEN: Đông - Tây đèn Xanh (15s), Bắc - Nam đèn Đỏ
    - EW_YELLOW: Đông - Tây đèn Vàng (3s), Bắc - Nam đèn Đỏ
    - EMERGENCY_ALL_RED: Chế độ khẩn cấp (Ưu tiên xe cứu thương / sự cố)
    
    Alphabet đầu vào:
    - 'TICK': 1 giây trôi qua
    - 'TIMEOUT': Hết thời gian đếm lùi của pha hiện tại
    - 'EMERGENCY_ON': Kích hoạt còi ưu tiên cứu thương
    - 'EMERGENCY_OFF': Tắt chế độ ưu tiên, phục hồi trạng thái
    - 'MANUAL_NEXT': Chuyển pha thủ công
    - 'RESET': Khởi động lại hệ thống
    """

    DURATIONS = {
        "NS_GREEN": 15,
        "NS_YELLOW": 3,
        "EW_GREEN": 15,
        "EW_YELLOW": 3,
        "EMERGENCY_ALL_RED": 0,
    }

    def __init__(self):
        self.states = {
            "NS_GREEN",
            "NS_YELLOW",
            "EW_GREEN",
            "EW_YELLOW",
            "EMERGENCY_ALL_RED",
        }
        self.alphabet = {
            "TIMEOUT",
            "EMERGENCY_ON",
            "EMERGENCY_OFF",
            "MANUAL_NEXT",
            "RESET",
        }
        self.start_state = "NS_GREEN"
        self.accept_states = {"NS_GREEN", "EW_GREEN"}

        self.transition_function = {
            ("NS_GREEN", "TIMEOUT"): "NS_YELLOW",
            ("NS_GREEN", "MANUAL_NEXT"): "NS_YELLOW",
            ("NS_YELLOW", "TIMEOUT"): "EW_GREEN",
            ("NS_YELLOW", "MANUAL_NEXT"): "EW_GREEN",
            ("EW_GREEN", "TIMEOUT"): "EW_YELLOW",
            ("EW_GREEN", "MANUAL_NEXT"): "EW_YELLOW",
            ("EW_YELLOW", "TIMEOUT"): "NS_GREEN",
            ("EW_YELLOW", "MANUAL_NEXT"): "NS_GREEN",
            # Sự kiện khẩn cấp
            ("NS_GREEN", "EMERGENCY_ON"): "EMERGENCY_ALL_RED",
            ("NS_YELLOW", "EMERGENCY_ON"): "EMERGENCY_ALL_RED",
            ("EW_GREEN", "EMERGENCY_ON"): "EMERGENCY_ALL_RED",
            ("EW_YELLOW", "EMERGENCY_ON"): "EMERGENCY_ALL_RED",
            ("EMERGENCY_ALL_RED", "EMERGENCY_OFF"): "NS_GREEN",
            ("EMERGENCY_ALL_RED", "TIMEOUT"): "EMERGENCY_ALL_RED",
            ("EMERGENCY_ALL_RED", "MANUAL_NEXT"): "NS_GREEN",
        }

        self.dfa = DFA(
            states=self.states,
            alphabet=self.alphabet,
            transition_function=self.transition_function,
            start_state=self.start_state,
            accept_states=self.accept_states,
            name="TrafficLight_DFA",
        )

        self.current_state = self.start_state
        self.time_left = self.DURATIONS[self.current_state]
        self.is_emergency = False
        self.log: List[Dict[str, Any]] = []
        self._record_log("INIT", self.current_state, "Khởi động hệ thống đèn giao thông")

    def _record_log(self, input_event: str, next_state: str, note: str = ""):
        self.log.append({
            "step": len(self.log) + 1,
            "prev_state": getattr(self, "current_state", "NONE"),
            "input_event": input_event,
            "next_state": next_state,
            "time_left": self.time_left,
            "note": note,
        })

    def tick_second(self) -> Tuple[bool, str]:
        """Đếm lùi 1 giây. Nếu hết giờ, tự động kích hoạt TIMEOUT transition.
        
        Trả về: (có_chuyển_pha_không, trạng_thái_mới)
        """
        if self.is_emergency:
            return False, self.current_state

        self.time_left -= 1
        if self.time_left <= 0:
            return self.trigger_input("TIMEOUT")
        return False, self.current_state

    def trigger_input(self, symbol: str) -> Tuple[bool, str]:
        """Kích hoạt tín hiệu đầu vào cho DFA."""
        prev = self.current_state
        dest = self.transition_function.get((prev, symbol), None)
        if dest is not None and dest != prev:
            self.current_state = dest
            self.dfa.current_state = dest
            self.time_left = self.DURATIONS.get(dest, 10)
            self._record_log(symbol, dest, f"Chuyển trạng thái từ {prev} sang {dest}")
            return True, dest
        elif symbol == "RESET":
            self.reset()
            return True, self.current_state
        return False, self.current_state

    def toggle_emergency(self) -> Tuple[bool, str]:
        """Bật/tắt chế độ ưu tiên xe cứu thương."""
        if not self.is_emergency:
            self.is_emergency = True
            return self.trigger_input("EMERGENCY_ON")
        else:
            self.is_emergency = False
            return self.trigger_input("EMERGENCY_OFF")

    def manual_step(self) -> Tuple[bool, str]:
        """Chuyển pha ngay lập tức (Manual Step)."""
        return self.trigger_input("MANUAL_NEXT")

    def reset(self):
        """Khởi động lại toàn bộ chu kỳ."""
        self.current_state = self.start_state
        self.dfa.reset()
        self.time_left = self.DURATIONS[self.current_state]
        self.is_emergency = False
        self._record_log("RESET", self.current_state, "Reset về trạng thái ban đầu")

    def get_light_signals(self) -> Dict[str, Dict[str, bool]]:
        """Trả về tín hiệu đèn (True/False) cho cả 2 hướng: Bắc-Nam (NS) và Đông-Tây (EW)."""
        st = self.current_state
        if st == "NS_GREEN":
            return {
                "NS": {"red": False, "yellow": False, "green": True},
                "EW": {"red": True, "yellow": False, "green": False},
            }
        elif st == "NS_YELLOW":
            return {
                "NS": {"red": False, "yellow": True, "green": False},
                "EW": {"red": True, "yellow": False, "green": False},
            }
        elif st == "EW_GREEN":
            return {
                "NS": {"red": True, "yellow": False, "green": False},
                "EW": {"red": False, "yellow": False, "green": True},
            }
        elif st == "EW_YELLOW":
            return {
                "NS": {"red": True, "yellow": False, "green": False},
                "EW": {"red": False, "yellow": True, "green": False},
            }
        else:  # EMERGENCY_ALL_RED
            return {
                "NS": {"red": True, "yellow": False, "green": False},
                "EW": {"red": True, "yellow": False, "green": False},
            }


class VendingMachineController:
    """Điều khiển Máy bán hàng tự động bằng DFA.
    
    Sản phẩm:
    - AQUAFINA: 5,000đ (5k)
    - COCA_COLA: 10,000đ (10k)
    - RED_BULL: 15,000đ (15k)
    - COFFEE: 20,000đ (20k)
    
    Trạng thái:
    - Tổng tiền hiện tại: 0k, 5k, 10k, 15k, 20k, 25k, 30k, 35k, 40k, 45k, 50k
    
    Đầu vào (Alphabet):
    - 'COIN_5K', 'COIN_10K', 'COIN_20K'
    - 'BUY_AQUAFINA', 'BUY_COCA', 'BUY_REDBULL', 'BUY_COFFEE'
    - 'REFUND'
    """

    PRODUCTS = {
        "AQUAFINA": {"name": "Nước suối Aquafina", "price": 5000, "icon": "💧"},
        "COCA": {"name": "Coca-Cola Sleek", "price": 10000, "icon": "🥤"},
        "REDBULL": {"name": "Tăng lực Red Bull", "price": 15000, "icon": "⚡"},
        "COFFEE": {"name": "Cà phê Highlands", "price": 20000, "icon": "☕"},
    }

    MAX_BALANCE = 50000

    def __init__(self):
        self.balance = 0
        self.states = [f"{b // 1000}k" for b in range(0, self.MAX_BALANCE + 5000, 5000)]
        self.alphabet = {
            "COIN_5K", "COIN_10K", "COIN_20K",
            "BUY_AQUAFINA", "BUY_COCA", "BUY_REDBULL", "BUY_COFFEE",
            "REFUND"
        }
        
        # Xây dựng DFA transition function
        self.transition_function: Dict[Tuple[str, str], str] = {}
        for b in range(0, self.MAX_BALANCE + 5000, 5000):
            st = f"{b // 1000}k"
            # Nạp tiền
            self.transition_function[(st, "COIN_5K")] = f"{min(b + 5000, self.MAX_BALANCE) // 1000}k"
            self.transition_function[(st, "COIN_10K")] = f"{min(b + 10000, self.MAX_BALANCE) // 1000}k"
            self.transition_function[(st, "COIN_20K")] = f"{min(b + 20000, self.MAX_BALANCE) // 1000}k"
            self.transition_function[(st, "REFUND")] = "0k"

            # Mua hàng
            for p_code, p_info in self.PRODUCTS.items():
                inp = f"BUY_{p_code}"
                if b >= p_info["price"]:
                    rem = b - p_info["price"]
                    self.transition_function[(st, inp)] = f"{rem // 1000}k"
                else:
                    self.transition_function[(st, inp)] = st

        self.accept_states = {f"{b // 1000}k" for b in range(5000, self.MAX_BALANCE + 5000, 5000)}
        self.dfa = DFA(
            states=set(self.states),
            alphabet=self.alphabet,
            transition_function=self.transition_function,
            start_state="0k",
            accept_states=self.accept_states,
            name="VendingMachine_DFA",
        )

        self.dispensed_items: List[str] = []
        self.change_returned: int = 0
        self.last_message: str = "Chào mừng quý khách! Vui lòng nạp tiền."
        self.log: List[Dict[str, Any]] = []
        self._record_log("INIT", "0k", "Khởi động máy bán hàng")

    def _record_log(self, input_event: str, next_state: str, action: str):
        self.log.append({
            "step": len(self.log) + 1,
            "prev_balance": self.balance,
            "input_event": input_event,
            "next_balance": int(next_state.replace("k", "")) * 1000,
            "state_label": next_state,
            "action": action,
        })

    @property
    def current_state(self) -> str:
        return f"{self.balance // 1000}k"

    def insert_money(self, amount: int) -> Tuple[bool, str]:
        """Nạp tiền vào máy (5000, 10000, 20000)."""
        coin_event_map = {5000: "COIN_5K", 10000: "COIN_10K", 20000: "COIN_20K"}
        event = coin_event_map.get(amount)
        if not event:
            return False, "Mệnh giá không hợp lệ (chỉ nhận 5k, 10k, 20k)"

        prev_st = self.current_state
        next_st = self.transition_function.get((prev_st, event), prev_st)
        self.balance = int(next_st.replace("k", "")) * 1000
        self.dfa.current_state = next_st
        self.last_message = f"Đã nhận +{amount:,} VND. Số dư: {self.balance:,} VND."
        self._record_log(event, next_st, self.last_message)
        return True, self.last_message

    def select_product(self, product_code: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Chọn mua một sản phẩm."""
        if product_code not in self.PRODUCTS:
            return False, "Sản phẩm không tồn tại", None

        product = self.PRODUCTS[product_code]
        event = f"BUY_{product_code}"
        price = product["price"]

        if self.balance < price:
            msg = f"Số dư không đủ! {product['name']} giá {price:,} VND (cần thêm {price - self.balance:,} VND)"
            self.last_message = msg
            self._record_log(event, self.current_state, msg)
            return False, msg, None

        prev_st = self.current_state
        next_st = self.transition_function.get((prev_st, event), prev_st)
        self.balance = int(next_st.replace("k", "")) * 1000
        self.dfa.current_state = next_st
        self.dispensed_items.append(product["name"])
        msg = f"Đã nhả {product['name']}! Số dư còn lại: {self.balance:,} VND."
        self.last_message = msg
        self._record_log(event, next_st, msg)
        return True, msg, product

    def refund(self) -> Tuple[int, Dict[int, int], str]:
        """Hủy giao dịch và trả lại tiền thừa."""
        rem = self.balance
        if rem == 0:
            msg = "Không có tiền thừa để trả lại."
            self.last_message = msg
            return 0, {}, msg

        # Phân tích mệnh giá trả lại
        change_breakdown: Dict[int, int] = {}
        for coin in [20000, 10000, 5000]:
            count = rem // coin
            if count > 0:
                change_breakdown[coin] = count
                rem %= coin

        returned_amount = self.balance
        self.balance = 0
        self.dfa.current_state = "0k"
        self.change_returned += returned_amount
        msg = f"Đã trả lại {returned_amount:,} VND tiền thừa."
        self.last_message = msg
        self._record_log("REFUND", "0k", msg)
        return returned_amount, change_breakdown, msg
