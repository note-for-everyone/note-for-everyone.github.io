#!/usr/bin/env python3
"""
Blog Auto-Post Generator for '오늘의 노트'
Automates topic selection, content drafting via Gemini API, and Hugo markdown generation.
"""

import os
import re
import glob
from datetime import datetime, timezone, timedelta

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from slugify import slugify
except ImportError:
    def slugify(text):
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[-\s]+", "-", text) or "post"

CATEGORIES = ["개발/IT", "금융/주식", "생활 꿀팁"]

def get_existing_post_titles():
    """Extract titles from existing posts to avoid topic duplication."""
    post_files = glob.glob("content/posts/*.md")
    titles = []
    for filepath in post_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                match = re.search(r"title\s*=\s*['\"](.*?)['\"]", content)
                if match:
                    titles.append(match.group(1))
        except Exception as e:
            print(f"Warning: Failed to read {filepath}: {e}")
    return titles

def determine_next_category():
    """Rotate through categories based on the current post count."""
    post_files = glob.glob("content/posts/*.md")
    return CATEGORIES[len(post_files) % len(CATEGORIES)]

def generate_post():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")

    if genai is None:
        raise ImportError("google-generativeai library is required. Install with: pip install google-generativeai")

    genai.configure(api_key=api_key)

    category = determine_next_category()
    existing_titles = get_existing_post_titles()
    recent_titles_str = ", ".join([f"'{t}'" for t in existing_titles[-10:]]) if existing_titles else "없음"

    kst = timezone(timedelta(hours=9))
    now = datetime.now(kst)
    date_str = now.strftime("%Y-%m-%dT%H:%M:%S+09:00")
    date_prefix = now.strftime("%Y-%m-%d")

    prompt = f"""
당신은 블로그 '오늘의 노트'를 운영하는 전문 에디터입니다.
이번에 작성할 분야는 [{category}] 카테고리입니다.

[작성 지침]
1. 주제: 최근 트렌드에 맞고, 검색 수요가 높으며 대중 또는 실무자에게 실질적으로 도움을 주는 유익한 주제 1개를 선정하세요.
2. 기존에 다룬 주제 목록: [{recent_titles_str}]
   - 위 목록과 중복되거나 유사한 주제는 절대 피하고, 새로운 주제로 선정하세요.
3. 어투: 친절하고 신뢰감 있는 전문적인 존댓말(~합니다, ~해보세요, ~입니다)
4. 본문 구성:
   - 도입부: 이 주제가 왜 중요하고 누구에게 필요한지 흥미 유발
   - 핵심 내용: 개념 설명 및 비교/정리 표(테이블) 반드시 포함
   - 실전 팁 & 활용 가이드: 구체적 사례 또는 실천 방법
   - 주의사항 & 핵심 요약 정리
5. 출력 형식:
   반드시 아래와 같은 정확한 TOML Frontmatter(+++로 감싸진 형태)를 포함하는 단일 마크다운 텍스트만 출력하세요.
   설명이나 인사말 등 불필요한 텍스트는 절대 포함하지 마세요.

+++
title = '여기에 매력적이고 구체적인 글 제목'
date = {date_str}
draft = false
categories = ['{category}']
tags = ['태그1', '태그2', '태그3', '태그4']
description = '글의 핵심 내용을 담은 매력적인 1~2줄 요약'
slug = 'english-slug-for-url'
+++

# 제목

본문 내용...
"""

    print(f"선택된 카테고리: {category}")
    print(f"Gemini AI 글 작성 요청 중...")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    content = response.text.strip()

    # Code fence cleanup if wrapped
    if content.startswith("```"):
        content = re.sub(r"^```[a-zA-Z]*\n", "", content)
        content = re.sub(r"\n```$", "", content)
    content = content.strip()

    # Extract slug
    slug_match = re.search(r"slug\s*=\s*['\"](.*?)['\"]", content)
    if slug_match and slug_match.group(1):
        slug = slugify(slug_match.group(1))
    else:
        slug = slugify(f"{category}-{now.strftime('%H%M%S')}")

    filename = f"content/posts/{date_prefix}-{slug}.md"
    os.makedirs("content/posts", exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"새 포스트 파일 저장 성공: {filename}")
    return filename

if __name__ == "__main__":
    generate_post()
