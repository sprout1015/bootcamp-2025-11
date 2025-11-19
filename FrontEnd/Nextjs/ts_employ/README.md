# Next.js & TypeScript를 이용한 직원 관리 예제 프로젝트

## 📖 프로젝트 소개
이 프로젝트는 Next.js, React, TypeScript를 사용하여 구현한 간단한 직원 정보 관리 애플리케이션 예제입니다. CRUD(생성, 읽기, 수정, 삭제) 기능의 기본적인 구현을 포함하고 있습니다.

## ✨ 주요 기능
- 직원 목록 조회
- 신규 직원 등록
- 직원 정보 수정

## 🛠️ 사용된 기술
- **Framework**: [Next.js](https://nextjs.org/)
- **Library**: [React](https://reactjs.org/)
- **Language**: [TypeScript](https://www.typescriptlang.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) (PostCSS)

## 📂 프로젝트 구조
```
.
├── public/              # 정적 파일 (이미지, 폰트 등)
├── src/
│   ├── app/             # Next.js 13+ App Router 페이지
│   ├── components/      # 리액트 컴포넌트
│   └── util/            # 유틸리티 및 스타일 관련 파일
├── next.config.ts       # Next.js 설정 파일
├── package.json         # 프로젝트 의존성 및 스크립트
└── tsconfig.json        # TypeScript 설정 파일
```

## 🚀 시작하기

### 1. 의존성 설치
프로젝트를 실행하기 위해 필요한 라이브러리들을 설치합니다.
```bash
npm install
```

### 2. 개발 서버 실행
Next.js 개발 서버를 시작합니다.
```bash
npm run dev
```
서버가 실행되면 브라우저에서 `http://localhost:3000`으로 접속하여 확인할 수 있습니다.

## 📜 사용 가능한 스크립트
- `npm run dev`: 개발 모드로 Next.js 애플리케이션을 실행합니다.
- `npm run build`: 프로덕션용으로 애플리케이션을 빌드합니다.
- `npm run start`: 빌드된 프로덕션 서버를 시작합니다.
- `npm run lint`: ESLint를 사용하여 코드 스타일을 검사합니다.