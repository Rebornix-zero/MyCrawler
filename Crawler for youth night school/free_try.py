import pandas as pd

# 创建数据框
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'San Francisco', 'Chicago']
}

df = pd.DataFrame(data)

# 指定要写入的 CSV 文件名
csv_file = 'aligned_data.csv'

# 将数据框格式化为字符串并写入 CSV 文件
formatted_data = df.to_string(index=False)
with open(csv_file, 'w') as file:
    file.write(formatted_data)

print("CSV 文件写入完成，并已对齐.")

