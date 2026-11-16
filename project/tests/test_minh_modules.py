"""
Unit tests kiểm thử toàn bộ phần việc của Minh:
1. fa_engine.py (DFA, NFA, Subset Construction)
2. atm.py (Moore Machine, 3 lần sai PIN -> Khóa thẻ, Rút tiền)
3. pattern_search.py (NFA matching, Subset Construction NFA->DFA)
"""

import unittest
from project.src.fa_engine import DFA, NFA, subset_construction_with_steps
from project.src.atm import ATMMooreMachine
from project.src.pattern_search import PatternSearcher


class TestMinhModules(unittest.TestCase):
    def test_dfa_engine(self):
        # DFA kiểm tra tính chẵn lẻ của chuỗi nhị phân (chấp nhận nếu lẻ số 1)
        dfa = DFA(
            states={"q0", "q1"},
            alphabet={"0", "1"},
            transition_function={
                ("q0", "0"): "q0",
                ("q0", "1"): "q1",
                ("q1", "0"): "q1",
                ("q1", "1"): "q0",
            },
            start_state="q0",
            accept_states={"q1"},
        )
        acc, log = dfa.run_with_input_list("10101")
        self.assertTrue(acc)
        self.assertEqual(len(log), 5)

        acc2, _ = dfa.run_with_input_list("1100")
        self.assertFalse(acc2)

    def test_atm_moore_machine_success_flow(self):
        atm = ATMMooreMachine()
        self.assertEqual(atm.current_state, atm.STATE_IDLE)

        # 1. Đưa thẻ
        atm.insert_card()
        self.assertEqual(atm.current_state, atm.STATE_CARD_INSERTED)

        # 2. Nhập PIN đúng 1234
        atm.entered_pin = "1234"
        atm.submit_pin()
        self.assertEqual(atm.current_state, atm.STATE_MAIN_MENU)

        # 3. Chọn rút tiền
        atm.select_withdraw()
        self.assertEqual(atm.current_state, atm.STATE_WITHDRAW_MENU)

        # 4. Rút 200,000 VND
        atm.execute_withdraw(200000)
        self.assertEqual(atm.current_state, atm.STATE_DISPENSING)
        self.assertEqual(atm.balance, 4800000)

        # 5. Lấy tiền & trả thẻ
        atm.take_cash()
        self.assertEqual(atm.current_state, atm.STATE_EJECTING_CARD)
        atm.take_card()
        self.assertEqual(atm.current_state, atm.STATE_IDLE)

    def test_atm_moore_machine_wrong_pin_3_times_locked(self):
        atm = ATMMooreMachine()
        atm.insert_card()

        # Nhập sai lần 1
        atm.entered_pin = "0000"
        atm.submit_pin()
        self.assertEqual(atm.current_state, atm.STATE_CARD_INSERTED)
        self.assertEqual(atm.failed_pin_attempts, 1)

        # Nhập sai lần 2
        atm.entered_pin = "1111"
        atm.submit_pin()
        self.assertEqual(atm.current_state, atm.STATE_CARD_INSERTED)
        self.assertEqual(atm.failed_pin_attempts, 2)

        # Nhập sai lần 3 -> Phải chuyển sang S_LOCKED
        atm.entered_pin = "2222"
        atm.submit_pin()
        self.assertEqual(atm.current_state, atm.STATE_LOCKED)
        self.assertEqual(atm.output["status_code"], "CARD_LOCKED_FATAL")

    def test_pattern_search_nfa_and_subset_construction(self):
        ps = PatternSearcher("ATG")
        text = "ATGCGATCGATGAACTGATG"
        res = ps.search_with_trace(text)
        self.assertEqual(res["total_matches"], 3)
        self.assertEqual(len(res["matches"]), 3)

        # Test Subset Construction chuyển NFA sang DFA
        dfa, mapping, steps = ps.convert_to_dfa()
        self.assertTrue(len(dfa.states) >= 4)
        self.assertTrue(len(steps) > 0)

        # Đối chiếu kết quả tìm kiếm giữa DFA và NFA
        dfa_matches = ps.search_with_dfa(text)
        self.assertEqual(len(dfa_matches), 3)


if __name__ == "__main__":
    unittest.main()
