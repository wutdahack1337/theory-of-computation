# Bài tập nhóm Lý thuyết tính toán — Ứng dụng FA trong thực tiễn

Nhóm sinh viên thực hiện:
- **Trần Quang Minh (B2304069)**: FA Engine, Máy ATM, Pattern Matching, Báo cáo LaTeX.
- **Hân**: Đèn giao thông, Máy bán hàng tự động, Slide báo cáo.

---

## 1. Yêu cầu môi trường

- **Python 3.8+**
- Đã tích hợp sẵn thư viện đồ họa **Tkinter** (mặc định đi kèm Python, không cần `pip install` bất kỳ thư viện ngoài nào).

---

## 2. Cách chạy ứng dụng

### Cách 1: Chạy từ thư mục gốc của repo
```bash
python project/src/main.py
```

### Cách 2: Chạy từ trong thư mục `project/`
```bash
cd project
python src/main.py
```

---

## 3. Cách chạy kiểm thử (Unit Test)

Chạy bộ test tự động kiểm tra logic FA Engine, ATM Moore Machine và Pattern Search:
```bash
python -m unittest project/tests/test_minh_modules.py
```

---

## 4. Cấu trúc 8 màn hình trong app

- **Màn 1 (Minh)**: Trang chủ & Giới thiệu tổng quan FA (DFA, NFA, Moore Machine).
- **Màn 2 (Hân)**: Đèn giao thông — Mô phỏng ngã tư và đồ thị DFA.
- **Màn 3 (Hân)**: Đèn giao thông — Chế độ Step và bảng Transition Log.
- **Màn 4 (Minh)**: Máy ATM — Giả lập ki-ốt vật lý, bàn phím PIN, rút tiền.
- **Màn 5 (Minh)**: Máy ATM — Sơ đồ Moore Machine và 4 Test Cases tự động (Khóa thẻ sai PIN 3 lần).
- **Màn 6 (Hân)**: Máy bán hàng tự động (Vending Machine) — Nạp coin, nhận hàng, trả tiền thừa.
- **Màn 7 (Minh)**: Pattern Search — Tìm kiếm chuỗi mẫu bằng NFA, highlight vị trí khớp.
- **Màn 8 (Minh)**: NFA → DFA — Trực quan hóa thuật toán Subset Construction.
