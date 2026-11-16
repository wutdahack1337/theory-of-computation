import os
import re
import sys
from collections import deque
from itertools import islice


def doc_file_co_ban(filepath="text.txt"):
    if not os.path.exists(filepath):
        return [], [], []

    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    lines_skip_first = lines[1:]

    char_lines = []
    for line in lines:
        char_lines.append(list(islice(line, len(line))))

    return lines, lines_skip_first, char_lines


class DFA(object):
    def __init__(
        self,
        states,
        alphabet,
        transition_function,
        start_state,
        accept_states,
        current_state=None,
    ):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = (
            set(accept_states)
            if isinstance(accept_states, (set, list, tuple))
            else {accept_states}
        )
        self.current_state = start_state

    def transition_to_state_with_input(self, input_value):
        if (self.current_state, input_value) not in self.transition_function.keys():
            self.current_state = None
            return
        self.current_state = self.transition_function[(self.current_state, input_value)]

    def in_accept_state(self):
        return self.current_state in self.accept_states

    def go_to_initial_state(self):
        self.current_state = self.start_state
        return self.current_state

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
        return self.in_accept_state()


def khoi_tao_dfa_mau():
    states = {0, 1, 2}
    alphabet = {"0", "1"}
    start_state = 0
    accept_states = {0}

    tf = dict()
    tf[(0, "0")] = 0
    tf[(0, "1")] = 1
    tf[(1, "0")] = 2
    tf[(1, "1")] = 0
    tf[(2, "0")] = 1
    tf[(2, "1")] = 2

    return DFA(states, alphabet, tf, start_state, accept_states)


def parse_state(val):
    val = val.strip()
    return int(val) if val.isdigit() else val


def doc_dfa_tu_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    states = {
        parse_state(s) for s in re.split(r"[, \t]+", raw_lines[0].strip()) if s
    }
    alphabet = {s.strip("'\" ") for s in re.split(r"[, \t]+", raw_lines[1].strip()) if s}
    start_state = parse_state(raw_lines[2].strip())
    accept_states = {
        parse_state(s) for s in re.split(r"[, \t]+", raw_lines[3].strip()) if s
    }

    tf = dict()
    for line in raw_lines[4:]:
        if "->" in line:
            left, right = line.split("->")
            parts = re.split(r"[, \t]+", left.strip())
            src = parse_state(parts[0])
            inp = parts[1].strip("'\" ")
            dest = parse_state(right.strip())
        else:
            parts = re.split(r"[, \t]+", line.strip())
            src = parse_state(parts[0])
            inp = parts[1].strip("'\" ")
            dest = parse_state(parts[2])
        tf[(src, inp)] = dest

    return DFA(states, alphabet, tf, start_state, accept_states)


def nhap_dfa_tu_ban_phim():
    st_line = input()
    states = {parse_state(s) for s in re.split(r"[, \t]+", st_line.strip()) if s}

    alpha_line = input()
    alphabet = {s.strip("'\" ") for s in re.split(r"[, \t]+", alpha_line.strip()) if s}

    start_line = input()
    start_state = parse_state(start_line.strip())

    acc_line = input()
    accept_states = {
        parse_state(s) for s in re.split(r"[, \t]+", acc_line.strip()) if s
    }

    tf = dict()
    while True:
        line = input().strip()
        if not line or line.lower() == "done":
            break
        if "->" in line:
            left, right = line.split("->")
            parts = re.split(r"[, \t]+", left.strip())
            src = parse_state(parts[0])
            inp = parts[1].strip("'\" ")
            dest = parse_state(right.strip())
        else:
            parts = re.split(r"[, \t]+", line)
            src = parse_state(parts[0])
            inp = parts[1].strip("'\" ")
            dest = parse_state(parts[2])
        tf[(src, inp)] = dest

    return DFA(states, alphabet, tf, start_state, accept_states)


def bai_tap_1(dfa_source, input_str):
    if isinstance(dfa_source, str):
        dfa = doc_dfa_tu_file(dfa_source)
    else:
        dfa = dfa_source

    return dfa.run_with_input_list(list(input_str))


class NFA(object):
    def __init__(
        self,
        states,
        alphabet,
        transition_function,
        start_state,
        accept_states,
        current_states=None,
    ):
        self.states = states
        self.alphabet = alphabet
        self.transition_function = transition_function
        self.start_state = start_state
        self.accept_states = (
            set(accept_states)
            if isinstance(accept_states, (set, list, tuple))
            else {accept_states}
        )
        self.current_states = (
            {start_state}
            if not isinstance(start_state, (set, list, tuple))
            else set(start_state)
        )

    def go_to_initial_state(self):
        self.current_states = (
            {self.start_state}
            if not isinstance(self.start_state, (set, list, tuple))
            else set(self.start_state)
        )
        return self.current_states

    def transition_to_state_with_input(self, input_value):
        next_states = set()
        for state in self.current_states:
            dest = self.transition_function.get((state, input_value))
            if dest is not None:
                if isinstance(dest, (set, list, tuple)):
                    next_states.update(dest)
                else:
                    next_states.add(dest)
        self.current_states = next_states
        return self.current_states

    def in_accept_state(self):
        return bool(self.current_states & self.accept_states)

    def run_with_input_list(self, input_list):
        self.go_to_initial_state()
        for inp in input_list:
            self.transition_to_state_with_input(inp)
        return self.in_accept_state()


