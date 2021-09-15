from datetime import datetime
import re
import settings
import os
import urllib.parse
import shutil
from zipfile import ZipFile
from distutils.dir_util import copy_tree

def getMemo(zipPath):
    # 압축풀기
    unZip(zipPath)
    
    # 파일 경로 변경
    renameFiles()
    
    # 파일 읽기
    md = open(os.path.join(tempPath, 'index.md'), 'r')
    txt = md.read()
    md.close()
    
    return txt
    

def unZip(zipPath):
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.makedirs('temp')
    
    global tempPath
    tempPath = os.path.join(os.getcwd(), 'temp')
    #os.getcwd() + "/temp"
    
    with ZipFile(zipPath, "r") as zip:
        zip.extractall(path=tempPath)


def renameFiles():
    childs = os.listdir(tempPath)
    for child in childs:
        fullPath = os.path.join(tempPath, child)
        if os.path.isdir(fullPath):
            originImgDirPath = fullPath
            global originImgDirName
            originImgDirName = child
            
            global renameImgDirName
            renameImgDirName = 'images'
            renameImgDirPath = os.path.join(tempPath, renameImgDirName)
            
            os.rename(originImgDirPath, renameImgDirPath)
            
            imgs = os.listdir(renameImgDirPath)
            global imgDict
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
            # mdFileName = child
            renameMdFilePath = os.path.join(tempPath, "index.md")
            os.rename(mdFilePath, renameMdFilePath)


def getPost(txt):
    res = re.split('\n\n', txt, 2)

    dic = {}    # front matters가 입력 될 딕셔너리

    dic['title'] = res[0].replace('# ','')

    # front matters 파싱
    try:
        frontMatters = re.split('\n', res[1])
        for frontMatter in frontMatters:
            splitKv = re.split(': ', frontMatter)
            dic[splitKv[0]] = splitKv[1]  
    except IndexError:
        # 마크다운에 front matter가 없는 경우, res[1]이랑 res[2]이랑 합치기
        body = [res[1], "\n\n" ,res[2]]
        res[2] = ''.join(body)

    # 비어있는 front matter 딕셔너리에 추가
    for i in settings.mattersForm:
        if i not in dic:
            dic[i] = ''


    # 카테고리 설정
    global categories
    categories = dic['category'].split('-')

    if len(categories) >= 1:
        global name
        name = nameFix(dic['title']) 
        identifier = dic['category'] + "-" + dic['title'] 
        parent = categories[len(categories) - 1]

    # 태그 설정
    if len(dic['tags']) > 0:
        tags = "[" + dic['tags'] + "]" 
    else:
        tags = ''


    #### 본문 수정 부분
    body = ''.join(['\n',res[2]])

    # h태그 단계 낮추기(본문에 백코트가 있으면 안됨)
    # body = re.sub("(```\w[^`]*?```\n)?([^`]*?)(#\s)", r"\1\2## ", body) 
    body = re.sub("(```\w[^`]*?```\n)?([^`]*?\n)(#{1,3})\s", r"\1\2\3# ", body) 
    # 이미지 링크 수정
    
    #body = re.sub("(!\[[\w\W]+?\]\()[\w\W]+?(/[\w\W]+?)\)", 
    #            r"\1" + "image" + urllib.parse.unquote(r"\2") + ")", body) 
    # body = re.sub("!\[([\w\W]+?)\]\([\w\W]+?(/[\w\W]+?)\)", 
    #             "![" + r"\1" + "](image/" + r"\1" + ")", body) 
    
    for key, val in imgDict.items():
        originPath = urllib.parse.quote(originImgDirName + "/" + key)
        fixPath = renameImgDirName + "/" + val
        body = body.replace(originPath, fixPath)
    

    # 줄바꿈 간격 수정 (코드블럭 아래는 줄바꿈이 안됨)
    # body = re.sub("(```\w[^`]*?```\n)?([^`]*?)\n\n", r"\1\2" + ("\nㅤ  " * settings.LINE_SPACE) + "\n", body) 
    # body = re.sub("(```)\n\n", r"\1" + ("\nㅤ  " * settings.LINE_SPACE) + "\n", body) 

    merge = []

    merge.append("---\n")
    merge.append("title: " + dic['title'] + "\n")
    merge.append("date: " + strToDate(dic['date']) + "\n")
    merge.append("hero: " + dic['hero'] + "\n")
    merge.append("description: " + dic['description'] + "\n")
    merge.append("tags: " + tags + "\n")
    merge.append("menu:\n")
    merge.append("  sidebar:\n")
    merge.append("    name: " + name + "\n")
    merge.append("    identifier: " + identifier + "\n")
    merge.append("    parent: " + parent + "\n")
    merge.append("    weight: " + dic['weight'] + "\n")
    merge.append("---\n\n")
    merge.append(body)

    modify = ''.join(merge)

    return modify


def savePost(isProjectPath, path, txt):
    
    # index.md 파일 저장
    md = open(os.path.join(tempPath, 'index.md'), 'w')
    md.write(txt)
    md.close()
    
    # 프로젝트 폴더가 있으면 content 폴더 + 부모폴더에 저장
    if(isProjectPath):
        path = os.path.join(path, 'content')
        for category in categories:
            path = os.path.join(path, category)
    
    path = os.path.join(path, name)
    
    try:
        shutil.copytree(tempPath, path)
    except:
        copy_tree(tempPath, path)
    
    return path




def eraseTemp():
    if os.path.exists('temp'):
        shutil.rmtree('temp')

def strToDate(str):
    str = re.sub("오후", "PM", str)
    str = re.sub("오전", "AM", str)

    try:
        res = datetime.strptime(str, "%Y년 %m월 %d일 %p %I:%M")
    except ValueError:
        try:
            res = datetime.strptime(str, "%Y년 %m월 %d일")
        except ValueError:
            res = datetime.now()

    res = settings.TIME_ZONE.localize(res).isoformat()
    return res


### 폴더에 못쓰는 문자 변경
def nameFix(name):
    name = name.replace('\\','_')
    name = name.replace('/','_')
    name = name.replace(':','_')
    name = name.replace('*','_')
    name = name.replace('<','_')
    name = name.replace('>','_')
    name = name.replace('|','_')
    name = name.replace('-','_')
    name = name.replace('?','')
    name = name.replace('"','\'')
    
    return name
    






### 안쓰는거
def readMd(zipPath):
    # 압축풀기
    
    
    global targetDir
    targetDir = re.sub("([\w\W]*/)[^/]*", r"\1", filePath)
    with open(filePath) as f:
        txt = f.read()
    return txt


def saveMd(txt):
    # index.md 생성
    md = open(targetDir + "index.md", 'w')
    md.write(txt)
    md.close()