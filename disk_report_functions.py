import os
from pathlib import Path

def FormatSize(file_bytes):
    # Input: # of bytes
    # Output: # converted to KB/MB/GB with suffix
    power = 2**10
    n = 0
    power_labels = [' B', ' KB', ' MB', ' GB', ' TB']
    
    while file_bytes > power:
        file_bytes /= power
        n += 1
    if n > 1: return '{:0.2f}'.format(file_bytes) + power_labels[n]
    else: return str(file_bytes) + power_labels[n]

def FolderSize(folder_path):
    # Input: folder path
    # Output: folder size in bytes
    if os.path.isfile(folder_path): return "FolderSize error - not a folder"

    folder_size = 0
    for root, list_folders, list_files in os.walk(folder_path):
        for file_name in list_files: folder_size += os.path.getsize(os.path.join(root, file_name))

    return folder_size

def ScanFolder(path_main):
    # Input: folder url
    # Return: list with tuples of each files/folder names and its size
    if os.path.isfile(path_main): return "ScanFolder error - not a folder"

    path_main = Path(path_main)
    list_files = os.listdir(path_main)
    list_files_url = [ path_main / x for x in list_files ]

    list_sizes = []
    for file_url in list_files_url:
        if os.path.isfile(file_url):
            list_sizes.append(os.path.getsize(file_url))
        else:
            list_sizes.append(FolderSize(file_url))

    dict_files = []
    for index, file in enumerate(list_files):
        dict_files.append(tuple(['{:.50}'.format(file), list_sizes[index]]))
    dict_files.sort(key = lambda item: item[1], reverse=True)

    for index, item in enumerate(dict_files):
        list_files[index] = item[0]
        list_sizes[index] = item[1]

    # return dict_files
    return list_files, list_sizes

if __name__ == "__main__":
    stest = r"C:\Users\krissay\Desktop\test"
    stest2 = r"D:\Downloads"
    stest3 = r"E:"

    list_files, list_sizes = ScanFolder(stest2)
    print("\n")
    for file, size in zip(list_files, list_sizes):
        print(file + " - " + FormatSize(size))
