from glob import glob
from os.path import isdir
from notion.client import *
from notion.block import *

# 개발자도구 > 애플리케이션 > 쿠키 > token_v2의 값
token = ""
# 해당 노션 url
url = ""

client = NotionClient(token_v2=token)
page = client.get_block(url)


# todo
# 0. 한글 지원이 안되서 fileread에 "utf-8" 조정, 이미지 저장이 안되서 try 사용, 개행 이슈가 있음
# 1. 딕셔너리로 언어에 따라 prefix를 자동 조정
# 2. 깊이가 2단계인데 필요시 전체 폴더로 조정 (우선순위 낮음)
# 3. 코드블록의 개행 해결 필요
확장자언어매핑 = {
    '.py': 'python',
    '.js': 'javascript',
    '.json': 'json',
    '.html': 'html',
    '.css': 'css',
    '.scss': 'sass',
    '.md': 'markdown',
    '.txt': 'plain text'
}

주석prefix매핑 = {
    '.py': '#/#/#',
    '.js': '//',
    '.json': '//',
    '.html': '',
    '.css': '//',
    '.scss': '',
    '.md': '',
    '.txt': '//'
}

# notion에서 공백처리를 html로 함.
# 일반 공백으로 하면 개행 후 들여쓰기 손실 생김.
공백prefix매핑 = {
    '.py': '&nbsp;',
    '.js': '&nbsp;',
    '.json': '&nbsp;',
    '.html': '&nbsp;',
    '.css': '&nbsp;',
    '.scss': '&nbsp;',
    '.md': ' ',
    '.txt': ' '
}

주석prefix = '//'
언어 = 'javascript'

for title in glob('*'):
    if isdir(title):
        childblock = page.children.add_new(PageBlock)
        childblock.title = title
        childblock.icon = "📝"
        for title2 in glob(f'{title}/*'):
            if isdir(title2):
                childblock2 = childblock.children.add_new(PageBlock)
                childblock2.title = title2
                childblock2.icon = "📝"
                for title3 in glob(f'{title2}/*'):
                    print(title3)
                    if not isdir(title3):
                        try:
                            확장자 = os.path.splitext(title3)[1]
                            f = open(title3, 'rt', encoding="utf-8")
                            data = f.read()
                            f.close()
                            data = data.replace(' ', 공백prefix매핑.get(확장자, " "))
                            codeblockinpage = childblock2.children.add_new(
                                CodeBlock)
                            codeblockinpage.title = f'{주석prefix매핑.get(확장자, "")} 파일이름 : {title3} \n\n{data}'
                            codeblockinpage.wrap = True
                            codeblockinpage.language = 확장자언어매핑.get(
                                확장자, 'plain text')
                        except:
                            print('error', 확장자)
            else:
                try:
                    확장자 = os.path.splitext(title2)[1]
                    f = open(title2, 'rt', encoding="utf-8")
                    data = f.read()
                    f.close()
                    data = data.replace(' ', 공백prefix매핑.get(확장자, " "))
                    codeblockinpage = childblock.children.add_new(CodeBlock)
                    codeblockinpage.title = f'{주석prefix매핑.get(확장자, "")} 파일이름 : {title2} \n\n{data}'
                    codeblockinpage.wrap = True
                    codeblockinpage.language = 확장자언어매핑.get(확장자, 'plain text')
                except:
                    print('error', 확장자)
    else:
        try:
            확장자 = os.path.splitext(title)[1]
            f = open(title, 'rt', encoding="utf-8")
            data = f.read()
            f.close()
            print(확장자)
            print(주석prefix매핑.get(확장자, ""))
            data = data.replace(' ', 공백prefix매핑.get(확장자, " "))
            codeblockinpage = page.children.add_new(CodeBlock)
            # print(주석prefix매핑.get(확장자, "")) #.py prefix가 제대로 작동하지 않음
            # 강제로 #을 넣으면 잘 작동함
            codeblockinpage.title = f'{주석prefix매핑.get(확장자, "")} 파일이름 : {title} \n\n{data}'
            codeblockinpage.wrap = True
            codeblockinpage.language = 확장자언어매핑.get(확장자, 'plain text')
        except:
            print('error', 확장자)
