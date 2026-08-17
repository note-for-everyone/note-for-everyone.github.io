# 📝 오늘의 노트 (note-for-everyone.github.io)

모두를 위한 **개발/IT**, **금융/주식**, **생활 꿀팁** 정보를 공유하는 Hugo 기반 기술 블로그입니다.

- **사이트 주소**: [https://note-for-everyone.github.io/](https://note-for-everyone.github.io/)
- **테마**: [PaperMod](https://github.com/adityatelange/hugo-PaperMod)

---

## 📂 카테고리 구성

1. 💻 **개발/IT (`개발/IT`)** : Git, 개발 기초, AI/LLM 동향, 생산성 도구, 실무 프로그래밍 가이드
2. 📈 **금융/주식 (`금융/주식`)** : 배당주, ETF, 절세 혜택(ISA/연금저축), 경제 상식, 기초 투자 가이드
3. 💡 **생활 꿀팁 (`생활 꿀팁`)** : 윈도우/Mac 생산성 단축키, 정부 지원금, 실생활 유용한 웹 서비스

---

## 🤖 자동 포스팅 시스템 (GitHub Actions)

이 저장소는 **Gemini API**와 **GitHub Actions**를 결합하여 매일 정해진 시간에 3대 카테고리를 순환하며 새로운 유익한 글을 자동으로 작성하고 배포합니다.

### 워크플로우 동작 구조
1. 매일 KST 오전 9시 (UTC 00:00) GitHub Actions 스케줄러 실행
2. `scripts/auto_post.py`가 최근 글 목록을 분석하여 중복되지 않는 최신 주제 선정
3. TOML Frontmatter 및 표/가이드가 포함된 고품질 마크다운 자동 생성 후 `content/posts/`에 저장
4. 변경 사항이 `main` 브랜치에 자동 커밋 & 푸시되면 `hugo.yaml` 워크플로우가 사이트 재배포

### GitHub Actions Secret 설정
- 저장소 `Settings` $\rightarrow$ `Secrets and variables` $\rightarrow$ `Actions`
- `GEMINI_API_KEY` : Google AI Studio에서 발급받은 API 키 등록
