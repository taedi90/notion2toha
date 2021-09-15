import pytz

def init():
    global TIME_ZONE
    TIME_ZONE = pytz.timezone('Asia/Seoul')

    global mattersForm
    mattersForm = ['title', 'category', 'date', 'description', 'hero', 'tags', 'weight']

    # 줄 간격
    global LINE_SPACE
    LINE_SPACE = 3

    # 저장경로(없을 경우 ""로)
    global PROJECT_PATH
    PROJECT_PATH = "/Users/taedi/taedi90.github.io"
    # PROJECT_PATH = ''