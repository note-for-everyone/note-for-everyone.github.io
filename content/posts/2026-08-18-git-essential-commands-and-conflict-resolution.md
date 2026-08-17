+++
title = '초보 개발자를 위한 Git 필수 명령어와 충돌(Conflict) 해결 가이드'
date = 2026-08-18T09:00:00+09:00
draft = false
categories = ['개발/IT']
tags = ['Git', '깃', '개발기초', '버전관리', 'GitHub']
description = '초보 개발자가 꼭 알아야 할 Git 핵심 명령어부터 협업 시 자주 마주치는 병합 충돌(Merge Conflict) 해결법까지 알기 쉽게 정리합니다.'
slug = 'git-essential-commands-and-conflict-resolution'
+++

# 초보 개발자를 위한 Git 필수 명령어와 충돌(Conflict) 해결 가이드

소프트웨어 개발을 시작하면 가장 먼저 마주치는 도구 중 하나가 바로 **Git(깃)**입니다. 협업과 버전 관리를 위해 필수적이지만, 낯선 명령어와 예기치 못한 **병합 충돌(Conflict)** 때문에 어려움을 겪는 초보 개발자가 많습니다.

이번 글에서는 실무에서 매일 쓰는 핵심 Git 명령어와 충돌 발생 시 당황하지 않고 해결하는 실전 가이드를 정리해 드립니다.

---

## 1. 실무에서 가장 많이 쓰는 Git 핵심 명령어

Git 워크플로우는 기본적으로 `작업 디렉토리` $\rightarrow$ `스테이징 영역(Staging Area)` $\rightarrow$ `로컬 저장소(Repository)` $\rightarrow$ `원격 저장소(Remote)` 순서로 이어집니다.

| 명령어 | 역할 및 용도 |
| :--- | :--- |
| `git status` | 현재 변경된 파일 상태 확인 |
| `git add .` | 변경된 파일들을 스테이징 영역에 추가 |
| `git commit -m "메시지"` | 변경 사항을 설명과 함께 로컬 저장소에 기록 |
| `git pull origin <브랜치>` | 원격 저장소의 최신 변경 사항을 내려받아 병합 |
| `git push origin <브랜치>` | 로컬 커밋 내역을 원격 저장소에 업로드 |
| `git branch <이름>` | 새로운 기능 개발용 브랜치 생성 |
| `git switch <이름>` | 지정한 브랜치로 전환 (구 `git checkout`) |

---

## 2. 안전한 브랜치 협업 워크플로우

`main` 브랜치에 직접 코드를 작성하고 푸시하는 것은 충돌과 버그의 위험이 큽니다. 기능 개발 시 항상 브랜치를 분기하여 작업하는 습관을 들이는 것이 좋습니다.

```bash
# 1. 최신 main 브랜치 상태로 이동
git switch main
git pull origin main

# 2. 새로운 기능 브랜치 생성 및 이동
git switch -c feature/login-page

# 3. 코드 작업 후 커밋
git add .
git commit -m "feat: 로그인 페이지 레이아웃 구현"

# 4. 원격 브랜치에 푸시
git push origin feature/login-page
```

---

## 3. 병합 충돌(Merge Conflict) 해결하는 3단계

충돌은 **동일한 파일의 같은 부분을 두 명 이상의 개발자가 서로 다르게 수정했을 때** 발생합니다. Git은 어떤 코드를 남겨야 할지 스스로 판단할 수 없으므로 개발자에게 수정을 요청합니다.

### 1단계: 충돌 발생 지점 확인
`git pull` 또는 `git merge` 시 충돌이 발생하면 Git은 다음과 같은 충돌 표시자를 파일에 남깁니다.

```plaintext
<<<<<<< HEAD (현재 브랜치 코드)
const API_URL = "https://api.myapp.com/v2";
=======
const API_URL = "https://staging.myapp.com/api";
>>>>>>> feature/new-api (병합하려는 브랜치 코드)
```

### 2단계: 코드 수정한 후 충돌 마커 삭제
남길 최종 코드를 결정하고, `<<<<<<<`, `=======`, `>>>>>>>` 기호들을 모두 지워줍니다.

```javascript
// 올바른 최종 코드로 정리
const API_URL = "https://api.myapp.com/v2";
```

### 3단계: 해결된 파일 스테이징 및 커밋
충돌을 수정한 후 다시 커밋을 진행하면 충돌 해결이 완료됩니다.

```bash
# 수정 완료한 파일 스테이징
git add .

# 충돌 해결 커밋 생성
git commit -m "fix: merge conflict in api config"

# 원격 저장소에 푸시
git push origin main
```

---

## 4. 초보자를 위한 Git 꿀팁 & 주의사항

1. **커밋 단위는 작고 명확하게**  
   너무 많은 변경 사항을 하나의 커밋에 몰아넣으면 나중에 충돌이 발생했을 때 원인을 추적하기 어렵습니다.
2. **작업 시작 전 항상 `git pull`**  
   아침에 작업을 시작하거나 새로운 브랜치를 만들기 전, 항상 원격 저장소의 최신 코드를 당겨오는 습관을 들여 충돌 가능성을 최소화하세요.
3. **`.gitignore` 설정 철저히**  
   `node_modules`, `.env`(보안 키), OS 임시 파일 등은 반드시 `.gitignore`에 등록하여 레포지토리에 올라가지 않도록 방지합니다.
