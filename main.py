```python
import cv2
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторна робота №2 — ESP32-CAM")
        self.root.geometry("800x600")

        self.camera = None
        self.running = False

        self.video_label = tk.Label(
            root, text="Камера не запущена",
            bg="black", fg="white",
            width=80, height=25
        )
        self.video_label.pack(pady=10)

        self.start_button = tk.Button(
            root, text="Почати трансляцію",
            command=self.start_camera
        )
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(
            root, text="Завершити трансляцію",
            command=self.stop_camera,
            state=tk.DISABLED
        )
        self.stop_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)

    def start_camera(self):
        if self.camera is None:
            self.camera = cv2.VideoCapture(0)

        if not self.camera.isOpened():
            self.camera.release()
            self.camera = None
            messagebox.showerror(
                "Помилка", "Не вдалося відкрити камеру."
            )
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_frame()

    def update_frame(self):
        if not self.running or self.camera is None:
            return

        success, frame = self.camera.read()

        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image.thumbnail((760, 420))
            photo = ImageTk.PhotoImage(image=image)

            self.video_label.config(image=photo, text="")
            self.video_label.image = photo

        self.root.after(30, self.update_frame)

    def stop_camera(self):
        self.running = False

        if self.camera is not None:
            self.camera.release()
            self.camera = None

        self.video_label.config(
            image="", text="Трансляцію завершено"
        )
        self.video_label.image = None

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def close_app(self):
        self.stop_camera()
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    app = CameraApp(window)
    window.mainloop()
```
