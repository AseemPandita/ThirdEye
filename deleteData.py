import os
import glob

def deleteData():
  filesList = glob.glob('data/*.jpg')
  numberOfFiles = len(filesList)
  for file in filesList:
    print(file)
    os.remove(file)
  updatedNumberOfFiles = len(glob.glob('data/*.jpg'))
  return (numberOfFiles - updatedNumberOfFiles) == 0

if __name__ == "__main__":
  deleteData()