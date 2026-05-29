import os
import zipfile

def main():
    output_dir = 'cvat_upload'
    zip_filename = 'cvat_ready.zip'
    
    # 1. Kiểm tra thư mục chứa nhãn đã được tạo chưa
    labels_dir = os.path.join(output_dir, 'obj_train_data')
    if not os.path.exists(labels_dir):
        print(f"Lỗi: Thư mục chứa nhãn '{labels_dir}' không tồn tại!")
        print("Vui lòng chạy file autolabel.py trước để tự động tạo nhãn.")
        return

    print("Đang dọn dẹp và đóng gói hành lý cho chuẩn CVAT...")

    # Quét lấy toàn bộ các file tọa độ đã tạo (sắp xếp tăng dần theo tên file để đảm bảo thứ tự)
    txt_files = sorted([f for f in os.listdir(labels_dir) if f.endswith('.txt')])
    num_files = len(txt_files)
    
    if num_files == 0:
        print(f"Lỗi: Không tìm thấy file nhãn .txt nào trong thư mục '{labels_dir}'!")
        return
        
    print(f"Tìm thấy {num_files} file nhãn .txt. Đang tiến hành đóng gói...")

    # 2. Tự động tạo file train.txt
    train_txt_path = os.path.join(output_dir, 'train.txt')
    with open(train_txt_path, 'w') as f:
        for txt_file in txt_files:
            # YOLO đòi phải có list file ảnh ảo (đuôi .jpg) để map với file .txt
            img_name = txt_file.replace('.txt', '.jpg')
            f.write(f"obj_train_data/{img_name}\n")
            
    # 3. Ghi đè lại file obj.data cho tuyệt đối chuẩn sách giáo khoa
    obj_data_path = os.path.join(output_dir, 'obj.data')
    with open(obj_data_path, 'w') as f:
        f.write("classes = 2\n")
        f.write("names = obj.names\n")
        f.write("train = train.txt\n")
        
    # 4. Nén Zip chuẩn gốc (Root Zip) - Ép file ra ngay mặt tiền
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Nhét 3 file cấu hình vào thẳng root
        for file in ['obj.names', 'obj.data', 'train.txt']:
            file_path = os.path.join(output_dir, file)
            if os.path.exists(file_path):
                zipf.write(file_path, arcname=file)
        
        # Nhét toàn bộ file tọa độ vào thư mục obj_train_data trong zip
        for txt_file in txt_files:
            file_path = os.path.join(labels_dir, txt_file)
            arcname = os.path.join('obj_train_data', txt_file)
            zipf.write(file_path, arcname=arcname)
            
    print(f"Hoàn hảo! Đã đóng gói thành công {num_files} file nhãn vào '{zip_filename}'.")
    print("Hãy lấy đúng file này upload lên CVAT làm Annotations!")

if __name__ == "__main__":
    main()
