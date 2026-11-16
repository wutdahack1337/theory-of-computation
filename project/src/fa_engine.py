"""
FA Engine - Thư viện lõi cho Deterministic Finite Automaton (DFA) và 
Nondeterministic Finite Automaton (NFA), bao gồm thuật toán chuyển đổi NFA -> DFA (Subset Construction).
Được mở rộng và chuẩn hóa từ bài thực hành TH2 (Trần Quang Minh - B2304069).
"""

from collections import deque
from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple, Union


class DFA:
    """Deterministic Finite Automaton (DFA) mô hình hóa máy hữu hạn đơn định."""

    def __init__(
        self,
        states: Union[Set[Any], List[Any]],
        alphabet: Union[Set[str], List[str]],
        transition_function: Dict[Tuple[Any, str], Any],
        start_state: Any,
        accept_states: Union[Set[Any], List[Any], Any],
        name: str = "DFA",
    ):
        self.name = name
        self.states = set(states)
        self.alphabet = set(alphabet)
        self.transition_function = dict(transition_function)
        self.start_state = start_state
        self.accept_states = (
            set(accept_states)
            if isinstance(accept_states, (set, list, tuple))
            else {accept_states}
        )
        self.current_state = start_state
        self.transition_log: List[Dict[str, Any]] = []

    def reset(self) -> Any:
        """Đưa DFA về trạng thái khởi đầu và xóa log."""
        self.current_state = self.start_state
        self.transition_log = []
        return self.current_state

    def step(self, input_value: str) -> Tuple[Any, str, Any, bool]:
        """Thực hiện một bước chuyển trạng thái với ký tự đầu vào.
        
        Trả về: (trạng_thái_trước, ký_tự, trạng_thái_sau, là_accept_state_hay_không)
        """
        prev_state = self.current_state
        next_state = self.transition_function.get((prev_state, input_value), None)
        self.current_state = next_state
        is_acc = self.in_accept_state()

        log_entry = {
            "step": len(self.transition_log) + 1,
            "from_state": prev_state,
            "input": input_value,
            "to_state": next_state,
            "is_accepted": is_acc,
        }
        self.transition_log.append(log_entry)
        return prev_state, input_value, next_state, is_acc

    def in_accept_state(self) -> bool:
        """Kiểm tra trạng thái hiện tại có thuộc tập trạng thái kết thúc không."""
        return self.current_state in self.accept_states

    def run_with_input_list(self, input_list: Union[List[str], str]) -> Tuple[bool, List[Dict[str, Any]]]:
        """Chạy toàn bộ chuỗi đầu vào và trả về (kết_quả_chấp_nhận, transition_log)."""
        self.reset()
        for sym in input_list:
            self.step(str(sym))
        return self.in_accept_state(), list(self.transition_log)

    def get_table_dict(self) -> Dict[Any, Dict[str, Any]]:
        """Trả về bảng chuyển trạng thái dưới dạng ma trận lồng nhau."""
        table: Dict[Any, Dict[str, Any]] = {}
        for s in self.states:
            table[s] = {}
            for a in self.alphabet:
                table[s][a] = self.transition_function.get((s, a), None)
        return table


class NFA:
    """Nondeterministic Finite Automaton (NFA) mô hình hóa máy hữu hạn không đơn định."""

    def __init__(
        self,
        states: Union[Set[Any], List[Any]],
        alphabet: Union[Set[str], List[str]],
        transition_function: Dict[Tuple[Any, str], Union[Set[Any], List[Any], Any]],
        start_state: Any,
        accept_states: Union[Set[Any], List[Any], Any],
        name: str = "NFA",
    ):
        self.name = name
        self.states = set(states)
        self.alphabet = set(alphabet)
        
        # Chuẩn hóa transition function: giá trị luôn là set các state đích
        self.transition_function: Dict[Tuple[Any, str], Set[Any]] = {}
        for k, v in transition_function.items():
            if isinstance(v, (set, list, tuple)):
                self.transition_function[k] = set(v)
            elif v is not None:
                self.transition_function[k] = {v}
            else:
                self.transition_function[k] = set()

        self.start_state = start_state
        self.accept_states = (
            set(accept_states)
            if isinstance(accept_states, (set, list, tuple))
            else {accept_states}
        )
        
        self.current_states: Set[Any] = (
            {start_state}
            if not isinstance(start_state, (set, list, tuple))
            else set(start_state)
        )
        self.transition_log: List[Dict[str, Any]] = []

    def reset(self) -> Set[Any]:
        """Đưa NFA về tập trạng thái khởi đầu và xóa log."""
        self.current_states = (
            {self.start_state}
            if not isinstance(self.start_state, (set, list, tuple))
            else set(self.start_state)
        )
        self.transition_log = []
        return set(self.current_states)

    def step(self, input_value: str) -> Tuple[Set[Any], str, Set[Any], bool]:
        """Thực hiện một bước chuyển trạng thái trên tập current_states với ký tự đầu vào.
        
        Trả về: (tập_trước, ký_tự, tập_sau, có_chứa_accept_state_hay_không)
        """
        prev_states = set(self.current_states)
        next_states: Set[Any] = set()

        for st in prev_states:
            dests = self.transition_function.get((st, input_value), set())
            next_states.update(dests)

        self.current_states = next_states
        is_acc = self.in_accept_state()

        log_entry = {
            "step": len(self.transition_log) + 1,
            "from_states": sorted(list(prev_states), key=str),
            "input": input_value,
            "to_states": sorted(list(next_states), key=str),
            "is_accepted": is_acc,
        }
        self.transition_log.append(log_entry)
        return prev_states, input_value, next_states, is_acc

    def in_accept_state(self) -> bool:
        """Kiểm tra có ít nhất 1 state hiện tại thuộc tập accept states hay không."""
        return bool(self.current_states & self.accept_states)

    def run_with_input_list(self, input_list: Union[List[str], str]) -> Tuple[bool, List[Dict[str, Any]]]:
        """Chạy toàn bộ chuỗi đầu vào và trả về (kết_quả_chấp_nhận, transition_log)."""
        self.reset()
        for sym in input_list:
            self.step(str(sym))
        return self.in_accept_state(), list(self.transition_log)


