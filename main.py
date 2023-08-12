import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import threading
import queue

class PingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("局域网主机Ping工具")

        self.label = tk.Label(root, text="请输入IP网段（例如：192.168.1.）：")
        self.label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.ping_button = tk.Button(root, text="开始Ping", command=self.start_ping)
        self.ping_button.pack()

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress_bar.pack()

        self.queue = queue.Queue()
        self.threads = []

    def start_ping(self):
        ip_subnet = self.entry.get()
        if not ip_subnet:
            messagebox.showerror("错误", "请输入IP网段")
            return

        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 255

        self.threads = []
        for i in range(1, 256):
            ip = ip_subnet + str(i)
            thread = threading.Thread(target=self.ping_thread, args=(ip,))
            self.threads.append(thread)
            thread.start()

        self.check_progress()

    def ping_thread(self, ip):
        response = subprocess.run(["ping", "-n", "4", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if response.returncode == 0:
            self.queue.put(ip)

    def check_progress(self):
        finished_threads = sum(1 for thread in self.threads if not thread.is_alive())
        self.progress_bar["value"] = finished_threads

        if finished_threads < 255:
            self.root.after(100, self.check_progress)
        else:
            self.show_results()

    # ... 之前的代码 ...

    # ... 之前的代码 ...

    def show_results(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Ping结果")

        results = []
        while not self.queue.empty():
            results.append(self.queue.get())

        # 将 IP 地址按照数字部分进行排序
        results.sort(key=lambda ip: list(map(int, ip.split('.'))))

        results_text = tk.Text(result_window)
        results_text.pack()

        for ip in results:
            results_text.insert(tk.END, f"Ping通：{ip}\n")

    # ... 之后的代码 ...


if __name__ == "__main__":
    root = tk.Tk()
    app = PingApp(root)
    root.mainloop()