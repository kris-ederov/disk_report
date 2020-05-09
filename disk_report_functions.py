import os, pickle
from pathlib import Path

def FormatSize(file_bytes):
    """Format integer bytes to KB/MB/GB"""
    power = 2**10
    n = 0
    power_labels = [' B', ' KB', ' MB', ' GB', ' TB']
    
    while file_bytes > power:
        file_bytes /= power
        n += 1
    if n > 0:
        if file_bytes >= 100: return '{:0.0f}'.format(file_bytes) + power_labels[n]
        if file_bytes >= 10: return '{:0.1f}'.format(file_bytes) + power_labels[n]
        else: return '{:0.1f}'.format(file_bytes) + power_labels[n]
    else: return str(file_bytes) + power_labels[n]

class FilesData:
    """ Data structure: [file index, file url, size, list with file indices contained in folder] """
    def __init__(self, path_main):
        self.init(path_main)

    def init(self, path_main):
        self.path_main = Path(path_main)
        self.list_files = []
        self.files_count = 0

        if os.path.isdir(self.path_main):
            self.list_files.append([self.files_count, self.path_main, -1, []])
            self.files_count += 1
            self.list_files[0][2], self.list_files[0][3] = self.ScanFolder(self.path_main)
        else:
            self.OpenScan(path_main)
            self.files_count = len(self.list_files)

    def SaveTo(self, save_path):
        outfile = open(save_path, "wb")
        pickle.dump(self.list_files, outfile)
        outfile.close()

    def OpenScan(self, open_path):
        infile = open(open_path, "rb")
        self.list_files = pickle.load(infile)
        infile.close()

    def ScanFolder(self, cur_path):
        cur_path = Path(cur_path)
        #Generate list of files for current dir
        folder_contents_temp = []
        try: temp_list = os.listdir(cur_path)
        except: return 0, folder_contents_temp

        cur_folder_size = 0

        # Go through each item in the list
        for item in temp_list:
            item = cur_path / item

            if os.path.isfile(item):
                item_size = os.path.getsize(item)
                self.list_files.append([self.files_count, item, item_size])
                cur_folder_size += item_size
            else:
                self.list_files.append([self.files_count, item, -1, []])

            folder_contents_temp.append(self.files_count)

            # temp_index, temp_size and cur_folder_size used to sum folder size
            temp_index = self.files_count

            self.files_count += 1

            if os.path.isdir(item):
                temp_size, folder_contents_sum = self.ScanFolder(item)
                cur_folder_size += temp_size
                self.list_files[temp_index][2] = temp_size
                self.list_files[temp_index][3] = folder_contents_sum
        
        return cur_folder_size, folder_contents_temp

    def MainFolderPath(self):
        return self.list_files[0][1]

    def MainFolderSize(self):
        return self.list_files[0][2]

    def PrintAllContents(self):
        for item in self.list_files: print(item)

    def FolderContents(self, path_folder, limit_list_flag, limit_filename_flg):
        """ Returns lists file names, sizes and url contained path_folder """
        if not path_folder: path_folder = self.MainFolderPath()
        path_folder = Path(path_folder)
        for item in self.list_files:
            if path_folder == item[1]:
                index_path_folder = item[0]
                list_urls = [str(self.list_files[x][1]) for x in self.list_files[index_path_folder][3]]
                list_sizes = [self.list_files[x][2] for x in self.list_files[index_path_folder][3]]

                list_urls, list_sizes = self.SortFiles(list_urls, list_sizes, limit_list_flag)
                
                if limit_filename_flg: list_filenames = ['{:.50}'.format(os.path.basename(x)) for x in list_urls]
                else: list_filenames = [os.path.basename(x) for x in list_urls]

                return list_filenames, list_sizes, list_urls

        return ["not found"], [0], ["N/A"]

    def SortFiles(self, list_items, list_sizes, limit_list_flag):
        #Sort items through a dictionnary
        dict_files = []

        for index, file in enumerate(list_items):
            # dict_files.append(tuple(['{:.50}'.format(file), list_sizes[index]]))
            dict_files.append(tuple([file, list_sizes[index]]))
        dict_files.sort(key = lambda item: item[1], reverse=True)

        #Filter out small items
        total_size = sum(list_sizes)
        count_size = 0
        sorted_list_items = []
        sorted_list_sizes = []

        # Combine all files less than 2% of the total size
        for item in dict_files:
            if total_size > 0:
                if limit_list_flag and item[1]/total_size < .025:
                    sorted_list_items.append("- REMAINING FILES -")
                    sorted_list_sizes.append(total_size - count_size)
                    break
            sorted_list_items.append(item[0])
            sorted_list_sizes.append(item[1])
            count_size += item[1]

        return sorted_list_items, sorted_list_sizes

if __name__ == "__main__":
    stest = r"C:\Users\krissay\Documents"
    stest2 = r"D:\Downloads"
    stest3 = r"E:\Google Drive"
    stest4 = "C:\\"

    # RootFolder = FilesData(stest)
    RootFolder = FilesData(r"C:\Users\krissay\Desktop\saved_scan.txt")

    list_filenames, list_sizes, list_urls = RootFolder.FolderContents("", False, False)

    for index, item in enumerate(list_filenames):
        print(item + " - " + FormatSize(list_sizes[index]) + " - " + list_urls[index])

    # RootFolder.SaveTo(r"C:\Users\krissay\Desktop\saved_scan.txt")
    