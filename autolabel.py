import cv2
import os
from ultralytics import YOLO

def main():
    # Đường dẫn đến file best.pt (ưu tiên cùng thư mục)
    model_path = 'best.pt'
    if not os.path.exists(model_path):
        # Fallback tìm trong thư mục web/backend
        model_path = os.path.join('..', 'web', 'backend', 'best.pt')
        
    if not os.path.exists(model_path):
        print(f"Lỗi: Không tìm thấy model '{model_path}'!")
        print("Hãy chắc chắn rằng file best.pt tồn tại ở cùng thư mục với script này.")
        return

    # Khởi tạo model YOLOv8 custom (đã được train sẵn ball/goalpost)
    model = YOLO(model_path)
    
    video_path = 'hlkc.mp4' # File video mặc định
    if not os.path.exists(video_path):
        # Fallback sang highlight.mp4 nếu thiếu hlkc.mp4
        if os.path.exists('highlight.mp4'):
            video_path = 'highlight.mp4'
        else:
            print("Lỗi: Không tìm thấy file video 'hlkc.mp4' hoặc 'highlight.mp4'!")
            print("Vui lòng chuẩn bị file video trong cùng thư mục.")
            return
    
    output_dir = 'cvat_upload'
    labels_dir = os.path.join(output_dir, 'obj_train_data')
    os.makedirs(labels_dir, exist_ok=True)
    
    # Class 0 là bóng (ball), Class 1 là khung thành (goal)
    with open(os.path.join(output_dir, 'obj.names'), 'w') as f:
        f.write("ball\n")
        f.write("goal\n")

    cap = cv2.VideoCapture(video_path)
    frame_id = 0
    
    print(f"Đang khởi động YOLO với model custom: {model_path}...")
    print(f"Đang quét video: {video_path}...")
    print("Quá trình quét bắt đầu, Hoàng tử chờ tớ chút nhé!")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Chạy inference
        results = model.predict(frame, verbose=False)
        
        txt_filename = os.path.join(labels_dir, f"frame_{frame_id:06d}.txt")
        
        with open(txt_filename, 'w') as f:
            for result in results:
                for box in result.boxes:
                    # Lấy 4 tọa độ chuẩn hóa (x_center, y_center, width, height)
                    x, y, w, h = box.xywhn[0].tolist()
                    
                    # Lấy class_id từ model (0: ball, 1: goalpost) khớp với obj.names
                    cvat_class_id = int(box.cls[0]) 
                    
                    # Ghi chuẩn 5 số
                    f.write(f"{cvat_class_id} {x:.6f} {y:.6f} {w:.6f} {h:.6f}\n")
                    
        frame_id += 1

    cap.release()
    print(f"Nhiệm vụ hoàn tất! Đã quét và label cả bóng lẫn khung thành cho {frame_id} frames.")
    print("Giờ Hoàng tử chỉ việc chạy file pack_cvat.py để nén thư mục nhãn lại rồi up lên CVAT!")

if __name__ == "__main__":
    main()
