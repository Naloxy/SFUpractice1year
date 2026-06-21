"""
Селютин Кирилл ЗКИ25-16Б
Вариант 20
"""
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
from torchvision import transforms
import torch
from tkinter import simpledialog
import numpy as np

class ImageApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Обработка изображений")
    self.root.geometry("800x700")

    self.image = None
    self.original_image = None
    self.display = None

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Загрузить изображение",
        command=self.load_image
    ).grid(row=0, column=0, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Сделать снимок с камеры",
        command=self.take_photo
    ).grid(row=0, column=1, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Исходное изображение",
        command=self.restore_image
    ).grid(row=0, column=2, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Обрезать изображение",
        command=self.crop_image
    ).grid(row=1, column=0, padx=5, pady=5)

    tk.Button(
        button_frame,
        text="Повысить яркость",
        command=self.increase_brightness
    ).grid(row=1, column=1, padx=5, pady=5)
    

    channel_frame = tk.Frame(root)
    channel_frame.pack(pady=10)

    tk.Button(
      channel_frame,
      text="Красный канал",
      command=lambda: self.show_channel(0)
    ).grid(row=0, column=0, padx=5)

    tk.Button(
      channel_frame,
      text="Зелёный канал",
      command=lambda: self.show_channel(1)
    ).grid(row=0, column=1, padx=5)

    tk.Button(
      channel_frame,
      text="Синий канал",
      command=lambda: self.show_channel(2)
    ).grid(row=0, column=2, padx=5)

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
    preview = img.copy()
    preview.thumbnail((600, 400))

    self.display = ImageTk.PhotoImage(preview)
    self.image_label.config(image=self.display)

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
      self.image = img
      self.original_image = img
      self.display_image(img)
      self.set_status(f"Изображение загружено: {file_path}")

    except Exception as e:
      messagebox.showerror(
        "Ошибка",
        f"Не удалось открыть файл:\n{e}"
      )
      self.set_status("Ошибка загрузки изображения.")

  def take_photo(self):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
      messagebox.showerror(
        "Ошибка",
        "Не удалось подключиться к веб-камере.\n\n"
        "Возможные причины:\n"
        "1. Камера отключена.\n"
        "2. Камера используется другим приложением.\n"
        "3. Не предоставлен доступ к камере."
      )
      self.set_status("Ошибка подключения к веб-камере.")
      return

    ret, frame = cap.read()
    cap.release()

    if not ret:
      messagebox.showerror(
        "Ошибка",
        "Не удалось получить изображение с камеры."
      )
      self.set_status("Ошибка получения изображения.")
      return

    frame = cv2.cvtColor(
      frame,
      cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(frame)
    self.image = img
    self.original_image = img
    self.display_image(img)
    self.set_status("Фотография успешно получена с веб-камеры.")

  def show_channel(self, channel):
    if self.image is None:
      messagebox.showwarning(
        "Предупреждение",
        "Сначала загрузите изображение."
      )
      self.set_status("Изображение отсутствует.")
      return

    tensor = transforms.ToTensor()(self.image)
    tensor = (tensor * 255).byte().permute(1, 2, 0)
    result = torch.zeros_like(tensor)
    result[:, :, channel] = tensor[:, :, channel]

    img = Image.fromarray(result.numpy())
    self.display_image(img)

    names = {
      0: "красный",
      1: "зелёный",
      2: "синий"
    }

    self.set_status(f"Отображён {names[channel]} канал.")

  def restore_image(self):
    if self.image is None:
      messagebox.showwarning(
        "Предупреждение",
        "Изображение отсутствует."
      )
      self.set_status("Изображение отсутствует.")
      return

    self.display_image(self.original_image)
    self.set_status("Показано исходное изображение.")
    self.image = self.original_image

  def crop_image(self):
    if self.image is None:
      messagebox.showwarning(
        "Предупреждение",
        "Сначала загрузите изображение."
      )
      return

    width, height = self.image.size
    try:
      x1 = simpledialog.askinteger(
        "Обрезка",
        f"x1 (0-{width - 1})"
      )
      y1 = simpledialog.askinteger(
        "Обрезка",
        f"y1 (0-{height - 1})"
      )
      x2 = simpledialog.askinteger(
        "Обрезка",
        f"x2 (1-{width})"
      )
      y2 = simpledialog.askinteger(
        "Обрезка",
        f"y2 (1-{height})"
      )

      if None in (x1, y1, x2, y2):
        self.set_status("Обрезка отменена.")
        return

      if (
        x1 < 0 or y1 < 0 or
        x2 > width or y2 > height or
        x1 >= x2 or y1 >= y2
      ):
        raise ValueError

      cropped = self.image.crop(
        (x1, y1, x2, y2)
      )

      self.image = cropped
      self.display_image(cropped)
      self.set_status("Изображение успешно обрезано.")

    except ValueError:
      messagebox.showerror(
        "Ошибка",
        "Некорректные координаты."
      )
  
  def increase_brightness(self):
    if self.image is None:
      messagebox.showwarning(
        "Предупреждение",
        "Сначала загрузите изображение."
      )
      return

    value = simpledialog.askinteger(
      "Яркость",
      "Введите значение увеличения яркости:"
    )

    if value is None:
      self.set_status("Изменение яркости отменено.")
      return

    try:
      img = np.array(self.image)
      img = img.astype(np.int16)
      img += value
      img = np.clip(
          img,
          0,
          255
      ).astype(np.uint8)

      result = Image.fromarray(img)
      self.image = result
      self.display_image(result)
      self.set_status(f"Яркость увеличена на {value}.")

    except Exception:
      messagebox.showerror(
        "Ошибка",
        "Не удалось изменить яркость."
      )

root = tk.Tk()
app = ImageApp(root)
root.mainloop()