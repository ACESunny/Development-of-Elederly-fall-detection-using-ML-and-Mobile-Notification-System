import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# ฟังก์ชันสำหรับเลือกไฟล์ CSV
def select_csv_file():
    Tk().withdraw()  # ซ่อนหน้าต่างหลักของ Tkinter
    file_path = askopenfilename(filetypes=[("CSV files", "*.csv")])
    return file_path

# ฟังก์ชันสำหรับสร้างกราฟเส้นแสดงความถี่ของ FPS
def create_line_plot(file_path):
    # อ่านไฟล์ CSV
    df = pd.read_csv(file_path)
    
    # ตรวจสอบว่ามีคอลัมน์ 'FPS' หรือไม่
    if 'FPS' not in df.columns:
        print("ไฟล์ CSV ต้องมีคอลัมน์ 'FPS'")
        return
    
    # คำนวณความถี่ของค่า FPS
    fps_frequency = df['FPS'].value_counts().sort_index()
    
    # สร้างกราฟเส้น
    plt.plot(fps_frequency.index, fps_frequency.values, marker='o', linestyle='-', color='blue')
    plt.title('Frequency of FPS')
    plt.xlabel('FPS')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# เรียกใช้ฟังก์ชัน
if __name__ == "__main__":
    file_path = select_csv_file()
    if file_path:
        create_line_plot(file_path)