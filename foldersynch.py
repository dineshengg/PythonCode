from os import path
from os import listdir, makedirs
import sys

class Folder(object):
    def __init__(self):
        pass        
        
    
    def copy_files(self, srcFolder, destFolder):
        if not path.exists(destFolder):
            makedirs(destFolder)

        if not path.exists(srcFolder):        
            raise FileNotFoundError(f"Source folder '{cls.srcFolder}' does not exist.")

        for filename in listdir(srcFolder):
            srcPath = path.join(srcFolder, filename)
            desPath = path.join(destFolder, filename)
            #for file copy
            if path.isfile(srcPath):
                if not path.exists(desPath):
                    print(f"copying from {srcPath} to {desPath}")
                    self.write_file(srcPath, desPath)
                    
                else:
                    print(f"file {filename} already exists at destination {destFolder}")
            #for directory copy
            else:
                if not path.exists(desPath):
                    makedirs(desPath)
                self.copy_files(srcPath, desPath)             
                
    
    def write_file(self, srcPath, desPath):
        with open(srcPath, "rb") as srcFile:
            with open(desPath, "wb") as desFile:
                desFile.write(srcFile.read())


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Expecting two command line arguments source folder and destination folder")
    else:
        folder = Folder()
        folder.copy_files(sys.argv[1], sys.argv[2])