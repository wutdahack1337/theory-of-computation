# Kế hoạch bài tập nhóm — Chủ đề 1: Ứng dụng FA trong thực tiễn

Nhóm 2 người, deadline ~2 tuần. Viết bằng LaTeX, demo bằng Python + Tkinter.

---

## Các ứng dụng sẽ làm (4 app → 8 màn hình)

### App 1 — Đèn giao thông (Traffic Light Controller)

Đèn giao thông là ví dụ kinh điển của DFA trong embedded systems. Mỗi trạng thái (đỏ/vàng/xanh) là một state, timer trigger là input alphabet.

Thực tế: hệ thống đèn đường ở Việt Nam, hầu hết PLC công nghiệp đều implement theo nguyên tắc này.

Demo:
- Màn 5: Vẽ đèn 3 bóng bằng canvas, animate chuyển state theo DFA. Có nút Play/Pause/Step.
- Trạng thái hiển thị rõ: đang ở state nào, input tiếp theo là gì.

### App 2 — Máy ATM

ATM là Moore machine điển hình. Các bước insert card → nhập PIN → chọn giao dịch → rút tiền → eject card đều là state transitions rõ ràng, dễ trace.

Thực tế: giao thức xử lý giao dịch của Visa/Mastercard implement trên nền state machine.

Demo:
- Màn 6: Giả lập giao diện ATM đơn giản. Người dùng thao tác từng bước, app hiện state hiện tại + transition vừa xảy ra.
- Có thể test case lỗi (sai PIN 3 lần → khóa thẻ).

### App 3 — Máy bán hàng tự động (Vending Machine)

Vending machine là bài toán mẫu trong mọi giáo trình lý thuyết tính toán. Input là các mệnh giá coin, state là tổng tiền đã nhập, accept state là khi đủ tiền.

Demo:
- Màn 7: Vẽ máy, hiện state (tổng tiền), các nút nhập coin 5k/10k/20k. Khi đủ 20k thì ra hàng + trả lại tiền thừa.

### App 4 — Kiểm tra chuỗi / Pattern Matching

Dùng NFA để tìm pattern trong văn bản, sau đó convert sang DFA. Tái sử dụng được code `bai_nang_cao_nfa_sang_dfa` đã viết ở TH2.

Thực tế: grep, Ctrl+F trong browser, antivirus scan signature đều dùng cơ chế này.

Demo:
- Màn 7: Nhập text + pattern, NFA chạy và highlight vị trí match.
- Màn 8: Visualize quá trình NFA → DFA conversion (subset construction).

---

## 8 màn hình

```
Màn 1  Home — giới thiệu FA, menu điều hướng
Màn 2  Traffic Light — sơ đồ DFA + animation đèn
Màn 3  Traffic Light — step-by-step, bảng transition log
Màn 4  ATM — giả lập thao tác, hiện state machine
Màn 5  ATM — sơ đồ state + test case lỗi (sai PIN)
Màn 6  Vending Machine — nhập coin, animate ra hàng
Màn 7  Pattern Search — NFA match, highlight kết quả
Màn 8  NFA → DFA — visualize subset construction
```

---

## Stack kỹ thuật

- Python 3, Tkinter (không cần cài thêm gì)
- FA engine tái dùng từ `practice/B2304069_TranQuangMinh_TH2.py`
- Báo cáo: LaTeX (TeX Live hoặc Overleaf)
- Slide: Beamer (LaTeX) hoặc PowerPoint tùy người trình bày

---

## Phân công

**Minh (A):** FA engine, ATM, Pattern Matching, viết báo cáo LaTeX.

**Hân (B):** Traffic Light, Vending Machine, làm slides.

---

## Kế hoạch theo stage

### Stage 1 — Setup + engine cơ bản

**Minh (A):**
- Tạo cấu trúc thư mục `src/`, `screens/`, `assets/`
- Tách `DFA`, `NFA` class ra file riêng `src/fa_engine.py`, thêm method trả về transition log từng bước
- Viết `src/atm.py` — Moore machine cho ATM
- Viết `src/pattern_search.py` — NFA match + NFA→DFA
- Dựng Tkinter skeleton: navigation + 8 màn placeholder, Màn 1 (Home) xong hoàn toàn

**Hân (B):**
- Thống nhất color scheme, font, layout chung với Minh
- Viết `src/controller.py` — DFA cho traffic light và vending machine (Minh hỗ trợ nếu cần)
- Bắt đầu đọc qua tài liệu FA cơ bản để hiểu context khi làm slides