def khoi_tao_nfa_mau():
    states = {"q0", "q1", "q2", "q3", "q4"}
    alphabet = {"0", "1"}
    start_state = "q0"
    accept_states = {"q2", "q4"}

    tf = dict()
    tf[("q0", "0")] = {"q0", "q3"}
    tf[("q0", "1")] = {"q0", "q1"}
    tf[("q1", "1")] = {"q2"}
    tf[("q2", "0")] = {"q2"}
    tf[("q2", "1")] = {"q2"}
    tf[("q3", "0")] = {"q4"}
    tf[("q4", "0")] = {"q4"}
    tf[("q4", "1")] = {"q4"}

    return NFA(states, alphabet, tf, start_state, accept_states)


def doc_nfa_tu_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw_lines = [
            line.strip()
            for line in f
            if line.strip() and not line.strip().startswith("#")
        ]

    states = {
        parse_state(s) for s in re.split(r"[, \t]+", raw_lines[0].strip()) if s
    }
    alphabet = {s.strip("'\" ") for s in re.split(r"[, \t]+", raw_lines[1].strip()) if s}
    start_state = parse_state(raw_lines[2].strip())
    accept_states = {
        parse_state(s) for s in re.split(r"[, \t]+", raw_lines[3].strip()) if s
    }

    tf = dict()
    for line in raw_lines[4:]:
        if "->" in line:
            left, right = line.split("->")
            parts = re.split(r"[, \t]+", left.strip())
            src = parse_state(parts[0])
            inp = parts[1].strip("'\" ")
            dest_states = {
                parse_state(s) for s in re.split(r"[, \t]+", right.strip()) if s
            }
        else:
            parts = re.split(r"[, \t]+", line.strip())
            src = parse_state(parts[0])
            inp = parts[1].strip("'\" ")
            dest_states = {parse_state(s) for s in parts[2:] if s}

        if (src, inp) in tf:
            tf[(src, inp)].update(dest_states)
        else:
            tf[(src, inp)] = dest_states

    return NFA(states, alphabet, tf, start_state, accept_states)


def bai_tap_2(nfa_source, input_str):
    if isinstance(nfa_source, str):
        nfa = doc_nfa_tu_file(nfa_source)
    else:
        nfa = nfa_source

    return nfa.run_with_input_list(list(input_str))


def bai_nang_cao_nfa_sang_dfa(nfa):
    start_set = frozenset([nfa.start_state])
    unprocessed = deque([start_set])
    dfa_states = {start_set}
    dfa_tf = {}
    dfa_accept = set()

    while unprocessed:
        curr = unprocessed.popleft()
        if any(s in nfa.accept_states for s in curr):
            dfa_accept.add(curr)

        for sym in sorted(nfa.alphabet):
            next_set = set()
            for s in curr:
                dest = nfa.transition_function.get((s, sym), set())
                if isinstance(dest, (set, list, tuple)):
                    next_set.update(dest)
                elif dest is not None:
                    next_set.add(dest)
            f_next = frozenset(next_set)
            dfa_tf[(curr, sym)] = f_next
            if f_next not in dfa_states:
                dfa_states.add(f_next)
                unprocessed.append(f_next)

    mapping = {st: f"D{i}" for i, st in enumerate(dfa_states)}
    named_states = set(mapping.values())
    named_start = mapping[start_set]
    named_accept = {mapping[st] for st in dfa_accept}
    named_tf = {
        (mapping[st], sym): mapping[dest] for (st, sym), dest in dfa_tf.items()
    }

    return DFA(named_states, nfa.alphabet, named_tf, named_start, named_accept)


def chay_tuong_tac():
    choice = input().strip()
    if choice == "1":
        dfa = nhap_dfa_tu_ban_phim()
        s = input().strip()
        print(dfa.run_with_input_list(list(s)))
    elif choice == "2":
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dfa_input.txt")
        dfa = doc_dfa_tu_file(filepath)
        s = input().strip()
        print(dfa.run_with_input_list(list(s)))
    elif choice == "3":
        nfa = khoi_tao_nfa_mau()
        s = input().strip()
        print(nfa.run_with_input_list(list(s)))


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_TEXT = os.path.join(BASE_DIR, "text.txt")
FILE_DFA = os.path.join(BASE_DIR, "dfa_input.txt")
FILE_NFA = os.path.join(BASE_DIR, "nfa_input.txt")

lines, skip_first, char_matrix = doc_file_co_ban(FILE_TEXT)
print(lines)
print(skip_first)
print(char_matrix)

dfa_guide = khoi_tao_dfa_mau()
print(dfa_guide.go_to_initial_state())
print(dfa_guide.run_with_input_list(list("1011101")))
print(dfa_guide.run_with_input_list(list("10111011")))

print(bai_tap_1(FILE_DFA, "1011101"))
print(bai_tap_1(FILE_DFA, "10111011"))

nfa_guide = khoi_tao_nfa_mau()
print(bai_tap_2(nfa_guide, "1011101"))
print(bai_tap_2(nfa_guide, "10111011"))
print(bai_tap_2(nfa_guide, "00"))
print(bai_tap_2(nfa_guide, "11"))
print(bai_tap_2(nfa_guide, "1001"))
print(bai_tap_2(nfa_guide, "010101"))
print(bai_tap_2(nfa_guide, "101010"))

print(bai_tap_2(FILE_NFA, "1001"))
print(bai_tap_2(FILE_NFA, "01010"))

dfa_from_nfa = bai_nang_cao_nfa_sang_dfa(nfa_guide)
print(dfa_from_nfa.run_with_input_list(list("1011101")))
print(dfa_from_nfa.run_with_input_list(list("010101")))
