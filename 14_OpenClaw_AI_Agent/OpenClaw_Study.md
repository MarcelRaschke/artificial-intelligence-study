# OpenClaw - 오픈소스 개인 AI 어시스턴트 스터디

## 1. OpenClaw 개요

**OpenClaw**은 자신의 디바이스에서 실행되는 오픈소스 개인 AI 어시스턴트입니다.
클라우드 서비스에 의존하지 않고, 이미 사용 중인 메시징 채널(WhatsApp, Telegram, Slack, Discord 등)을 통해 소통할 수 있습니다.

- **공식 사이트**: https://openclaw.ai/
- **GitHub**: https://github.com/openclaw/openclaw
- **문서**: https://docs.openclaw.ai

### 주요 특징
- 오픈소스 (GitHub 공개)
- 크로스 플랫폼 (macOS, Linux, Windows WSL2)
- 프라이버시 중심 (자체 인프라에서 실행)
- 다중 채널 지원 (20개 이상의 메시징 플랫폼)
- BYOM (Bring Your Own Model) — Ollama를 통한 오프라인 운영 가능

---

## 2. 아키텍처

OpenClaw은 세 가지 핵심 구성 요소로 이루어져 있습니다:

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│  Channels    │────▶│    Gateway       │────▶│ Agent Runtime│
│ (WhatsApp,   │◀────│ (Control Plane)  │◀────│  (AI Models) │
│  Telegram,   │     │  WebSocket-based │     │              │
│  Slack, ...) │     │  Port: 18789     │     │              │
└─────────────┘     └─────────────────┘     └──────────────┘
```

### Gateway (게이트웨이)
- WebSocket 기반 컨트롤 플레인
- 모든 채널 연결 관리
- 기본 포트: 18789 (API), 18790 (Bridge)

### Agent Runtime (에이전트 런타임)
- AI 모델과의 상호작용 처리
- 분산 실행 지원
- 지원 모델: Anthropic Claude, OpenAI GPT, Google Gemini, Ollama (로컬)

### Channels (채널)
- 사용자와의 통신 인터페이스
- 지원 채널: WhatsApp (Baileys), Telegram (grammY), Slack (Bolt), Discord (discord.js), Signal, Google Chat, iMessage, Teams, Matrix, IRC 등

---

## 3. 기존 챗봇과의 차이점

| 구분 | 기존 챗봇 | OpenClaw |
|------|----------|----------|
| 실행 환경 | 클라우드 서비스 | 자체 디바이스/서버 |
| 데이터 소유 | 서비스 제공자 | 사용자 |
| 모델 선택 | 고정 | BYOM (자유 선택) |
| 채널 | 단일 플랫폼 | 다중 채널 동시 지원 |
| 확장성 | 제한적 | Skills 시스템으로 무한 확장 |
| 오프라인 | 불가 | Ollama로 가능 |

---

## 4. 핵심 개념

### Skills (스킬)
- 커뮤니티가 개발한 확장 기능
- 플러그인 방식으로 활성화/비활성화
- 자동 활성화 옵션 지원

### BYOM (Bring Your Own Model)
- 어떤 AI 모델이든 사용 가능
- Ollama를 통한 로컬 모델 실행 (Llama, Mistral 등)
- API 키 없이 완전 오프라인 운영 가능
- Air-gapped 환경에서도 사용 가능

### Canvas / A2UI
- 인터랙티브 캔버스 인터페이스 렌더링
- 웹 기반 UI 제공

---

## 5. 설치 방법

### 빠른 설치 (npm)
```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

### Docker 설치
```bash
docker run -d --name openclaw \
  -p 18789:18789 -p 18790:18790 \
  -e ANTHROPIC_API_KEY=your-key \
  alpine/openclaw:latest
```

### 소스에서 빌드
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm ui:build && pnpm build
pnpm gateway:watch
```

### 시스템 요구사항
- Node.js 24+ (또는 22.16+)
- RAM: 최소 2GB (프로덕션 4GB+ 권장)
- SSD 스토리지 권장
- CPU: 2코어 이상

---

## 6. 유용한 명령어

```bash
# 시스템 상태 확인 및 자동 수정
openclaw doctor --fix

# 모든 서비스 상태 확인
openclaw status --all

# 게이트웨이 수동 시작
openclaw gateway --port 18789 --verbose

# 에이전트 작업 실행
openclaw agent --message "작업 내용" --thinking high
```

---

## 7. 참고 자료

- [OpenClaw 공식 문서](https://docs.openclaw.ai)
- [Getting Started 가이드](https://docs.openclaw.ai/start/getting-started)
- [GitHub 저장소](https://github.com/openclaw/openclaw)
- [OpenClaw 튜토리얼 (AIML API)](https://aimlapi.com/blog/openclaw-full-tutorial-installation-setup-real-automation-use-step-by-step)
