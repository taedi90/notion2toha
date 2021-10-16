from datetime import datetime
import re
import settings
import os
from urllib import parse
import shutil
from zipfile import ZipFile
from distutils.dir_util import copy_tree

def getMemo(filePath):
    # 임시 폴더 생성
    setTempPath()

    # 파일 확장자 확인
    ext = os.path.splitext(filePath)[1]
    if ext in '.zip':
        unZip(filePath)
    elif ext in '.md':
        copyMd(filePath)

    # 파일 이름 변경
    renameFiles()
    
    # 파일 읽기
    txt = None
    try:
        md = open(tempPath + '/index.md', 'rt', encoding='UTF8')
        txt = md.read()
        md.close()
    finally:
        return txt

def setTempPath():
    global tempPath
    # tempPath = os.path.join(os.getcwd(), 'temp')
    tempPath = settings.PROGRAM_PATH + "/temp"

    if os.path.exists(tempPath):
        shutil.rmtree(tempPath)
    os.makedirs(tempPath)
    

    
def copyMd(filePath):
    shutil.copy(filePath, tempPath)
    

def unZip(zipPath):
    with ZipFile(zipPath, "r") as zip:
        zip.extractall(path=tempPath)


def renameFiles():
    childs = os.listdir(tempPath)
    for child in childs:
        # fullPath = os.path.join(tempPath, child)
        fullPath = tempPath + "/" + child
        if os.path.isdir(fullPath):
            originImgDirPath = fullPath
            global originImgDirName
            originImgDirName = child
            
            global renameImgDirName
            renameImgDirName = 'images'
            # renameImgDirPath = os.path.join(tempPath, renameImgDirName)
            renameImgDirPath = tempPath + "/" + renameImgDirName
            
            os.rename(originImgDirPath, renameImgDirPath)
            
            imgs = os.listdir(renameImgDirPath)
            global imgDict
            imgDict = {}
            idx = 1
            
            for img in imgs:
                imgExt = re.sub("[\w\W]+?(\.[\w]+?\Z)",r"\1",img) # 확장자 가져오기
                renameImg = "pic-{0:04d}".format(idx) + imgExt # 이름 변경
                imgDict[img] = renameImg
                
                # originImgPath = os.path.join(renameImgDirPath, img)
                originImgPath = renameImgDirPath + "/" + img
                # renameImgPath = os.path.join(renameImgDirPath, renameImg)
                renameImgPath = renameImgDirPath + "/" + renameImg

                os.rename(originImgPath, renameImgPath)
                idx += 1
        else:
            if os.path.splitext(fullPath)[1] == '.md' :
                mdFilePath = fullPath
                # renameMdFilePath = os.path.join(tempPath, "index.md")
                renameMdFilePath = tempPath + "/index.md"
                os.rename(mdFilePath, renameMdFilePath)


