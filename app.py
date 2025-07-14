import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import subprocess
import threading
import time
import os
import json
import datetime

CONFIG_FILE = "upkeep_config.json"
LOG_FILE = "upkeep_log.txt"
MAX_SERVERS = 5

class UpKeepApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("UpKeep - Server Uptime Monitor")
        self.geometry("500x300")
        self.resizable(False, False)
        self.dark_mode = False
        self.servers = []
        self.ping_interval = 10  # in seconds
        self.ping_thread = None
        self.ping_running = False

        self.load_config()
        self.setup_ui()
        self.apply_theme()
        self.start_ping_loop()

    def setup_ui(self):
        menubar = tk.Menu(self)
        upkeep_menu = tk.Menu(menubar, tearoff=0)
        upkeep_menu.add_command(label="Exit", command=self.on_close)
        menubar.add_cascade(label="UpKeep", menu=upkeep_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Toggle Dark Mode", command=self.toggle_theme)
        settings_menu.add_command(label="Set Ping Interval", command=self.change_interval)
        settings_menu.add_command(label="Clear Servers", command=self.clear_servers)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "UpKeep by BrockerDev"))
        menubar.add_cascade(label="About", menu=about_menu)

        self.config(menu=menubar)

        self.listbox = tk.Listbox(self, font=("Consolas", 11))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        controls = tk.Frame(self)
        controls.pack(pady=5)

        self.add_btn = ttk.Button(controls, text="Add Server", command=self.add_server)
        self.add_btn.grid(row=0, column=0, padx=5)

        self.refresh_btn = ttk.Button(controls, text="Refresh Now", command=self.manual_refresh)
        self.refresh_btn.grid(row=0, column=1, padx=5)

        self.stats_label = tk.Label(self, text="", anchor="w")
        self.stats_label.pack(fill=tk.X, padx=10)

        self.statusbar = tk.Label(self, text="Starting...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def apply_theme(self):
        if self.dark_mode:
            self.configure(bg="#222222")
            self.listbox.config(bg="#333333", fg="white", selectbackground="#555555")
            self.stats_label.config(bg="#222222", fg="white")
            self.statusbar.config(bg="#333333", fg="white")
            style = ttk.Style(self)
            style.theme_use("clam")
        else:
            self.configure(bg="#f0f0f0")
            self.listbox.config(bg="white", fg="black", selectbackground="#cce5ff")
            self.stats_label.config(bg="#f0f0f0", fg="black")
            self.statusbar.config(bg="#e0e0e0", fg="black")
            style = ttk.Style(self)
            style.theme_use("default")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.save_config()

    def change_interval(self):
        val = simpledialog.askinteger("Ping Interval", "Set ping interval (seconds):", initialvalue=self.ping_interval, minvalue=1, maxvalue=3600)
        if val:
            self.ping_interval = val
            self.save_config()

    def clear_servers(self):
        if messagebox.askyesno("Clear Servers", "Remove all servers?"):
            self.servers.clear()
            self.listbox.delete(0, tk.END)
            self.save_config()

    def add_server(self):
        if len(self.servers) >= MAX_SERVERS:
            messagebox.showwarning("Limit reached", f"Maximum {MAX_SERVERS} servers allowed.")
            return
        ip = simpledialog.askstring("Add Server", "Enter IP or domain:")
        if ip and ip.strip() and ip not in self.servers:
            self.servers.append(ip.strip())
            self.save_config()
            self.update_server_list([])

    def update_server_list(self, statuses):
        self.listbox.delete(0, tk.END)
        online_count = 0
        for idx, server in enumerate(self.servers):
            status = statuses[idx] if idx < len(statuses) else "Unknown"
            display_text = f"{server}: {status}"
            self.listbox.insert(tk.END, display_text)
            if "Online" in status:
                online_count += 1
        self.stats_label.config(text=f"Online: {online_count} / {len(self.servers)}")

    def manual_refresh(self):
        if not self.ping_running:
            self.statusbar.config(text="Refreshing...")
            threading.Thread(target=self.ping_servers, daemon=True).start()
        else:
            messagebox.showinfo("Info", "Ping already running.")

    def ping_servers(self):
        self.ping_running = True
        statuses = []
        for server in self.servers:
            alive = self.ping(server)
            statuses.append("🟢 Online" if alive else "🔴 Offline")
            self.log_status(server, alive)
            if not alive:
                self.send_notification(server)
        self.after(0, lambda: self.update_server_list(statuses))
        self.after(0, lambda: self.statusbar.config(text="Monitoring..."))
        self.ping_running = False

    def start_ping_loop(self):
        if not self.ping_running:
            threading.Thread(target=self.ping_servers, daemon=True).start()
        self.after(self.ping_interval * 1000, self.start_ping_loop)

    def ping(self, host):
        try:
            param = "-n" if os.name == "nt" else "-c"
            command = ["ping", param, "1", "-w", "2", host]
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return result.returncode == 0
        except Exception:
            return False

    def send_notification(self, server_ip):
        if os.name != "nt":
            subprocess.Popen(["notify-send", f"Server Down: {server_ip}"])

    def log_status(self, server_ip, status):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a") as f:
            f.write(f"[{now}] {server_ip} - {'Online' if status else 'Offline'}\n")

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.servers = data.get("servers", [])
                self.dark_mode = data.get("dark_mode", False)
                self.ping_interval = data.get("interval", 10)

    def save_config(self):
        data = {
            "servers": self.servers,
            "dark_mode": self.dark_mode,
            "interval": self.ping_interval
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def on_close(self):
        self.save_config()
        self.destroy()

if __name__ == "__main__":
    app = UpKeepApp()
    app.mainloop()
