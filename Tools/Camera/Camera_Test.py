import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import cv2
import csv
import time
from datetime import datetime  # นำเข้าโมดูล datetime

# ตั้งค่า
CAMERA_URL = 0
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
FPS = 30

# ตั้งค่ากล้อง CCTV
cap = cv2.VideoCapture(CAMERA_URL)

# ตรวจสอบว่ากล้องเปิดได้หรือไม่
if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

# ตั้งค่าความละเอียดเป็น FHD (1920x1080)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# ตั้งค่าเฟรมเรต
cap.set(cv2.CAP_PROP_FPS, FPS)

# ตรวจสอบเฟรมเรตจริงของกล้อง
actual_fps = cap.get(cv2.CAP_PROP_FPS)
print(f"เฟรมเรตที่กล้องตั้งค่าไว้: {actual_fps} FPS")

# สร้างชื่อไฟล์ CSV โดยใช้วันที่ปัจจุบัน
current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f'frame_fps_{current_date}.csv'

# สร้างไฟล์ CSV เพื่อบันทึกเวลา
csv_file = open(csv_filename, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Frame_Number', 'FPS'])
frame_count = 1

# ตัวแปรสำหรับคำนวณ FPS
prev_time = 0  # เวลาของเฟรมก่อนหน้า
curr_time = 0  # เวลาปัจจุบัน

delay = 1 / FPS  # เวลาที่ต้องรอระหว่างเฟรม

try:
    while True:
        # วัดเวลาเริ่มต้น
        prev_time = time.time()
        
        # รับเฟรมจากกล้อง
        ret, frame = cap.read()
        if not ret:
            print("ไม่สามารถรับเฟรมจากกล้องได้")
            break

        # รอให้ครบเวลา 1/30 วินาที
        elapsed_time = time.time() - prev_time
        if elapsed_time < delay:
            time.sleep(delay - elapsed_time)
            
        # วัดเวลาสิ้นสุด
        curr_time = time.time()
        
        # คำนวณเวลา difference
        time_diff = curr_time - prev_time
        
        # คำนวณ FPS
        fps = int(1 / time_diff)

        # บันทึกข้อมูลลงใน CSV
        csv_writer.writerow([frame_count, fps])

        # แสดง FPS บนเฟรม
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # แสดงภาพของเฟรม
        cv2.imshow('Camera', frame)
        

        # เพิ่มจำนวนเฟรม
        frame_count += 1

        # หยุดโปรแกรมเมื่อกดปุ่ม 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # ปิดการเชื่อมต่อกล้องและไฟล์ CSV
    cap.release()
    csv_file.close()
    cv2.destroyAllWindows()
    print(f"บันทึกข้อมูลเสร็จสิ้น: {csv_filename}")