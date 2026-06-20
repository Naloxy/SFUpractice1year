"""
Селютин Кирилл ЗКИ25-16Б
Вариант 20
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class ImageApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Обработка изображений")
    self.root.geometry("700x650")
    self.image = None

    tk.Button(
      root,
      text="Загрузить изображение",
      command=self.load_image
    ).pack(pady=5)

    self.image_label = tk.Label(root)
    self.image_label.pack(pady=10)

    self.status = tk.Label(
      root,
      text="Готово к работе",
      fg="blue"
    )
    self.status.pack(pady=5)

  def set_status(self, text):
    self.status.config(text=text)

  def display_image(self, img):
    self.image = img

    preview = img.copy()
    preview.thumbnail((600, 400))

    self.photo = ImageTk.PhotoImage(preview)
    self.image_label.config(image=self.photo)

  def load_image(self):
    file_path = filedialog.askopenfilename(
      title="Выберите изображение",
      filetypes=[
        ("Изображения", "*.png *.jpg *.jpeg")
      ]
    )

    if not file_path:
      self.set_status("Загрузка отменена.")
      return

    try:
      img = Image.open(file_path).convert("RGB")

      self.display_image(img)

      self.set_status(
        f"Изображение загружено: {file_path}"
      )

    except Exception as e:
      messagebox.showerror(
        "Ошибка",
        f"Не удалось открыть файл:\n{e}"
      )
      self.set_status("Ошибка загрузки изображения.")

root = tk.Tk()
app = ImageApp(root)
root.mainloop()