def getPost(txt):
    res = re.split('\n\n', txt, 2)

    dic = {}    # front matters가 입력 될 딕셔너리

    dic['title'] = res[0].replace('# ','', 1)

    # front matters 파싱
    try:
        frontMatters = re.split('\n', res[1])
        for frontMatter in frontMatters:
            splitKv = re.split(': ', frontMatter)
            dic[splitKv[0]] = splitKv[1]  
    except IndexError:
        # 마크다운에 front matter가 없는 경우, 본문 다시 합치기
        body = [res[1], "\n\n" ,res[2]]
        res[2] = ''.join(body)

    # 비어있는 front matter 딕셔너리에 추가
    for i in settings.mattersForm:
        if i not in dic:
            dic[i] = ''


    # 카테고리 설정
    global categories
    categories = dic['category'].split('-')
        
        
    # name 설정
    global name
    if len(dic['name']) > 0:
        name = nameFix(dic['name'])
    else:
        name = nameFix(dic['title'])
        
    # parent & identfier 설정
    # if len(categories) >= 1:
    if categories[0] != '':
        parent = categories[len(categories) - 1]
        identifier = dic['category'] + '-' + name
    else:
        parent = dic['category']
        identifier = name



    # 태그 설정
    if len(dic['tags']) > 0:
        tags = "[" + dic['tags'] + "]" 
    else:
        tags = ''


    #### 본문 수정 부분
    body = ''.join(['\n',res[2]])

    # h태그 단계 낮추기(본문에 백코트가 있으면 안됨)
    # body = re.sub("(```\w[^`]*?```\n)?([^`]*?\n)(#{1,3})\s", r"\1\2\3# ", body) 
    
    # 줄바꿈 간격 수정 (코드블럭 아래는 줄바꿈이 안됨)
    # body = re.sub("(```\w[^`]*?```\n)?([^`]*?)\n\n", r"\1\2" + ("\nㅤ  " * settings.LINE_SPACE) + "\n", body) 
    # body = re.sub("(```)\n\n", r"\1" + ("\nㅤ  " * settings.LINE_SPACE) + "\n", body) 
    
    # 이미지 링크 수정
    if 'imgDict' in globals():
        for key, val in imgDict.items():
            originPath = parse.quote(originImgDirName + "/" + key, '/!@#$&()_-+=~\';,')
            fixPath = renameImgDirName + "/" + val
            body = body.replace(originPath, fixPath)

        
    # 줄별로 나누기
    paragraphs = body.split('\n')
    modParagraphs = []
    blockquote = 0
    quotation = 0
    
    
    # h태그 단계 낮추기
    for p in paragraphs:
        # ``` 코드블럭 확인(스페이스 제외)
        if re.match('[\s]*```', p):
            blockquote ^= 1
            
        # 코드블럭 내부인 경우 h 태그 탐색안함
        if blockquote == 1:
            modParagraphs.append(p)
            continue
        
        # > 인용문 줄바꿈 풀리는 현상(다단 인용은 처리 어려움)
        if re.match('[\s]*>' , p):
            quotation = 1
        elif quotation == 1 and re.fullmatch('', p):
            quotation = 0   # 인용문 종료
            
            
        # > 인용문 줄바꿈 처리, h 태그 탐색안함
        if quotation == 1:
            modParagraphs.append(p + '  ')
            continue
        
        # h1 ~ h5 태그 hn + 1 태그로 바꾸기
        if re.match('[\s]*#{1,5}\s', p):
            p = re.sub('([\s]*#{1,5})\s',r'\1# ', p) 
        
        # h6 태그는 볼드체로 수정
        elif re.match('[\s]*#{6}\s', p):
            p = re.sub('([\s]*)#{6}\s([\W\w]*)',r'** \1\2 **', p)         
            
        # 문장을 리스트에 추가
        modParagraphs.append(p)
            
    # 줄별로 합치기
    modBody = '\n'.join(modParagraphs)
    


    # front matters 입력 및 본문 병합
    merge = []

    merge.append("---\n")
    merge.append("title: \"" + dic['title'] + "\"\n")
    merge.append("date: " + strToDate(dic['date']) + "\n")
    merge.append("lastmod: " + strToDate(dic['lastmod']) + "\n")
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
    merge.append(modBody)

    modify = ''.join(merge)

    return modify


def savePost(isProjectPath, path, txt):
    
    # index.md 파일 저장
    # md = open(os.path.join(tempPath, 'index.md'), 'w', encoding='UTF8')
    md = open(tempPath + '/index.md', 'wt', encoding='UTF8')
    md.write(txt)
    md.close()
    
    # 프로젝트 폴더가 있으면 content 폴더 + 부모폴더에 저장
    if(isProjectPath):
        # path = os.path.join(path, 'content')
        # path = os.path.join(path, 'posts')
        path = path + '/content/posts'
        postsPath = path # _index.md 생성용도
        for category in categories:
            # path = os.path.join(path, category)
            path = path + '/' + category
    
    # path = os.path.join(path, name)
    path = path + '/' + name
    
    try:
        shutil.copytree(tempPath, path)
    except:
        copy_tree(tempPath, path)
        
    # 부모폴더에 _index.md 만들기
    if(isProjectPath):
        for category in categories:
            # postsPath = os.path.join(postsPath, category)
            postsPath = postsPath + '/' + category
            # mdFile = os.path.join(postsPath, "index.md")
            index1 = postsPath + "/index.md"
            index2 = postsPath + "/_index.md"
            if not os.path.isfile(index1) and not os.path.isfile(index2):
                # md = open(os.path.join(postsPath, '_index.md'), 'w', encoding='UTF8')
                md = open(postsPath + '/_index.md', 'wt', encoding='UTF8')
                md.write(getIndexMd(category))
                md.close()
                
    return path

# _index.md 문구 생성
def getIndexMd(category):
    idx = categories.index(category)
    
    merge = []

    merge.append("---\n")
    merge.append("title: " + category + "\n")
    merge.append("menu:\n")
    merge.append("  sidebar:\n")
    merge.append("    name: " + category + "\n")
    merge.append("    identifier: " + category + "\n")
    
    if idx > 0:
        merge.append("    parent: " + categories[idx - 1] + "\n")
        
    merge.append("    weight: 10\n")
    merge.append("---\n\n")
    
    txt = ''.join(merge)
    
    return txt
    


def eraseTemp():
    try:
        shutil.rmtree(tempPath)
    finally:
        return

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


### 폴더, front matter에 사용하지 못하는 문자 수정
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
    name = name.replace('[','(')
    name = name.replace(']',')')
    
    return name
    
