import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Combobox
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd

def load_csv():
    # global DATA
    # # Mở hộp thoại chọn tệp
    # file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    # # Kiểm tra xem người dùng đã chọn tệp hay chưa
    # if file_path:
    #     try:
    #         # Đọc tệp CSV và lưu vào DataFrame
    #         file_label.config(text=f"File loaded: {file_path.split('/')[-1]}")  # Only show the basename of the filepath
    #         data = pd.read_csv(file_path)
    #         update_variable_options()
    #         status_label.config(text="Tệp CSV đã được tải thành công!")
    #         # Cập nhật danh sách biến mục tiêu và biến đầu vào 1
    #         target_combobox['values'] = list(data.columns)
    #         DATA = data
    #     except Exception as e:
    #         status_label.config(text="Lỗi: Không thể tải tệp CSV!")
    # else:
    #     status_label.config(text="Lỗi: Không có tệp CSV được chọn!")
    global DATA
    global data
    global target_var
    
    file_path = filedialog.askopenfilename()
    if file_path:
        file_extension = file_path.split(".")[-1].lower()
        if file_extension == "csv":
            file_label.config(text=f"File loaded: {file_path.split('/')[-1]}")
            data = pd.read_csv(file_path)
            
        elif file_extension == "xlsx":
            data = pd.read_excel(file_path)
        elif file_extension == "json":
            data = pd.read_json(file_path)
        elif file_extension == "txt":
            with open(file_path, "r") as file:
                data = pd.DataFrame(file.readlines(), columns=["Text"])
        else:
            print("Unsupported file type")
            return
        
        update_variable_options()
        status_label.config(text="Tệp CSV đã được tải thành công!")
        target_combobox['values'] = list(data.columns)
        DATA = data
        on_show_data_table()
        
def on_show_data_table(): 
    data_table.delete(1.0, "end")
    data_table.insert("end", DATA.to_string(index=False))

def fill_nah_data():
    target_variable = target_combobox.get()
    data[str(target_variable)].fillna(value=round(data[str(target_variable)].mean(), 2), inplace=True)
    on_show_data_table()

def update_variable_options():
    # Xóa các giá trị cũ trong Listbox
    input_listbox.delete(0, 'end')
    
    # Lấy danh sách các biến từ DataFrame
    variables = list(data.columns)

    # Cập nhật giá trị trong Listbox
    for var in variables:
        input_listbox.insert('end', var)

def add_variable():
    selected_var = input_listbox.get(input_listbox.curselection())
    input_listbox2.insert('end', selected_var)
    input_listbox.delete(input_listbox.curselection())  # Xóa biến đã chọn từ select input 1

def remove_variable():
    selected_var = input_listbox2.get(input_listbox2.curselection())
    input_listbox2.delete(input_listbox2.curselection())  # Xóa biến đã chọn từ select input 2
    input_listbox.insert('end', selected_var)

def update_input_options(*args):
    selected_var = target_combobox.get()
    if selected_var:
        input_listbox.delete(0, tk.END)  # Xóa tất cả các biến trong select input 1
        for var in DATA.columns:
            if var != selected_var:
                input_listbox.insert('end', var)

def display_selected_variables():
    selected_vars = input_listbox2.get(0, tk.END)
    selected_label.config(text="Các biến đã chọn: " + ", ".join(selected_vars))

def execute():
    # Lấy giá trị từ giao diện
    target_variable = target_combobox.get()
    input_variables = input_listbox2.get(0, tk.END)
    model = model_combobox.get()

    # Kiểm tra xem đã chọn đủ thông tin cần thiết chưa
    if not target_variable or not input_variables or not model:
        status_label.config(text="Lỗi: Vui lòng chọn đủ thông tin!")
        return

    # Kiểm tra xem đã tải dữ liệu từ tệp CSV hay chưa
    if 'DATA' not in globals():
        status_label.config(text="Lỗi: Vui lòng tải tệp CSV trước!")
        return

    # Chuyển đổi dữ liệu thành DataFrame và lựa chọn các cột phù hợp
    selected_columns = [target_variable] + list(input_variables)
    selected_data = data[selected_columns]

    # Chia dữ liệu thành tập huấn luyện và tập kiểm tra
    X = selected_data.drop(columns=[target_variable])
    y = selected_data[target_variable]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Thực hiện phân tích dựa trên mô hình đã chọn
    if model == "Linear Regression":
        # Thực hiện Linear Regression
        lr_model = LinearRegression()
        lr_model.fit(X_train, y_train)
        accuracy = lr_model.score(X_test, y_test)
        status_label.config(text=f"Độ chính xác của Linear Regression: {accuracy:.2f}")

    elif model == "Logistic Regression":
        # Thực hiện Logistic Regression
        log_reg_model = LogisticRegression()
        log_reg_model.fit(X_train, y_train)
        predictions = log_reg_model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        status_label.config(text=f"Độ chính xác của Logistic Regression: {accuracy:.2f}")

    elif model == "K-Nearest Neighbors (KNN)":
        # Thực hiện KNN
        knn_model = KNeighborsClassifier()
        knn_model.fit(X_train, y_train)
        predictions = knn_model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        status_label.config(text=f"Độ chính xác của K-Nearest Neighbors (KNN): {accuracy:.2f}")

    # Hiển thị kết quả hoặc thực hiện các hành động tiếp theo tùy thuộc vào mục đích của bạn
    # Hiển thị biểu đồ
    show_accuracy_chart(model, accuracy)