def subset_construction_with_steps(nfa: NFA) -> Tuple[DFA, Dict[FrozenSet[Any], str], List[Dict[str, Any]]]:
    """Thuật toán Subset Construction chuyển đổi NFA sang DFA kèm lịch sử từng bước chi tiết.
    
    Trả về:
        (dfa, subset_to_name_map, step_records)
    """
    start_set = frozenset([nfa.start_state]) if not isinstance(nfa.start_state, (set, list, tuple)) else frozenset(nfa.start_state)
    unprocessed = deque([start_set])
    discovered_subsets: Set[FrozenSet[Any]] = {start_set}
    
    # Đặt tên các subset: D0, D1, D2,...
    naming_map: Dict[FrozenSet[Any], str] = {start_set: "D0"}
    counter = 1

    dfa_transitions: Dict[Tuple[str, str], str] = {}
    dfa_accept_states: Set[str] = set()
    step_records: List[Dict[str, Any]] = []

    alphabet_sorted = sorted(list(nfa.alphabet), key=str)

    while unprocessed:
        curr_subset = unprocessed.popleft()
        curr_name = naming_map[curr_subset]
        curr_list = sorted(list(curr_subset), key=str)

        # Kiểm tra xem có chứa accept state của NFA không
        is_acc = any(s in nfa.accept_states for s in curr_subset)
        if is_acc:
            dfa_accept_states.add(curr_name)

        for sym in alphabet_sorted:
            next_set: Set[Any] = set()
            for s in curr_subset:
                dests = nfa.transition_function.get((s, sym), set())
                next_set.update(dests)

            f_next = frozenset(next_set)
            is_new = False
            if f_next not in naming_map:
                naming_map[f_next] = f"D{counter}"
                counter += 1
                is_new = True
                discovered_subsets.add(f_next)
                unprocessed.append(f_next)

            dest_name = naming_map[f_next]
            dfa_transitions[(curr_name, sym)] = dest_name

            step_records.append({
                "source_name": curr_name,
                "source_subset": curr_list,
                "symbol": sym,
                "dest_name": dest_name,
                "dest_subset": sorted(list(f_next), key=str),
                "is_new": is_new,
                "is_dest_accept": any(s in nfa.accept_states for s in f_next),
            })

    all_dfa_states = set(naming_map.values())
    result_dfa = DFA(
        states=all_dfa_states,
        alphabet=set(nfa.alphabet),
        transition_function=dfa_transitions,
        start_state="D0",
        accept_states=dfa_accept_states,
        name=f"DFA_from_{nfa.name}",
    )

    return result_dfa, naming_map, step_records


def khoi_tao_dfa_mau() -> DFA:
    """Khởi tạo DFA mẫu từ bài TH2 (Nhận chuỗi nhị phân có số lẻ số 1 và chẵn số 0...)."""
    states = {0, 1, 2}
    alphabet = {"0", "1"}
    start_state = 0
    accept_states = {0}

    tf = {
        (0, "0"): 0,
        (0, "1"): 1,
        (1, "0"): 2,
        (1, "1"): 0,
        (2, "0"): 1,
        (2, "1"): 2,
    }
    return DFA(states, alphabet, tf, start_state, accept_states, name="DFA_Mau_TH2")


def khoi_tao_nfa_mau() -> NFA:
    """Khởi tạo NFA mẫu từ bài TH2 (Chấp nhận chuỗi kết thúc bởi 11 hoặc 00)."""
    states = {"q0", "q1", "q2", "q3", "q4"}
    alphabet = {"0", "1"}
    start_state = "q0"
    accept_states = {"q2", "q4"}

    tf = {
        ("q0", "0"): {"q0", "q3"},
        ("q0", "1"): {"q0", "q1"},
        ("q1", "1"): {"q2"},
        ("q2", "0"): {"q2"},
        ("q2", "1"): {"q2"},
        ("q3", "0"): {"q4"},
        ("q4", "0"): {"q4"},
        ("q4", "1"): {"q4"},
    }
    return NFA(states, alphabet, tf, start_state, accept_states, name="NFA_Mau_TH2")
