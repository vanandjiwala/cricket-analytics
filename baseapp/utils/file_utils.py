import os
import glob

class FileUtils:

    @staticmethod
    def list_files(dir: str, file_extension: str = "*") -> list:
        """
        Get list of files or list of files for a perticular file extension
        :param dir: Base directoy
        :param file_extension: file type/extension
        :return: list of files
        """
        dir_path = os.path.join(dir, f"*.{file_extension.lower()}")
        files_list = glob.glob(dir_path)
        return files_list

    @staticmethod
    def create_dir_if_not_exist(dir_path: str):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)