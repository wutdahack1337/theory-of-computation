import itertools


def loai_bo_trung_dict(d):
    res = {}
    for k, v in d.items():
        if v not in res.values():
            res[k] = v
    return res


def bai1(s1, s2):
    return s2[:2] + s1[2:] + " " + s1[:2] + s2[2:]


def bai2(s):
    return s[1::2]


def bai3(s):
    words = s.split()
    return {w: words.count(w) for w in words}


def bai4(s):
    res = ""
    for c in s:
        if "a" <= c <= "z":
            res += chr((ord(c) - ord("a") - 3) % 26 + ord("a"))
        elif "A" <= c <= "Z":
            res += chr((ord(c) - ord("A") - 3) % 26 + ord("A"))
        else:
            res += c
    return res


def bai5(s, S):
    return set(str(s)).issubset(set(str(x) for x in S))


def bai6(s):
    return s.split()


def bai7(s):
    for c in s:
        if s.count(c) == 1:
            return c
    return "None"


def bai8(s):
    return s.replace(" ", "")


def bai9(s):
    seen = set()
    for w in s.split():
        if w in seen:
            return w
        seen.add(w)
    return None


def bai10(s):
    return max(len(chunk) for chunk in s.split("1"))


def bai_nang_cao_1(A, B, max_len=6):
    n = len(A)
    for length in range(1, max_len + 1):
        for seq in itertools.product(range(n), repeat=length):
            sA = "".join(str(A[i]) for i in seq)
            sB = "".join(str(B[i]) for i in seq)
            if sA == sB:
                return "Có"
    return "Không"


def bai_nang_cao_2(gene):
    if len(gene) < 9 or len(gene) % 3 != 0:
        return "không hợp lệ"

    codons = [gene[i : i + 3] for i in range(0, len(gene), 3)]

    if codons[0] != "ATG" or codons[-1] not in ("TAA", "TAG", "TGA"):
        return "không hợp lệ"

    for c in codons:
        if not set(c).issubset({"A", "C", "G", "T"}):
            return "không hợp lệ"
        if len(set(c)) != 3 and c != "TAA":
            return "không hợp lệ"

    return "hợp lệ"


print(loai_bo_trung_dict({"a": 1, "b": 2, "c": 1, "d": 3}))

print(bai1("abc", "efg"))
print(bai2("python"))
print(bai3("no pain no gain"))
print(bai4("def"))
print(bai5("0011", {0, 1, 2}))
print(bai5("123", {0, 1, 2}))
print(bai6("This is a list"))
print(bai7("abcdef"))
print(bai7("abcabcdef"))
print(bai7("aabbcc"))
print(bai8("a b c"))
print(bai9("ab ca bc ca ab bc"))
print(bai9("ab ca bc ab"))
print(bai10("1110001110000"))

print(bai_nang_cao_1(("110", "0011", "0110"), ("110110", "00", "110")))
print(bai_nang_cao_1(("0011", "11", "1101"), ("101", "011", "110")))
print(bai_nang_cao_1(("100", "0", "1"), ("1", "100", "0")))

print(bai_nang_cao_2("ATGCCCTAG"))
print(bai_nang_cao_2("ATGCGTTGA"))
