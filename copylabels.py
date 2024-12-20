# 写入标签到文件
def write_labels_to_file(labels, file_path):
    with open(file_path, 'w') as file:
        for label in labels:
            file.write(str(label) + '\n')

# 从文件中读取标签
def read_labels_from_file(file_path):
    labels = []
    with open(file_path, 'r') as file:
        for line in file:
            labels.append(line.strip())
    return labels

'''
# 将标签写入文件
write_labels_to_file(generated_labels, "generated_labels.txt")

# 从文件中读取标签
read_labels = read_labels_from_file("generated_labels.txt")
print(read_labels)
'''