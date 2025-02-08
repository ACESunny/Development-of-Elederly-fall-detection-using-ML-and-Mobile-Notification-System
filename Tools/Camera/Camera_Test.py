import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import cv2
import csv
import time
from datetime import datetime
import schedule
import tkinter as tk
from tkinter import ttk

# ฟังก์ชันสำหรับเริ่มบันทึก FPS
def start_recording():
    global CAMERA_URL, FRAME_WIDTH, FRAME_HEIGHT, FPS, TIME_TO_RECORD
    
    CAMERA_URL = camera_url_entry.get()
    if CAMERA_URL.isdigit():
        CAMERA_URL = int(CAMERA_URL)
    
    FRAME_WIDTH = int(frame_width_entry.get())
    FRAME_HEIGHT = int(frame_height_entry.get())
    FPS = int(fps_entry.get())
    TIME_TO_RECORD = int(time_to_record_entry.get())
    
    # ตั้งค่ากล้อง CCTV
    cap = cv2.VideoCapture(CAMERA_URL)

    # ตรวจสอบว่ากล้องเปิดได้หรือไม่
    if not cap.isOpened():
        print("ไม่สามารถเปิดกล้องได้")
        return

    # ตั้งค่าความละเอียด
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # ตั้งค่าเฟรมเรต
    cap.set(cv2.CAP_PROP_FPS, FPS)

    # ตรวจสอบเฟรมเรตจริงของกล้อง
    actual_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"เฟรมเรตที่กล้องตั้งค่าไว้: {actual_fps} FPS")

    # ตัวแปรสำหรับคำนวณ FPS
    prev_time = 0  # เวลาของเฟรมก่อนหน้า
    curr_time = 0  # เวลาปัจจุบัน

    delay = 1 / FPS  # เวลาที่ต้องรอระหว่างเฟรม

    def record_fps():
        # สร้างชื่อไฟล์ CSV โดยใช้วันที่ปัจจุบัน
        current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        csv_filename = f'frame_fps_{current_date}.csv'

        # สร้างไฟล์ CSV เพื่อบันทึกเวลา
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Frame_Number', 'FPS'])
            frame_count = 1

            start_time = time.time()
            
            while time.time() - start_time < TIME_TO_RECORD:  # บันทึก FPS เป็นเวลา TIME_TO_RECORD วินาที
                # วัดเวลาเริ่มต้น
                prev_time = time.time()
                
                # รับเฟรมจากกล้อง
                ret, frame = cap.read()
                if not ret:
                    print("ไม่สามารถรับเฟรมจากกล้องได้")
                    break

                # รอให้ครบเวลา 1/F วินาที
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
                    return

    # ตั้งเวลาให้ record_fps ทำงานทุก TIME_TO_RECORD วินาที
    schedule.every(TIME_TO_RECORD).seconds.do(record_fps)

    try:
        while True:
            schedule.run_pending()
            # แสดงเฟรมขณะที่รอ schedule
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Camera', frame)
            # หยุดโปรแกรมเมื่อกดปุ่ม 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        # ปิดการเชื่อมต่อกล้องและไฟล์ CSV
        cap.release()
        cv2.destroyAllWindows()
        print("โปรแกรมหยุดทำงาน")

# สร้างหน้าต่าง GUI
root = tk.Tk()
root.title("Camera Settings")

# สร้างและจัดวาง Widgets
tk.Label(root, text="Camera URL or Index:").grid(row=0, column=0, padx=10, pady=10)
camera_url_entry = tk.Entry(root)
camera_url_entry.grid(row=0, column=1, padx=10, pady=10)
camera_url_entry.insert(0, "0")

tk.Label(root, text="Frame Width:").grid(row=1, column=0, padx=10, pady=10)
frame_width_entry = tk.Entry(root)
frame_width_entry.grid(row=1, column=1, padx=10, pady=10)
frame_width_entry.insert(0, "1920")

tk.Label(root, text="Frame Height:").grid(row=2, column=0, padx=10, pady=10)
frame_height_entry = tk.Entry(root)
frame_height_entry.grid(row=2, column=1, padx=10, pady=10)
frame_height_entry.insert(0, "1080")

tk.Label(root, text="FPS:").grid(row=3, column=0, padx=10, pady=10)
fps_entry = tk.Entry(root)
fps_entry.grid(row=3, column=1, padx=10, pady=10)
fps_entry.insert(0, "30")

tk.Label(root, text="Time to Record (seconds):").grid(row=4, column=0, padx=10, pady=10)
time_to_record_entry = tk.Entry(root)
time_to_record_entry.grid(row=4, column=1, padx=10, pady=10)
time_to_record_entry.insert(0, "30")

start_button = tk.Button(root, text="Start Recording", command=start_recording)
start_button.grid(row=5, column=0, columnspan=2, pady=10)

# เริ่มการทำงานของ GUI
root.mainloop()