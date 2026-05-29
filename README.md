# ⚽ Tool Tự Động Gán Nhãn Football Highlight cho CVAT (YOLOv8)

Chào cậu! Đây là tài liệu hướng dẫn nhanh để sử dụng bộ công cụ tự động gán nhãn (Autolabel) bóng và khung thành bóng đá bằng model YOLOv8 custom (`best.pt`) và đóng gói để upload lên CVAT.

---

## 📁 Cấu Trúc Thư Mục Dự Án

Thư mục mới chạy độc lập (standalone) có cấu trúc như sau:

```text
cvat_autolabel/
├── best.pt            # Model YOLOv8 đã được huấn luyện sẵn (0: ball, 1: goalpost)
├── autolabel.py       # Script tự động quét video và xuất nhãn YOLO
├── pack_cvat.py       # Script đóng gói nhãn và tạo file cấu hình cho CVAT
├── hlkc.mp4           # Video mẫu (hoặc đặt tên là highlight.mp4)
└── README.md          # File hướng dẫn này
```

---

## ⚙️ Chuẩn Bị Môi Trường

Trước khi chạy, hãy cài đặt các thư viện cần thiết.

### 1. Kích hoạt môi trường ảo (Virtual Environment)
Mở terminal tại thư mục `cvat_autolabel/` và chạy lệnh:

**Trên Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```
**Trên Windows (CMD):**
```cmd
.\.venv\Scripts\activate.bat
```
*(Nếu chưa có môi trường ảo, bạn có thể chạy trực tiếp python của máy hoặc tạo mới bằng `python -m venv .venv`)*

### 2. Cài đặt các thư viện (nếu chưa cài)
```bash
pip install ultralytics opencv-python numpy
```

---

## 🚀 Hướng Dẫn Sử Dụng

Quy trình gán nhãn tự động gồm **2 bước** cực kỳ đơn giản:

### Bước 1: Quét Video và Gán Nhãn Tự Động (`autolabel.py`)
Đặt file video của bạn vào thư mục `cvat_autolabel/` với tên `hlkc.mp4` (hoặc `highlight.mp4`). Sau đó chạy script gán nhãn:

```bash
python autolabel.py
```

* **Cơ chế hoạt động:**
  1. Script tự động nạp model custom `best.pt` nằm cùng thư mục.
  2. Đọc từng khung hình (frame) của video.
  3. Sử dụng mô hình YOLOv8 để nhận diện vị trí bóng (`ball` - class 0) và khung thành (`goal` - class 1).
  4. Tạo ra thư mục `cvat_upload/obj_train_data/` chứa các file nhãn `.txt` tương ứng với mỗi frame.

---

### Bước 2: Đóng Gói Nhãn Chuẩn Định Dạng CVAT (`pack_cvat.py`)
Sau khi chạy xong bước 1, chạy tiếp script đóng gói:

```bash
python pack_cvat.py
```

* **Cơ chế hoạt động:**
  1. Tự động kiểm tra danh sách file tọa độ đã tạo.
  2. Sắp xếp thứ tự các file theo thứ tự frame từ nhỏ đến lớn.
  3. Tạo file `train.txt` danh sách ánh xạ các frame.
  4. Tạo file cấu hình `obj.data` và danh sách nhãn `obj.names` đúng định dạng YOLO 1.1 của CVAT.
  5. Nén toàn bộ cấu hình và các file nhãn `.txt` vào file zip duy nhất là **`cvat_ready.zip`** nằm ngay ở thư mục gốc của `cvat_autolabel/`.

---

## 📤 Hướng Dẫn Upload Lên CVAT

Để import nhãn này vào CVAT, làm theo các bước sau:

1. **Tạo Task trên CVAT:**
   * Lên CVAT tạo mới một **Task**.
   * Đặt tên cho Task và thêm 2 nhãn (Labels) với tên chính xác là:
     * `ball`
     * `goal`
   * Tải file video (`hlkc.mp4` hoặc `highlight.mp4`) lên Task này và nhấn **Submit**.

2. **Upload Annotations:**
   * Sau khi CVAT xử lý xong video, bấm vào nút ba chấm ở góc phải của Task hoặc Job đó.
   * Chọn **Upload Annotations**.
   * Chọn định dạng **`YOLO 1.1`**.
   * Chọn và tải lên file **`cvat_ready.zip`** vừa được tạo ra ở Bước 2.
   * Bấm **OK** và tận hưởng thành quả gán nhãn tự động!

---

*Chúc cậu gán nhãn hiệu quả và nhanh chóng! Nếu có bất kỳ câu hỏi nào, hãy liên hệ tớ nhé.*
