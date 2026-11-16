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
1. Giới thiệu
   - FA là gì, lịch sử hình thành
   - DFA vs NFA — điểm giống và khác nhau
   - Ứng dụng FA trong thực tế (tổng quan)

2. Mục tiêu bài toán
   - Mô phỏng 4 hệ thống thực tế bằng FA
   - Xây dựng giao diện demo trực quan (8 màn hình)
   - Minh chứng FA không chỉ là lý thuyết

3. Phương pháp thực hiện
   - Quy trình mô hình hóa: bài toán thực → FA
     (xác định states, alphabet, transition function, accept states)
   - DFA cho hệ thống tuần tự (Traffic Light, Vending Machine)
   - Moore machine cho hệ thống có output (ATM)
   - NFA + NFA→DFA conversion cho Pattern Matching
   - Công cụ: Python 3, Tkinter, tikz (vẽ diagram trong báo cáo)

4. Thiết kế và cài đặt
   4.1 Traffic Light
       - State diagram, bảng transition function
       - Cài đặt DFA, animation màn hình
   4.2 ATM
       - Moore machine diagram, bảng transition
       - Xử lý test case: sai PIN 3 lần → khóa thẻ
   4.3 Vending Machine
       - DFA nhận coin 5k/10k/20k, state = tổng tiền
       - Xử lý tiền thừa khi vượt mệnh giá
   4.4 Pattern Matching
       - Xây dựng NFA từ pattern
       - Subset construction: NFA → DFA
       - Highlight kết quả match trong text

5. Kết quả đạt được
   - Ảnh chụp từng màn hình demo
   - Nhận xét: ưu/nhược điểm FA khi áp dụng thực tế
   - So sánh NFA vs DFA trong Pattern Matching (độ phức tạp)

6. Hướng phát triển
   - Mở rộng ATM: chuyển khoản, nhiều loại thẻ, timeout session
   - Pattern Matching: hỗ trợ regex đầy đủ, Aho-Corasick nhiều pattern
   - Tích hợp epsilon-NFA để xử lý bài toán phức tạp hơn
   - Áp dụng FA vào các bài toán lớn hơn: lexer compiler, network protocol

7. Tài liệu tham khảo
   - Giáo trình môn Lý thuyết tính toán
   - Introduction to the Theory of Computation — Michael Sipser
   - Các nguồn khác (ghi theo chuẩn IEEE)
```

**Workflow LaTeX:**
- Dùng Overleaf hoặc local TeX Live
- Template: `\documentclass[12pt]{report}` hoặc template báo cáo của trường
- Vẽ state diagram bằng package `tikz` + `automata`
- Mỗi app là 1 subsection trong mục 4, dùng `\input{chapters/...}` để chia file (đẹp hơn vẽ tay)

---

### Stage 4 — Slide + rehearsal

**Hân** làm slide theo cấu trúc yêu cầu. Minh review nội dung kỹ thuật, sửa chỗ nào giải thích sai.

```
1. Giới thiệu
   - FA là gì, DFA vs NFA (tóm tắt ngắn)
   - Tại sao FA xuất hiện trong thực tế
   - Overview 4 ứng dụng sẽ trình bày

2. Mục tiêu bài toán
   - Mục tiêu từng app: mô phỏng hệ thống thực tế bằng FA
   - Yêu cầu demo: 8 màn hình giao diện tương tác

3. Phương pháp thực hiện
   - Mô hình hóa bài toán thực tế thành DFA/NFA
   - Các bước: xác định states → alphabet → transition function → accept states
   - Lý do chọn Python + Tkinter

4. Thiết kế và cài đặt
   - Traffic Light: state diagram, bảng transition, ảnh chụp app
   - ATM: Moore machine diagram, bảng transition, test case sai PIN
   - Vending Machine: DFA nhận coin, xử lý tiền thừa, ảnh chụp app
   - Pattern Matching: NFA từ pattern, NFA→DFA conversion, ảnh highlight kết quả

5. Kết quả đạt được
   - Demo live từng app (hoặc ảnh chụp nếu không demo trực tiếp)
   - Nhận xét: FA phù hợp với dạng bài toán nào

6. Hướng phát triển
   - Mở rộng ATM: thêm giao dịch chuyển khoản, nhiều loại thẻ
   - Mở rộng Pattern Matching: hỗ trợ regex đầy đủ
   - Tích hợp epsilon-NFA để xử lý bài toán phức tạp hơn

7. Tài liệu tham khảo
   - Giáo trình môn học
   - Introduction to the Theory of Computation — Michael Sipser
   - Các nguồn tham khảo khác (ghi theo chuẩn IEEE hoặc APA)
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
