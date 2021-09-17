import pytz

def init():
    # 타임존 설정
    global TIME_ZONE
    TIME_ZONE = pytz.timezone('Asia/Seoul')

    # front matters 항목
    global mattersForm
    mattersForm = ['title', 'category', 'date', 'description', 'hero', 'tags', 'weight']

    # 줄 간격
    # global LINE_SPACE
    # LINE_SPACE = 3

    # 프로젝트 경로(경로는 \ 말고 /로 구분)
    global PROJECT_PATH
    
    PROJECT_PATH = "/Users/taedi/taedi90.github.io"
    
    # 프로젝트 경로를 ''으로 설정해둘 경우 저장시마다 저장 위치 확인
    # PROJECT_PATH = ''
