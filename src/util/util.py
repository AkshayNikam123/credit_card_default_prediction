import os ,sys



content = list()

def get_log_content():
    ROOT_DIR = os.getcwd()
    folder_path = os.path.join(ROOT_DIR ,"logs")
    file_name =  os.listdir(folder_path)[-1]
    file_path = os.path.join(folder_path , file_name)
    content = list()
    with open(file_path, "r") as log_file:
        for line in log_file.readlines():
            content.append(line)
    return content


