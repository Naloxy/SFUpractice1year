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

class ImageApp:
  def __init__(self, root):
    self.root = root
    self.root.title("Обработка изображений")
    self.root.geometry("700x650")

    self.image = None
    self.photo = None
    self.original_image = None

    tk.Button(
      root,
      text="Загрузить изображение",
      command=self.load_image
    ).pack(pady=5)

    tk.Button(
      root,
      text="Сделать снимок с камеры",
      command=self.take_photo
    ).pack(pady=5)

    # Кнопки каналов
    channel_frame = tk.Frame(root)
    channel_frame.pack(pady=5)

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

    # Кнопка восстановления
    tk.Button(
      root,
      text="Исходное изображение",
      command=self.restore_image
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
    self.original_image = img
    self.display_image(img)
    self.set_status("Фотография успешно получена с веб-камеры.")

  def show_channel(self, channel):
    if self.original_image is None:
      messagebox.showwarning(
        "Предупреждение",
        "Сначала загрузите изображение."
      )
      self.set_status("Изображение отсутствует.")
      return

    tensor = transforms.ToTensor()(self.original_image)
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
    if self.original_image is None:
      messagebox.showwarning(
        "Предупреждение",
        "Изображение отсутствует."
      )
      self.set_status("Изображение отсутствует.")
      return

    self.display_image(self.original_image)
    self.set_status("Показано исходное изображение.")

root = tk.Tk()
app = ImageApp(root)
root.mainloop()