import cv2
import numpy as np
import pyautogui
import time
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker Application")

        # Banner
        banner = """
                      Yb    `Yb.   Yb    88888 Yb    88888 8888P Yb  dP
    ________ ________  Yb     `Yb.  Yb   88     Yb      88   dP   YbdP
    """""""" """"""""   Yb    .dP'   Yb  88      Yb     88  dP    dPYb
                         Yb .dP'      Yb 88888    Yb 88888 d8888 dP  Yb

                         
                         BOSS
                         tele: zikdevtd
    """
        self.banner_label = tk.Label(root, text=banner, justify="left", font=("Courier", 10))
        self.banner_label.pack(pady=10)

        # Frame cho các đường dẫn mẫu ảnh
        self.paths_frame = tk.Frame(root)
        self.paths_frame.pack(pady=10)

        self.paths = {}
        for i in range(1, 6):
            lbl = tk.Label(self.paths_frame, text=f"Đường dẫn đến temp{i}:")
            lbl.grid(row=i-1, column=0, padx=5, pady=5, sticky="e")
            
            entry = tk.Entry(self.paths_frame, width=50)
            entry.grid(row=i-1, column=1, padx=5, pady=5)
            
            btn = tk.Button(self.paths_frame, text="Chọn", command=lambda i=i: self.browse_file(i))
            btn.grid(row=i-1, column=2, padx=5, pady=5)
            
            self.paths[i] = entry

        # Buttons Start và Stop
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        self.start_button = tk.Button(self.buttons_frame, text="Bắt đầu", command=self.start_autoclick)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(self.buttons_frame, text="Dừng", command=self.stop_autoclick, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10)

        # Text area để hiển thị log
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20, state='disabled')
        self.log_area.pack(pady=10)

        # Biến để kiểm soát vòng lặp
        self.running = False
        self.thread = None

    def browse_file(self, temp_num):
        file_path = filedialog.askopenfilename(title=f"Chọn file cho temp{temp_num}", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if file_path:
            self.paths[temp_num].delete(0, tk.END)
            self.paths[temp_num].insert(0, file_path)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_autoclick(self):
        # Đọc đường dẫn từ các entry
        try:
            self.temp_paths = {}
            for i in range(1, 6):
                path = self.paths[i].get()
                if not path:
                    raise ValueError(f"Đường dẫn cho temp{i} không được để trống.")
                self.temp_paths[i] = cv2.imread(path, 0)
                if self.temp_paths[i] is None:
                    raise ValueError(f"Không thể tải temp{i} từ đường dẫn: {path}")
        except ValueError as ve:
            messagebox.showerror("Lỗi", str(ve))
            return

        # Vô hiệu hóa nút Start và kích hoạt nút Stop
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.log("Bắt đầu tự động click.")

        self.running = True
        self.thread = threading.Thread(target=self.autoclick_loop)
        self.thread.start()

    def stop_autoclick(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.log("Đã dừng tự động click.")

    def autoclick_loop(self):
        # Lấy kích thước màn hình
        screen_width, screen_height = pyautogui.size()

        # Xác định vùng nửa màn hình bên trái
        x1, y1 = 0, 0  # Góc trên bên trái
        width = screen_width // 2  # Nửa chiều rộng màn hình
        height = screen_height  # Toàn bộ chiều cao màn hình

        def move_to_center():
            pyautogui.moveTo(screen_width // 2, screen_height // 2)

        while self.running:
            self.log("Chụp ảnh màn hình...")
            
            # Chụp toàn màn hình
            screenshot = pyautogui.screenshot()
            screenshot = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

            # Đọc các mẫu ảnh
            temp1 = self.temp_paths.get(1)
            temp2 = self.temp_paths.get(2)
            temp3 = self.temp_paths.get(3)
            temp4 = self.temp_paths.get(4)
            temp5 = self.temp_paths.get(5)

            if temp1 is None or temp2 is None or temp3 is None or temp4 is None or temp5 is None:
                self.log("Một hoặc nhiều mẫu ảnh không được tải.")
                time.sleep(1)
                continue

            # Lấy kích thước các mẫu ảnh
            w1, h1 = temp1.shape[::-1]
            w2, h2 = temp2.shape[::-1]
            w3, h3 = temp3.shape[::-1]
            w4, h4 = temp4.shape[::-1]
            w5, h5 = temp5.shape[::-1]

            # Danh sách các mẫu theo thứ tự ưu tiên
            templates = [
                
                (temp4, w4, h4, 0.8, 0.5, "click: thoat"),
                (temp3, w3, h3, 0.8, 0.5, "click: sk3"),
                (temp2, w2, h2, 0.8, 0.4, "click: sk2"),
                (temp1, w1, h1, 0.8, 0.3, "click: sk1"),
                
                (temp5, w5, h5, 0.8, 0.4, "click: end")
            ]

            clicked = False
            for template, w, h, threshold, delay, label in templates:
                if template is not None:
                    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
                    loc = np.where(res >= threshold)
                    if len(loc[0]) > 0:
                        for pt in zip(*loc[::-1]):
                            real_x = pt[0] + w // 2
                            real_y = pt[1] + h // 2
                            pyautogui.click(real_x, real_y)
                            self.log(label)
                            move_to_center()
                            time.sleep(delay)
                            clicked = True
                            break
                    if clicked:
                        break  # Nếu đã click vào một mẫu, bỏ qua các mẫu khác

            if not clicked:
                self.log("Không tìm thấy mẫu nào khớp.")
            clicked = False

            time.sleep(0.5)  # Thời gian chờ trước khi lặp lại

        self.log("Vòng lặp tự động click đã dừng.")

def run_app():
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