def show_accuracy_chart(model, accuracy):
    plt.bar(model, accuracy)
    plt.xlabel('Model')
    plt.ylabel('Accuracy')
    plt.title('Accuracy of Models')
    plt.ylim(0, 1)  # Giới hạn trục y từ 0 đến 1
    plt.show()


# Create the main window
window = tk.Tk()
window.title("CSV Variable Selector")

# Tạo frame bên trái
left_frame = tk.Frame(window)
left_frame.pack(side="left", fill="both", expand=True)

# Tạo frame bên phải
right_frame = tk.Frame(window)
right_frame.pack(side="right", fill="both", expand=True)

button_frame = tk.Frame(right_frame)
button_frame.pack(side="top", fill="x")

button1 = tk.Button(button_frame, text="Show data", command=on_show_data_table)
button1.pack(side="left", padx=5, pady=5)

button2 = tk.Button(button_frame, text="Fill na", command=fill_nah_data)
button2.pack(side="left", padx=5, pady=5)

data_table_frame = tk.Frame(right_frame)
data_table_frame.pack(side="bottom", fill="both", expand=True)

data_table = tk.Text(data_table_frame, wrap="none")
data_table.pack(side="top", fill="both", expand=True)
scrollbar_y = tk.Scrollbar(data_table_frame, command=data_table.yview)
scrollbar_y.pack(side="right", fill="y")
data_table.config(yscrollcommand=scrollbar_y.set)
scrollbar_x = tk.Scrollbar(data_table_frame, orient="horizontal", command=data_table.xview)
scrollbar_x.pack(side="bottom", fill="x")
data_table.config(xscrollcommand=scrollbar_x.set)


# Label for CSV file upload
csv_label = tk.Label(left_frame, text="Tải tệp CSV:")
csv_label.pack(anchor='w', pady=(10, 5))

# Button for CSV file upload
load_button = tk.Button(left_frame, text="Chọn tệp CSV", command=load_csv)
load_button.pack(anchor='w', pady=5)

# Label to display the loaded file name
file_label = tk.Label(left_frame, text="No file loaded")
file_label.pack(anchor='w', pady=5)

# Combobox for target variable selection
target_var = tk.StringVar(window)
target_combobox = Combobox(window, textvariable=target_var, state="readonly")
target_combobox.pack(anchor='w', pady=5)


# More widgets for variable selection etc, also aligned left
input_var1_label = tk.Label(window, text="Select input variable 1:")
input_var1_label.pack(anchor='w', pady=5)

input_listbox = tk.Listbox(window, selectmode='multiple')
input_listbox.pack(anchor='w', pady=5)

add_button = tk.Button(window, text="Add", command=add_variable)
add_button.pack(anchor='w', pady=5)

input_var2_label = tk.Label(window, text="Select input variable 2:")
input_var2_label.pack(anchor='w', pady=5)

input_listbox2 = tk.Listbox(window, selectmode='multiple')
input_listbox2.pack(anchor='w', pady=5)

remove_button = tk.Button(window, text="Remove", command=remove_variable)
remove_button.pack(anchor='w', pady=5)

model_label = tk.Label(window, text="Select model:")
model_label.pack(anchor='w', pady=5)

model_var = tk.StringVar(window)
model_combobox = Combobox(window, textvariable=model_var, state="readonly")
model_combobox['values'] = ["Linear Regression", "Logistic Regression", "K-Nearest Neighbors (KNN)"]
model_combobox.pack(anchor='w', pady=5)

selected_label = tk.Label(window, text="")
selected_label.pack(anchor='w', pady=5)

status_label = tk.Label(window, text="")
status_label.pack(anchor='w', pady=5)

display_button = tk.Button(window, text="Execute", command=execute)
display_button.pack(anchor='w', pady=5)


# Tracking changes in the target variable selection
target_var.trace("w", update_input_options)

# Run the application
window.mainloop()
