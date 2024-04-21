import tkinter as tk
from tkinter import filedialog, ttk
from tabulate import tabulate
import csv
import os

def draw_separator(canvas, x, height):
    canvas.create_line(x, 0, x, height, fill="black", width=2)

def read_csv(filename):
    data = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def add_column():
    selected_index = listbox.curselection()
    if selected_index:
        selected_column = listbox.get(selected_index)
        listbox2.insert(tk.END, selected_column)

def delete_column():
    selected_index = listbox2.curselection()
    if selected_index:
        listbox2.delete(selected_index)

def execute_model():
    selected_model = model_combobox.get()
    print("Đã chọn model:", selected_model)

def update_variable_options():
    # Xóa các giá trị cũ trong Listbox
    listbox.delete(0, 'end')
    
    # Lấy danh sách các biến từ DataFrame
    variables = column_names

    # Cập nhật giá trị trong Listbox
    for var in variables:
        listbox.insert('end', var)

def browse_file():
    global data
    global column_names
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        base_name = os.path.basename(filename)
        label_select_csv.config(text="Tệp đã chọn: " + base_name)
        data = read_csv(filename)
        if data:
            column_names = data[0]
            combobox["values"] = column_names
            update_variable_options()
            on_show_data_table()  # Hiển thị dữ liệu trong bảng sau khi đọc

def on_show_data_table(): 
    data_table.delete("1.0", tk.END)
    if data:
        table = tabulate(data, headers="firstrow", tablefmt="pretty")
        data_table.insert(tk.END, table)

# Tạo cửa sổ
window = tk.Tk()
window.title("Giao diện 1 hàng 2 cột")

# Tính toán kích thước màn hình
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Tính toán kích thước cột
col1_width = int(screen_width * 0.3)
col2_width = int(screen_width * 0.7)

# Tạo Frame chứa cột 1
frame_col1 = tk.Frame(window, bg="#F0F0F0")
frame_col1.grid(row=0, column=0, sticky="nsew")

# Tạo đường kẻ phân tách
canvas_separator = tk.Canvas(window, width=2, height=screen_height, bg="white", highlightthickness=0)
canvas_separator.grid(row=0, column=1, sticky="ns")
draw_separator(canvas_separator, 0, screen_height)

# Tạo Frame chứa cột 2
frame_col2 = tk.Frame(window, bg="#F0F0F0")
frame_col2.grid(row=0, column=2, sticky="nsew")

# Định cấu hình của cột 1 và cột 2
window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(2, weight=8)

# Định cấu hình của hàng
window.grid_rowconfigure(0, weight=1)

# Label và Button cho cột 1
label_select_csv = tk.Label(frame_col1, text="Chọn tệp CSV:")
label_select_csv.pack(pady=(50, 10))

button_select_csv = tk.Button(frame_col1, text="Chọn tệp CSV", command=browse_file)
button_select_csv.pack(pady=10)

# Combobox cho cột 1
combobox = ttk.Combobox(frame_col1, state="readonly")
combobox.pack(pady=10)

# Listbox cho cột 1
listbox = tk.Listbox(frame_col1)
listbox.pack(pady=10)

# Nút thêm cho cột 1
button_add = tk.Button(frame_col1, text="Thêm", command=add_column)
button_add.pack(pady=10)

# Listbox thứ hai cho cột 1
listbox2 = tk.Listbox(frame_col1)
listbox2.pack(pady=10)

# Nút xoá cho cột 1
button_delete = tk.Button(frame_col1, text="Xoá", command=delete_column)
button_delete.pack(pady=10)

# Label "Chọn model" cho cột 1
label_select_model = tk.Label(frame_col1, text="Chọn model:")
label_select_model.pack(pady=10)

# Combobox chứa các model cho cột 1
model_combobox = ttk.Combobox(frame_col1, values=["Linear", "Logistic", "KNN"])
model_combobox.pack(pady=10)

# Nút thực thi cho cột 1
execute_button = tk.Button(frame_col1, text="Thực thi", command=execute_model)
execute_button.pack(pady=10)

# Định cấu hình của frame_col2
frame_col2.grid_columnconfigure(0, weight=1)
frame_col2.grid_rowconfigure(0, weight=1)
frame_col2.grid_rowconfigure(1, weight=9)

# Tạo hàng đầu tiên của frame_col2
frame_col2_row1 = tk.Frame(frame_col2, bg="blue")
frame_col2_row1.grid(row=0, column=0, sticky="nsew")

int_convert_button = tk.Button(frame_col2_row1, text="Int convert", )
int_convert_button.pack(side="left", padx=5, pady=5)

float_convert_button = tk.Button(frame_col2_row1, text="Float convert", )
float_convert_button.pack(side="left", padx=5, pady=5)

category_convert_button = tk.Button(frame_col2_row1, text="Category convert", )
category_convert_button.pack(side="left", padx=5, pady=5)

remove_column_button = tk.Button(frame_col2_row1, text="Remove column", )
remove_column_button.pack(side="left", padx=5, pady=5)

fill_data_button = tk.Button(frame_col2_row1, text="Fill data", )
fill_data_button.pack(side="left", padx=5, pady=5)

data_table_frame = tk.Frame(frame_col2)
data_table_frame.grid(row=1, column=0, sticky="nsew")

# Tạo phối cảnh chứa Text widget và thanh trượt dọc
text_scroll_frame = tk.Frame(data_table_frame, bg="white")
text_scroll_frame.pack(side="top", fill="both", expand=True)

# Tạo Text widget trong phối cảnh mới
data_table = tk.Text(text_scroll_frame, wrap="none", height=20, width=80)
data_table.pack(side="left", fill="both", expand=True)

# Tạo thanh trượt dọc
scrollbar_y = tk.Scrollbar(text_scroll_frame, command=data_table.yview)
scrollbar_y.pack(side="right", fill="y")

# Kích hoạt thanh trượt dọc cho Text widget
data_table.config(yscrollcommand=scrollbar_y.set)

# Tạo thanh trượt ngang
scrollbar_x = tk.Scrollbar(data_table_frame, orient="horizontal", command=data_table.xview)
scrollbar_x.pack(side="bottom", fill="x")

# Kích hoạt thanh trượt ngang cho Text widget
data_table.config(xscrollcommand=scrollbar_x.set)

# Chạy ứng dụng
window.mainloop()
