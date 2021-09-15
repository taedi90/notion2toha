from zipfile import ZipFile
import os
import shutil
import urllib.parse
import re

if os.path.exists('temp'):
    shutil.rmtree('temp')
os.makedirs('temp')

tempPath = os.getcwd() + "/temp"

with ZipFile("/Users/taedi/Downloads/GIthub 블로그 설정.zip", "r") as zip:
    zip.extractall(path=tempPath)
    


childs = os.listdir(tempPath)
for child in childs:
    fullPath = os.path.join(tempPath, child)
    if os.path.isdir(fullPath):
        originImgDirPath = fullPath
        originImgDirName = child
        
        renameImgDirName = 'images'
        renameImgDirPath = os.path.join(tempPath, renameImgDirName)
        
        os.rename(originImgDirPath, renameImgDirPath)
        
        imgs = os.listdir(renameImgDirPath)
        imgDict = {}
        idx = 1
        
        for img in imgs:
            imgExt = re.sub("[\w\W]+?(\.[\w]+?\Z)",r"\1",img)
            renameImg = "pic-{0:04d}".format(idx) + imgExt
            imgDict[img] = renameImg
            
            originImgPath = os.path.join(renameImgDirPath, img)
            renameImgPath = os.path.join(renameImgDirPath, renameImg)

            os.rename(originImgPath, renameImgPath)
            idx += 1
    else:
        mdFilePath = fullPath
        mdFileName = child


print(originImgDirName)
print(renameImgDirName)

for key, val in imgDict.items():
    print("key = {key}, value={value}".format(key=key,value=val))


# print(imgDirPath)
# print(imgDirName)
# print(mdFilePath)
# print(mdFileName)
# print(imgFileNames)
# print(urllib.parse.quote(mdFileName))

# MD파일 경로 + / + 파일명 -> 인코딩 후 변환
# 실제 파일 이름 변환 -> pic(n)포멧, md는 index로
# 전역변수 쓰지말고 그냥 함수에 값 넣어서 보내자





# shutil.rmtree('temp')
