from os import path
from shutil import make_archive
from zipfile import ZipFile
from helpers import Helpers




def make_zip_file():
    zip_path = Helpers.zip_file_path
    files_directory = "./data/covers/"
    make_archive(f'{Helpers.zip_file_path}covers', 'zip', files_directory)
    
# with ZipFile(f"{zip_path}zipfile.zip", 'w') as zip_file:
#   zip_file.write()