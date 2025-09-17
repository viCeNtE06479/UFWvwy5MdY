# 代码生成时间: 2025-09-17 19:55:36
import os
from celery import Celery

# 配置Celery
app = Celery('batch_rename_tool',
             broker='pyamqp://guest@localhost//',
             backend='rpc://')

# 定义批量重命名任务
@app.task
def batch_rename(files, prefix):
    """
    批量重命名文件，每个文件名前添加指定前缀。
    
    :param files: 需要重命名的文件列表
    :param prefix: 文件名前缀
    :return: None
    """
    try:
        for file in files:
            original_path = file['path']
            file_name = file['name']
            directory = os.path.dirname(original_path)
            new_file_name = prefix + file_name
            new_path = os.path.join(directory, new_file_name)
            os.rename(original_path, new_path)
            print(f"Renamed {original_path} to {new_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# 示例使用
if __name__ == '__main__':
    # 定义文件列表和前缀
    files_to_rename = [
        {'path': '/path/to/file1.txt', 'name': 'file1.txt'},
        {'path': '/path/to/file2.txt', 'name': 'file2.txt'},
    ]
    new_prefix = 'new_'

    # 调用批量重命名任务
    batch_rename.delay(files_to_rename, new_prefix)