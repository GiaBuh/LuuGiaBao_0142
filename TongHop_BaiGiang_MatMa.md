# Tổng hợp Bài giảng Mật mã học (Lab 02 & Lab 03)

Tài liệu này tổng hợp các kiến thức đã trao đổi về các thuật toán mã hóa cổ điển và hiện đại.

## 1. Mật mã Caesar (Mã hóa thay thế - Substitution Cipher)
- **Cơ chế:** Dịch chuyển từng chữ cái trong bảng chữ cái đi `K` bước.
- **Công thức:** 
  - Mã hóa: $E(x) = (x + K) \pmod{26}$
  - Giải mã: $D(x) = (x - K) \pmod{26}$
- **Ưu điểm:** Đơn giản, dễ hiểu.
- **Nhược điểm:** Rất yếu, dễ bị tấn công vét cạn (Brute-force) vỏn vẹn 25 trường hợp hoặc phân tích tần suất chữ cái.

## 2. Mật mã Playfair (Mã hóa đa ký tự - Digraph Substitution)
- **Cơ chế:** Sử dụng Ma trận 5x5 chứa cả Khóa và các chữ cái còn lại (gộp I và J). Bản rõ được bẻ thành từng cặp chữ cái.
- **Quy tắc:**
  1. Cùng hàng: Lấy chữ bên phải.
  2. Cùng cột: Lấy chữ bên dưới.
  3. Khác hàng/cột: Lấy góc đối diện của hình chữ nhật.
- **Mã nguồn:** Code xử lý rất tốt việc cắt ma trận, tuy nhiên có một thiếu sót nhỏ ở quy tắc bẻ chữ (chưa chèn X giữa 2 ký tự giống nhau liên tiếp ở bước Mã hóa). Về cơ bản, xử lý vòng lặp xoay `% 5` cực kỳ thông minh.

## 3. Mật mã Rail Fence (Hàng rào mã hóa - Transposition Cipher)
- **Cơ chế:** Thay vì biến đổi chữ cái, thuật toán đi tráo đổi vị trí của chúng. Viết các chữ theo hình zigzag lên $K$ dòng, sau đó đọc ngang từng dòng lại với nhau.
- **Mã nguồn:** Module được lập trình hoàn hảo nhất. Để giải mã, thuật toán tạo một cuốn sổ rỗng `[0] * K` đếm xem mỗi hàng chứa bao nhiêu chữ, sau đó cắt Bản Mã thả lại vào mảng rồi đọc zigzag một lần nữa. Rất tinh xảo bằng tư duy Lập trình Khai báo (Slicing/Queue).

## 4. Columnar Transposition (Mã hóa hoán vị theo cột)
- **Cơ chế:** Viết văn bản ngang theo hàng tự động chia cột, đọc dọc từ trên xuống dưới theo từng cột. 
- **Mã nguồn:**
  - Hàm **Encrypt:** Dùng bước lùi con trỏ `pointer += key` rất thông minh.
  - Hàm **Decrypt:** Phát hiện lỗi Logic kinh điển! Việc tạo mảng `[''] * key` (lấy Khóa làm số Cột giải mã) thay vì dùng toán học tính số Cột mới `math.ceil(len(text)/key)` khiến chương trình giải mã bị sai lệch vị trí với hầu hết các độ dài văn bản lẻ. Một bài học tuyệt vời về tầm quan trọng của Unit Test trong Security!

## 5. Mật mã Vigenère (Thay thế đa bảng chữ cái)
- **Cơ chế:** Caesar "Nâng cấp" với chìa khóa lặp lại. Cử khắc tinh chống lại phép Đếm tần suất chữ cái do 1 chữ 'A' có thể biến thành 2 chữ cái hoàn toàn khác nhau.
- **Mã nguồn:** Cách viết cực kỳ đỉnh cao. Biết sử dụng `isalpha()`, `isupper()`, `chr()` và `ord()` để xử lý chuẩn xác mã ASCII, phớt lờ Dấu Câu và Khoảng trắng. Thuật toán vững chãi.

## 6. Mật mã RSA & ECC (Lab 03 - Hệ mã hóa Phi đối xứng/Asymmetric)
- **Cơ chế:** Khác với mã cổ điển, ở đây dùng 2 chìa khóa riêng biệt: Khóa Công Khai (Mã hóa / Xác minh Chữ Ký) và Khóa Bí Mật (Giải mã / Ký nháy).
- **Thực tiễn:** RSA & ECC dính líu đến tính toán số nguyên tố lớn và các phương trình đường cong Elliptic cực rủi ro để "tự code chay". Việc ứng dụng thư viện `rsa` và `ecdsa` mô phỏng định dạng PEM/PKCS1 chính là quy chuẩn Công nghiệp (chuẩn kiến trúc HTTPS/SSL ngày nay).
