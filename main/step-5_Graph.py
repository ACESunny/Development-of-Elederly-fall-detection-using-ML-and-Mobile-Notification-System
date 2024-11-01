import pandas as pd
import matplotlib.pyplot as plt

# ฟังก์ชันสำหรับสร้างกราฟ
def plot_graphs():
    # อ่านข้อมูลจากไฟล์ CSV
    data_path = 'csv/data_walk.csv'
    data = pd.read_csv(data_path)
    print(data[['Movement_Rate', 'Angular_Velocity']].describe())
    
    plt.figure(figsize=(12, 6))
    
    # สร้างกราฟ Movement Rate
    plt.subplot(1, 3, 1)
    plt.plot(data.index, data['Movement_Rate'], color='blue', linestyle='-', linewidth=1) 
    plt.title('Movement Rate')
    plt.xlabel('Frame')
    plt.ylabel('Movement Rate')

    # สร้างกราฟ Angular Velocity
    plt.subplot(1, 3, 2)
    plt.plot(data.index, data['Angular_Velocity'], color='red', linestyle='-', linewidth=1) 
    plt.title('Angular Velocity')
    plt.xlabel('Frame')
    plt.ylabel('Angular Velocity')
    
    # สร้างกราฟ Scatter Plot ของ Movement Rate และ Angular Velocity
    plt.subplot(1, 3, 3)
    plt.scatter(data['Movement_Rate'], data['Angular_Velocity'], color='purple', alpha=0.5)
    plt.title('Movement Rate vs Angular Velocity')
    plt.xlabel('Movement Rate')
    plt.ylabel('Angular Velocity')

    # แสดงกราฟ
    plt.tight_layout()
    plt.show()

# เรียกใช้งานฟังก์ชัน
plot_graphs()
