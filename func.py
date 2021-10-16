from datetime import datetime
import re
import settings
import os
from urllib import parse
import shutil
from zipfile import ZipFile
from distutils.dir_util import copy_tree

def get_memo(file_path):
    # 임시 폴더 생성
    set_temp_path()

    # 파일 확장자 확인
    ext = os.path.splitext(file_path)[1]
    if ext in '.zip':
        un_zip(file_path)
    elif ext in '.md':
        copy_md(file_path)

    # 파일 이름 변경
    rename_files()
    
    # 파일 읽기
    txt = None
    try:
        md = open(temp_path + '/index.md', 'rt', encoding='UTF8')
        txt = md.read()
        md.close()
    finally:
        return txt

def set_temp_path():
    global temp_path
    # temp_path = os.path.join(os.getcwd(), 'temp')
    temp_path = settings.PROGRAM_PATH + "/temp"

    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
    os.makedirs(temp_path)
    

    
def copy_md(file_path):
    shutil.copy(file_path, temp_path)
    

def un_zip(zip_path):
    with ZipFile(zip_path, "r") as zip:
        zip.extractall(path=temp_path)


def rename_files():
    childs = os.listdir(temp_path)
    for child in childs:
        # full_path = os.path.join(temp_path, child)
        full_path = temp_path + "/" + child
        if os.path.isdir(full_path):
            origin_img_dir_path = full_path
            global origin_img_dir_name
            origin_img_dir_name = child
            
            global rename_img_dir_name
            rename_img_dir_name = 'images'
            # rename_img_dir_path = os.path.join(temp_path, rename_img_dir_name)
            rename_img_dir_path = temp_path + "/" + rename_img_dir_name
            
            os.rename(origin_img_dir_path, rename_img_dir_path)
            
            imgs = os.listdir(rename_img_dir_path)
            global img_dict
            img_dict = {}
            idx = 1
            
            for img in imgs:
                img_ext = re.sub("[\w\W]+?(\.[\w]+?\Z)",r"\1",img) # 확장자 가져오기
                rename_img = "pic-{0:04d}".format(idx) + img_ext # 이름 변경
                img_dict[img] = rename_img
                
                # originImgPath = os.path.join(rename_img_dir_path, img)
                originImgPath = rename_img_dir_path + "/" + img
                # rename_imgPath = os.path.join(rename_img_dir_path, rename_img)
                rename_imgPath = rename_img_dir_path + "/" + rename_img

                os.rename(originImgPath, rename_imgPath)
                idx += 1
        else:
            if os.path.splitext(full_path)[1] == '.md' :
                mdfile_path = full_path
                # rename_mdfile_path = os.path.join(temp_path, "index.md")
                rename_mdfile_path = temp_path + "/index.md"
                os.rename(mdfile_path, rename_mdfile_path)


def get_post(txt):
    res = re.split('\n\n', txt, 2)

    dic = {}    # front matters가 입력 될 딕셔너리

    dic['title'] = res[0].replace('# ','', 1)

    # front matters 파싱
    try:
        front_matters = re.split('\n', res[1])
        for front_matter in front_matters:
            split_kv = re.split(': ', front_matter)
            dic[split_kv[0]] = split_kv[1]  
    except IndexError:
        # 마크다운에 front matter가 없는 경우, 본문 다시 합치기
        body = [res[1], "\n\n" ,res[2]]
        res[2] = ''.join(body)

    # 비어있는 front matter 딕셔너리에 추가
    for i in settings.matters_form:
        if i not in dic:
            dic[i] = ''


    # 카테고리 설정
    global categories
    categories = dic['category'].split('-')
        
        
    # name 설정
    global name
    if len(dic['name']) > 0:
        name = name_fix(dic['name'])
    else:
        name = name_fix(dic['title'])
        
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
    if 'img_dict' in globals():
        for key, val in img_dict.items():
            origin_path = parse.quote(origin_img_dir_name + "/" + key, '/!@#$&()_-+=~\';,')
            fix_path = rename_img_dir_name + "/" + val
            body = body.replace(origin_path, fix_path)

        
    # 줄별로 나누기
    paragraphs = body.split('\n')
    mod_paragraphs = []
    blockquote = 0
    quotation = 0
    
    
    # h태그 단계 낮추기
    for p in paragraphs:
        # ``` 코드블럭 확인(스페이스 제외)
        if re.match('[\s]*```', p):
            blockquote ^= 1
            
        # 코드블럭 내부인 경우 h 태그 탐색안함
        if blockquote == 1:
            mod_paragraphs.append(p)
            continue
        
        # > 인용문 줄바꿈 풀리는 현상(다단 인용은 처리 어려움)
        if re.match('[\s]*>' , p):
            quotation = 1
        elif quotation == 1 and re.fullmatch('', p):
            quotation = 0   # 인용문 종료
            
            
        # > 인용문 줄바꿈 처리, h 태그 탐색안함
        if quotation == 1:
            mod_paragraphs.append(p + '  ')
            continue
        
        # h1 ~ h5 태그 hn + 1 태그로 바꾸기
        if re.match('[\s]*#{1,5}\s', p):
            p = re.sub('([\s]*#{1,5})\s',r'\1# ', p) 
        
        # h6 태그는 볼드체로 수정
        elif re.match('[\s]*#{6}\s', p):
            p = re.sub('([\s]*)#{6}\s([\W\w]*)',r'** \1\2 **', p)         
            
        # 문장을 리스트에 추가
        mod_paragraphs.append(p)
            
    # 줄별로 합치기
    mod_body = '\n'.join(mod_paragraphs)
    


    # front matters 입력 및 본문 병합
    merge = []

    merge.append("---\n")
    merge.append("title: \"" + dic['title'] + "\"\n")
    merge.append("date: " + str_to_date(dic['date']) + "\n")
    merge.append("lastmod: " + str_to_date(dic['lastmod']) + "\n")
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
    merge.append(mod_body)

    modify = ''.join(merge)

    return modify


def save_post(is_project_path, path, txt):
    
    # index.md 파일 저장
    # md = open(os.path.join(temp_path, 'index.md'), 'w', encoding='UTF8')
    md = open(temp_path + '/index.md', 'wt', encoding='UTF8')
    md.write(txt)
    md.close()
    
    # 프로젝트 폴더가 있으면 content 폴더 + 부모폴더에 저장
    if(is_project_path):
        # path = os.path.join(path, 'content')
        # path = os.path.join(path, 'posts')
        path = path + '/content/posts'
        posts_path = path # _index.md 생성용도
        for category in categories:
            # path = os.path.join(path, category)
            path = path + '/' + category
    
    # path = os.path.join(path, name)
    path = path + '/' + name
    
    try:
        shutil.copytree(temp_path, path)
    except:
        copy_tree(temp_path, path)
        
    # 부모폴더에 _index.md 만들기
    if(is_project_path):
        for category in categories:
            # posts_path = os.path.join(posts_path, category)
            posts_path = posts_path + '/' + category
            # mdFile = os.path.join(posts_path, "index.md")
            index1 = posts_path + "/index.md"
            index2 = posts_path + "/_index.md"
            if not os.path.isfile(index1) and not os.path.isfile(index2):
                # md = open(os.path.join(posts_path, '_index.md'), 'w', encoding='UTF8')
                md = open(posts_path + '/_index.md', 'wt', encoding='UTF8')
                md.write(get_index_md(category))
                md.close()
                
    return path

# _index.md 문구 생성
def get_index_md(category):
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
    


def erase_temp():
    try:
        shutil.rmtree(temp_path)
    finally:
        return

def str_to_date(str):
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
def name_fix(name):
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
    