Xong stage 1 khi: chạy được app → vào được Màn 1 → click sang các màn còn lại (dù còn trống).

---

### Stage 2 — Làm 8 màn hình

**Minh (A):**
- Màn 4+5: ATM — logic state machine, test case lỗi (sai PIN 3 lần)
- Màn 7+8: Pattern Search + NFA→DFA visualization

**Hân (B):**
- Màn 2+3: Traffic Light — animation + step mode
- Màn 6: Vending Machine — UI + logic coin (dùng `controller.py` đã viết ở Stage 1)

Xong stage 2 khi: tất cả 8 màn chạy được, không crash.

---

### Stage 3 — Báo cáo LaTeX

**Minh** viết toàn bộ báo cáo. Hân cung cấp ảnh chụp màn hình Traffic Light + Vending Machine để đưa vào báo cáo.

```
Chương 1: Giới thiệu
  - FA là gì, DFA vs NFA
  - Tại sao FA quan trọng trong thực tế

Chương 2: Ứng dụng 1 — Đèn giao thông
  - Mô hình hóa bằng DFA
  - Bảng transition function
  - Hình minh họa (export từ app)

Chương 3: Ứng dụng 2 — ATM
  - Mô hình Moore machine
  - Diagram state + transition
  - Test case

Chương 4: Ứng dụng 3 — Vending Machine
  - DFA nhận coin
  - Xử lý tiền thừa

Chương 5: Ứng dụng 4 — Pattern Matching
  - Xây dựng NFA từ pattern
  - Chuyển NFA → DFA
  - So sánh độ phức tạp

Chương 6: Kết luận
  - Nhận xét về FA trong thực tế
  - Hướng mở rộng
```

**Workflow LaTeX:**
- Dùng Overleaf hoặc local TeX Live
- Template: `\documentclass[12pt]{report}` hoặc tìm template báo cáo của trường
- Vẽ state diagram bằng package `tikz` + `automata` (đẹp hơn vẽ tay)

---

### Stage 4 — Slide + rehearsal

**Hân** làm slide theo outline dưới. Minh review nội dung kỹ thuật, sửa chỗ nào giải thích sai.

```
Trang 1    Trang bìa
Trang 2    FA là gì — tóm tắt lý thuyết ngắn gọn
Trang 3    Overview 4 ứng dụng
Trang 4-5  Traffic Light — diagram + ảnh chụp app
Trang 6-7  ATM — diagram + demo live
Trang 8-9  Vending Machine — diagram + demo live
Trang 10-11 Pattern Matching — NFA→DFA, highlight result
Trang 12   Kết luận
Trang 13   Q&A
```

Slide dùng PowerPoint hoặc Google Slides cho nhanh. Nếu Hân muốn học Beamer thì dùng Beamer.

**Minh** trình bày phần demo app live (ATM, Pattern Matching).
**Hân** trình bày phần lý thuyết + Traffic Light + Vending Machine.

Chạy rehearsal 1 lần trước khi nộp.

---

## Cấu trúc thư mục

```
project/
├── plan.md
├── src/
│   ├── main.py
│   ├── fa_engine.py        DFA + NFA (từ TH2.py)
│   ├── controller.py       traffic light + vending machine
│   ├── atm.py              ATM state machine
│   └── pattern_search.py   NFA match + NFA→DFA
├── screens/
│   ├── home.py
│   ├── traffic_screen.py
│   ├── atm_screen.py
│   ├── vending_screen.py
│   └── pattern_screen.py
├── report/
│   ├── main.tex
│   ├── chapters/
│   │   ├── intro.tex
│   │   ├── traffic.tex
│   │   ├── atm.tex
│   │   ├── vending.tex
│   │   └── pattern.tex
│   └── figures/
└── slides/
    └── presentation.tex    (hoặc .pptx)
```

---

## Ghi chú

Code FA engine từ TH2.py đã có đủ DFA + NFA + NFA→DFA conversion, không cần viết lại. Stage 1 chủ yếu là tổ chức lại code và dựng skeleton UI — xong sớm thì Stage 2 thoải mái chia song song.

Nếu ép timeline, có thể gộp Màn 2+3 (Traffic Light) thành 1 màn split-view, bỏ Màn 8 (NFA→DFA visualization) thay bằng thêm test case cho ATM — vẫn đủ 8 màn.
