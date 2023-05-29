import os
import shutil


def show_command_list():
    print("\033[94mList of commands:\n",
          "\033[34ma - \033[37mAdd a folder to explore\n",
          "\033[34md - \033[37mDelete selected file/folder\n",
          "\033[34mg - \033[37mShow disk-usage analysis\n",
          "\033[34mh - \033[37mShow list of commands\n",
          "\033[34mq - \033[37mQuit")


def remove_files(path):
    print("\033[94mDelete this file(s)?\033[37m")
    files, dirs = [], []
    for root, dirs, files in os.walk(path):
        break
    for file in files:
        print(file)
    for directory in dirs:
        print(directory)
    print("\033[31m'y' - yes\n'n' - no")
    accept = input("Answer: \033[37m")

    while (accept != 'y') and (accept != 'n'):
        print(f"\033[31mError: no answer - {accept}")
        print("\033[94mDelete this file(s)?")
        for file in files:
            print(file)
        for directory in dirs:
            print(directory)
        print("\033[31m'y' - yes\n'n' - no")
        accept = input("Answer: \033[37m")

    if accept == 'y':
        for root, dirs, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))
            for directory in dirs:
                shutil.rmtree(os.path.join(root, directory))
        print("\033[93mSuccessfully cleaned!")


class Cleaner:
    def __init__(self):
        self.units = ["B", "KB", "MB", "GB", "TB"]

    def convert_file_size(self, size: int) -> str:
        index = 0
        while size >= 1024 and index < len(self.units)-1:
            index += 1
            size /= 1024
        return f"{size:.2f} {self.units[index]}"

    def disk_memory(self):
        DiskUsage = shutil.disk_usage(os.path.expanduser('~'))
        print("\033[94mDisk usage analysis:\n",
              "\033[34mTotal: \033[37m", f"{self.convert_file_size(DiskUsage.total)}\n",
              "\033[34mUsed: \033[37m", f"{self.convert_file_size(DiskUsage.used)}\n",
              "\033[34mFree: \033[37m", f"{self.convert_file_size(DiskUsage.free)}")

    def get_directory_sizes(self, path='.'):
        result = []
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    result.append(
                        f"{entry.name}: {self.convert_file_size(entry.stat().st_size)}")
                elif entry.is_dir():

                    size = self._get_directory_size(entry.path)
                    result.append(
                        f"{entry.name}: {self.convert_file_size(size)}")
        return result

    def _get_directory_size(self, path):
        total = 0
        with os.scandir(path) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self._get_directory_size(entry.path)
        return total


if __name__ == '__main__':
    cleaner = Cleaner()
    show_command_list()

    command = input("\033[32mEnter a command: \033[37m")
    while command != 'q':
        if command == 'a':
            folder = input(
                "\033[92mInput a path of folder/file to explore: \033[37m")
            if os.path.isfile(folder) or os.path.isdir(folder):
                print('\n'.join(cleaner.get_directory_sizes(folder)))
            else:
                print(f"\033[31mError: no file/folder - {folder}")
            command = input("\033[32mEnter a command: \033[37m")
        elif command == 'd':
            folder = input("\033[92mInput a path of folder/file to delete: ")
            if os.path.isfile(folder) or os.path.isdir(folder):
                remove_files(folder)
            else:
                print(f"\033[31mError: no file/folder - {folder}")
            command = input("\033[32mEnter a command: \033[37m")
        elif command == 'g':
            cleaner.disk_memory()
            command = input("\033[32mEnter a command: \033[37m")
        elif command == 'h':
            show_command_list()
            command = input("\033[32mEnter a command: \033[37m")
        else:
            print(f"\033[31mError: no command - {command}")
            command = input("\033[32mEnter a command: \033[37m")
    exit(0)
