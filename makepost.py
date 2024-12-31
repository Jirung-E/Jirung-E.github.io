# 포스트를 작성하고 함수를 실행하면 알아서 포스트를 올려주는 파이썬 프로그램

# 현재 시간 알아내기, 파일 불러오기
# 현재 시간으로 제목 설정
# 엔터 적용
# 불러온 파일을 본문으로 해서 _posts폴더 안에 포스트 생성
# 포스트 생성 후 git add, git commit, git push?

import sys
from datetime import datetime


def makePost(file):
    head = '''---
title: "{title}"
excerpt: "{excerpt}"
last_modified_at: {now}

categories: 
  - {category}

tags: {tags}

toc: true
toc_sticky: true
---

'''

    body_file = open(file, "r", encoding="utf-8")

    # 첫줄 빼와서 제목으로 쓰기
    title = body_file.readline().replace("#", "").strip()

    # 다음줄 빼와서 요약으로 쓰기,
    # 본문 시작 전 -로 시작하는거 빼와서 카테고리로 쓰기
    excerpt = ""
    line = body_file.readline().strip()
    if line.startswith("-"):
        category = line.replace('-', '').replace(' ', '').strip()       # 여러개 안됨
    else:
        excerpt = line
        line = body_file.readline()
        if line.startswith("-"):
            category = line.replace('-', '').replace(' ', '').strip()       # 여러개 안됨
        
    # 본문 시작 전 +로 시작하는거 빼와서 태그로 쓰기
    tags = []
    for line in body_file:
        if line.startswith("+"):
            line = line.replace('+', '').replace(' ', '').strip()
            if line not in tags:
                tags.append(line)
        else:
            break
    tags_str = ""
    for e in tags:
        tags_str += "\n  - " + e.lower()

    # 남은거 읽기
    body = "\n"
    for line in body_file:
        body += line.replace("\n", "  \n")

    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    post = head.format(title=title, excerpt=excerpt, now=current_time, category=category, tags=tags_str) + body

    print("::PREVIEW::")
    print(post)

    if input("Post? (y/n)\n> ").lower() == "y":
        post_file = open("_posts/" + current_time[:10] + "-" + title.replace(" ", "-") + ".md", "w", encoding="utf-8")
        post_file.write(post)
        post_file.close()
        print("Posted.")




if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: post <file>")
    else:
        sys.argv.pop(0)
        for arg in sys.argv:
            makePost(arg)