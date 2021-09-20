import configparser
import pytz
import os

def init():
    # 타임존 설정
    global TIME_ZONE
    TIME_ZONE = pytz.timezone('Asia/Seoul')

    # front matters 항목
    global mattersForm
    mattersForm = ['title', 'category', 'name', 'date', 'lastmod', 'description', 'hero', 'tags', 'weight']

    # 줄 간격
    # global LINE_SPACE
    # LINE_SPACE = 3

    # 프로젝트 경로(경로는 \ 말고 /로 구분)
    # 프로젝트 경로를 ''으로 설정해둘 경우 저장시마다 저장 위치 확인
    global PROJECT_PATH
    PROJECT_PATH = ''
    
    # 프로그램 경로
    global PROGRAM_PATH
    PROGRAM_PATH = os.path.dirname(os.path.abspath(__file__))
    
    # config.ini 경로
    global CONF_PATH
    CONF_PATH = PROGRAM_PATH + '/config.ini'
    
    config = configparser.ConfigParser()
    config.read(CONF_PATH)
    PROJECT_PATH = config['DEFAULT'].get('projectPath', fallback='')

def readIni():
    config = configparser.ConfigParser()
    config.read(CONF_PATH)
    PROJECT_PATH = config['DEFAULT'].get('projectPath', fallback='')
    
def writeIni():
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'projectPath': PROJECT_PATH}
    with open(CONF_PATH, 'w') as configfile:
        config.write(configfile)