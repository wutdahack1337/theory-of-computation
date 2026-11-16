"""
Pattern Search - Xây dựng NFA từ chuỗi mẫu (Pattern) để tìm kiếm trong văn bản (Text),
và chuyển đổi NFA sang DFA bằng thuật toán Subset Construction.
Tái sử dụng nền tảng từ bài TH2 (Trần Quang Minh - B2304069).
"""

from typing import Any, Dict, FrozenSet, List, Optional, Set, Tuple
from .fa_engine import DFA, NFA, subset_construction_with_steps


class PatternSearcher:
    """Bộ tìm kiếm chuỗi mẫu trong văn bản sử dụng NFA và chuyển đổi sang DFA."""

    def __init__(self, pattern: str = "ATG"):
        self.pattern = pattern
        self.nfa: Optional[NFA] = None
        self.dfa: Optional[DFA] = None
        self.dfa_mapping: Dict[FrozenSet[Any], str] = {}
        self.dfa_steps: List[Dict[str, Any]] = []
        if pattern:
            self.build_nfa(pattern)

    def build_nfa(self, pattern: str, extra_alphabet: Optional[Set[str]] = None) -> NFA:
        """Xây dựng NFA từ pattern P = p_0 p_1 ... p_{m-1}.
        
        Q = {q0, q1, ..., qm}
        start = q0
        accept = {qm}
        delta(q0, c) = {q0} với mọi c thuộc Alphabet (cho phép match bắt đầu ở bất kỳ vị trí nào)
        delta(qi, p_i) = {qi+1}
        """
        self.pattern = pattern
        m = len(pattern)
        states = {f"q{i}" for i in range(m + 1)}
        start_state = "q0"
        accept_states = {f"q{m}"}

        # Bảng chữ cái bao gồm các ký tự trong pattern và các ký tự thường gặp / thêm vào
        alphabet = set(pattern)
        if extra_alphabet:
            alphabet.update(extra_alphabet)
        # Thêm bảng chữ cái mặc định (chữ cái, chữ số, khoảng trắng cơ bản)
        alphabet.update(set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 _-.,!?:;"))

        transition_function: Dict[Tuple[str, str], Set[str]] = {}

        # Khởi tạo self-loop tại q0 với mọi ký tự trong alphabet
        for char in alphabet:
            transition_function[("q0", char)] = {"q0"}

        # Thêm bước chuyển cho từng ký tự của pattern: q_i --p_i--> q_{i+1}
        for i, char in enumerate(pattern):
            src = f"q{i}"
            dest = f"q{i+1}"
            if (src, char) in transition_function:
                transition_function[(src, char)].add(dest)
            else:
                transition_function[(src, char)] = {dest}

        self.nfa = NFA(
            states=states,
            alphabet=alphabet,
            transition_function=transition_function,
            start_state=start_state,
            accept_states=accept_states,
            name=f"NFA_Pattern_{pattern}",
        )
        return self.nfa

    def search_with_trace(self, text: str) -> Dict[str, Any]:
        """Duyệt văn bản từng ký tự một bằng NFA và ghi lại nhật ký (trace) từng bước."""
        if not self.nfa:
            self.build_nfa(self.pattern)

        # Đảm bảo alphabet của NFA chứa tất cả ký tự trong text
        text_chars = set(text)
        if not text_chars.issubset(self.nfa.alphabet):
            self.build_nfa(self.pattern, extra_alphabet=text_chars)

        self.nfa.reset()
        step_trace: List[Dict[str, Any]] = []
        matches: List[Tuple[int, int, str]] = []  # (start_idx, end_idx, matched_str)
        m = len(self.pattern)

        # Trạng thái ban đầu trước khi đọc ký tự đầu tiên
        curr_states = set(self.nfa.current_states)
        step_trace.append({
            "step": 0,
            "char": "ε (Bắt đầu)",
            "char_index": -1,
            "active_states": sorted(list(curr_states)),
            "is_match": False,
            "match_at": None,
        })

        for idx, char in enumerate(text):
            prev_states, _, next_states, is_acc = self.nfa.step(char)
            is_match = f"q{m}" in next_states
            match_span = None

            if is_match and m > 0:
                start_pos = idx - m + 1
                end_pos = idx + 1
                match_span = (start_pos, end_pos)
                matches.append((start_pos, end_pos, text[start_pos:end_pos]))

            step_trace.append({
                "step": idx + 1,
                "char": char,
                "char_index": idx,
                "active_states": sorted(list(next_states)),
                "is_match": is_match,
                "match_span": match_span,
            })

        return {
            "pattern": self.pattern,
            "text": text,
            "total_matches": len(matches),
            "matches": matches,
            "step_trace": step_trace,
        }

    def convert_to_dfa(self) -> Tuple[DFA, Dict[FrozenSet[Any], str], List[Dict[str, Any]]]:
        """Chuyển đổi NFA hiện tại sang DFA kèm các bước Subset Construction chi tiết."""
        if not self.nfa:
            self.build_nfa(self.pattern)

        # Giới hạn alphabet rút gọn khi chuyển đổi sang DFA (chỉ lấy các ký tự xuất hiện trong pattern)
        # để DFA có số trạng thái gọn gàng, trực quan và dễ vẽ trên biểu đồ
        condensed_alphabet = sorted(list(set(self.pattern)))
        condensed_tf = {}
        for (st, sym), dests in self.nfa.transition_function.items():
            if sym in condensed_alphabet:
                condensed_tf[(st, sym)] = dests

        condensed_nfa = NFA(
            states=self.nfa.states,
            alphabet=condensed_alphabet,
            transition_function=condensed_tf,
            start_state=self.nfa.start_state,
            accept_states=self.nfa.accept_states,
            name=f"NFA_Condensed_{self.pattern}",
        )

        dfa, mapping, steps = subset_construction_with_steps(condensed_nfa)
        self.dfa = dfa
        self.dfa_mapping = mapping
        self.dfa_steps = steps
        return dfa, mapping, steps

    def search_with_dfa(self, text: str) -> List[Tuple[int, int, str]]:
        """Tìm kiếm bằng DFA đã chuyển đổi để đối chiếu kết quả với NFA."""
        if not self.dfa:
            self.convert_to_dfa()

        self.dfa.reset()
        matches = []
        m = len(self.pattern)

        for idx, char in enumerate(text):
            if char in self.dfa.alphabet:
                self.dfa.step(char)
                if self.dfa.in_accept_state():
                    start_pos = idx - m + 1
                    matches.append((start_pos, idx + 1, text[start_pos:idx+1]))
            else:
                self.dfa.reset()

        return matches
