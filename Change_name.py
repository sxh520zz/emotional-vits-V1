import os
import shutil

def extract_copy_and_update(file_path, destination_folder, updated_file_path):
    # 创建目标文件夹，如果不存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # 打开原始文件，准备读取和写入新文件
    with open(file_path, 'r') as infile, open(updated_file_path, 'w') as outfile:
        for line in infile:
            # 提取每行的第一个字段（文件路径）和其他内容
            parts = line.strip().split('|')
            original_path = parts[0]
            other_content = '|'.join(parts[1:])

            # 确定新的文件路径
            file_name = os.path.basename(original_path)
            new_path = os.path.join(destination_folder, file_name)

            # 复制文件到目标文件夹
            if os.path.exists(original_path):
                shutil.copy(original_path, new_path)
                print(f"Copied: {original_path} to {new_path}")
            else:
                print(f"File not found: {original_path}")
                continue  # 跳过不存在的文件

            # 写入新文件的内容
            updated_line = f"{new_path}|{other_content}\n"
            outfile.write(updated_line)

    print(f"Updated file saved to: {updated_file_path}")

# 示例调用
source_file = '/home/Shi22/nas01home/Conference/TTS_EMO/emotional-vits-main-ESD-E2V/filelists/test.txt'  # 替换为您的实际文件路径
destination_dir = '/home/Shi22/nas01home/Conference/TTS_EMO/emotional-vits-main-ESD-E2V/test_wav'  # 替换为目标文件夹路径
updated_txt = '/home/Shi22/nas01home/Conference/TTS_EMO/emotional-vits-main-ESD-E2V/filelists//updated_test.txt'  # 替换为新生成的 txt 文件路径

extract_copy_and_update(source_file, destination_dir, updated_txt)


