import os
import platform
import subprocess

def ping(host):
    """
    ฟังก์ชันสำหรับ ping ไปยัง host เพื่อตรวจสอบว่าอุปกรณ์นั้นตอบสนองหรือไม่
    """
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def find_devices_in_network(network_prefix):
    """
    สแกนหา IP Address ทั้งหมดในเครือข่าย
    """
    active_devices = []
    for i in range(1, 255):  # สแกน IP ตั้งแต่ .1 ถึง .254
        ip = f"{network_prefix}.{i}"
        if ping(ip):
            active_devices.append(ip)
            print(f"พบอุปกรณ์ที่: {ip}")
    return active_devices

if __name__ == "__main__":
    # เปลี่ยน network_prefix ให้ตรงกับเครือข่ายของคุณ (เช่น 192.168.1)
    network_prefix = "192.168.1"
    print(f"กำลังสแกนเครือข่าย {network_prefix}.0/24...")
    devices = find_devices_in_network(network_prefix)
    print("การสแกนเสร็จสิ้น!")
    print(f"พบอุปกรณ์ทั้งหมด: {devices}")