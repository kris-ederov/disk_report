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
    if n > 0:
        if file_bytes >= 100: return '{:0.0f}'.format(file_bytes) + power_labels[n]
        if file_bytes >= 10: return '{:0.1f}'.format(file_bytes) + power_labels[n]
        else: return '{:0.2f}'.format(file_bytes) + power_labels[n]
    else: return str(file_bytes) + power_labels[n]

def FolderSize(folder_path):
    # Input: folder path
    # Output: folder size in bytes

    #Exit if given path is not a folder
    if os.path.isfile(folder_path): return "FolderSize error - not a folder"

    folder_size = 0
    for root, list_folders, list_files in os.walk(folder_path):
        for file_name in list_files: 
            folder_size += os.path.getsize(os.path.join(root, file_name))

    return folder_size

def ScanFolder(path_main, limit_list_flag):
    # Input: folder url, boolean controlling if small sizes will be omitted
    # Return: list with tuples of each files/folder names and its size

    # Exit if given path is not a folder
    if os.path.isfile(path_main): return "ScanFolder error - not a folder"
    if type(limit_list_flag) is not bool: return "ScanFolder error - limit_list_flag needs to be a bool"

    #Build list of all files and folders in given path
    path_main = Path(path_main)
    try: list_files = os.listdir(path_main)
    except: return [], [], []
    if not list_files: return ["_Empty_"], [0], ["N/A"]
    list_urls = [ path_main / x for x in list_files ]

    #Build a list of sizes for each file/folder
    list_sizes = []
    for file_url in list_urls:
        if os.path.isfile(file_url):
            list_sizes.append(os.path.getsize(file_url))
        else:
            list_sizes.append(FolderSize(file_url))

    #Sort items through a dictionnary
    dict_files = []
    for index, file in enumerate(list_files):
        dict_files.append(tuple(['{:.50}'.format(file), list_sizes[index], list_urls[index]]))
    dict_files.sort(key = lambda item: item[1], reverse=True)

    #Filter out small items
    total_size = sum(list_sizes)
    count_size = 0
    sorted_list_files = []
    sorted_list_sizes = []
    sorted_list_urls = []
    # for item in dict_files:
    #     sorted_list_files.append(item[0])
    #     sorted_list_sizes.append(item[1])
    #     sorted_list_urls.append(item[2])
    #     count_size += item[1]
    #     if total_size > 0:
    #         if limit_list_flag and count_size/total_size > .95 and len(sorted_list_files) < len(list_sizes):
    #             sorted_list_files.append("_REMAINING FILES_")
    #             sorted_list_sizes.append(total_size - count_size)
    #             sorted_list_urls.append("N/A")
    #             break

    # Combine all files less than 2% of the total size
    for item in dict_files:
        if total_size > 0:
            if limit_list_flag and item[1]/total_size < .025:
                sorted_list_files.append("- REMAINING FILES -")
                sorted_list_sizes.append(total_size - count_size)
                sorted_list_urls.append("N/A")
                break
        sorted_list_files.append(item[0])
        sorted_list_sizes.append(item[1])
        sorted_list_urls.append(item[2])
        count_size += item[1]

    return sorted_list_files, sorted_list_sizes, sorted_list_urls

if __name__ == "__main__":
    stest = r"C:\Users\krissay\Documents\My Music"
    stest2 = r"D:\Downloads"
    stest3 = r"E:"

    list_files, list_sizes, list_urls = ScanFolder(stest, False)
    print("\n")
    for file, size, url in zip(list_files, list_sizes, list_urls):
        print(file + " - " + FormatSize(size))
        print(url)
