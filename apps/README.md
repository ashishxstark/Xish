### Xish AI Monorepo

- apps/backend: FastAPI server with SSE chat, memory, preferences
- apps/mobile: Expo React Native app with landing + chat

Quick start backend (Docker):

```bash
cd apps/backend
cp .env.example .env
# Edit env as needed
docker compose up --build
```

Quick start mobile:

```bash
cd apps/mobile
cp .env.example .env
npm install
npm run start
```

Deploy targets:
- Backend: container on any cloud (Fly.io, Railway, Render, etc.)
- Mobile: EAS build for Play Store / App Store
