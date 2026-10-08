# RoadmapScience

Интерактивная карта изучения фундаментальных наук. React + TypeScript + Vite + GSAP + Motion + Three.js.

## Разработка

```bash
npm install
npm run dev
npm run typecheck
npm run build
```

## GitHub Pages

Settings → Pages → Build and deployment → Source: **GitHub Actions**. Push в main запускает workflow. Адрес после успешного деплоя: https://kumofsoc.github.io/RoadmapScience/.

Прогресс хранится только в localStorage текущего браузера. Другие дисциплины отмечены как планируемые; полная карта доступна для математики. Для слабых устройств и reduced-motion 3D отключается.
