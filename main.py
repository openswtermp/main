import tkinter as tk
from PIL import Image, ImageTk
from annoying_fruits import orange,pear,watermelon,apple

def start_fruit_processing(fruit_name):
    if fruit_name == "Orange":
        orange.process()
    if fruit_name == "Pear":
        pear.process()
    if fruit_name == "Watermelon":
        watermelon.process()
    if fruit_name == "Apple":
        apple.process()

def create_fruit_button(grid_row, grid_column, image_path, text, command):
    # 이미지 로드 및 변환
    img = Image.open(image_path)
    img = img.resize((100, 100), Image.Resampling.LANCZOS)

    photo = ImageTk.PhotoImage(img)

    # 버튼 생성
    btn = tk.Button(root, image=photo, command=command, borderwidth=0)
    btn.image = photo  # 참조 유지
    btn.grid(row=grid_row, column=grid_column, padx=10, pady=5)

    # 텍스트 라벨 추가
    label = tk.Label(root, text=text, font=("Arial", 14))
    label.grid(row=grid_row + 1, column=grid_column, padx=10, pady=5)

# GUI 생성
root = tk.Tk()
root.title("Annoying fruits")

root.geometry("250x450")  # 창 크기 조정

# UI 제목
tk.Label(root, text="Select a Fruit!", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)

# 과일 버튼 추가
create_fruit_button(1, 0, "assets/orange_icon.png", "Orange", lambda: start_fruit_processing("Orange"))
create_fruit_button(1, 1, "assets/watermelon_icon.png", "Watermelon", lambda: start_fruit_processing("Watermelon"))
create_fruit_button(3, 0, "assets/pear_icon.jpg", "Pear", lambda: start_fruit_processing("Pear"))
create_fruit_button(3, 1, "assets/apple.jpg", "Apple", lambda: start_fruit_processing("Apple"))

# Quit버튼 추가
tk.Button(root, text=" Quit ", command=root.destroy, font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()

