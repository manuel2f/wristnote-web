# WristNote Web 🎙️

Web oficial y landing page de **WristNote**, la app de Android y Wear OS para grabar notas de voz desde el reloj con el micrófono del móvil y transcribirlas en el propio teléfono.

Misma base que [amperelab-web](../amperelab-web/): HTML estático, CSS con variables y Vanilla JS, sin dependencias.

## ✨ Qué incluye

- **Bilingüe:** inglés en `/` y español en `/es/`.
- **Modo claro / oscuro** automático, con botón y persistencia en `localStorage`.
- **Mockups ilustrados en HTML/CSS** (esfera con la complicación REC, lista de notas, notificación y Ajustes rápidos) mientras no haya capturas reales.
- **Bento grid** de funciones, flujo «cómo funciona», acceso anticipado, novedades y FAQ.
- **Política de privacidad** en `/privacy/` (copia de `WristNote/docs/legal/privacy-policy.html`).

## 🚀 Probar en local

```bash
npm run dev   # http://localhost:3000
```

## 🌐 Desplegar

Igual que AmpereLab: GitHub Pages (rama `main`, carpeta raíz), Cloudflare Pages o Vercel sin comando de build.

## 📝 Pendiente

- Sustituir los mockups por capturas reales (`assets/img/en|es/`) y añadir `feature-graphic.png` para `og:image`.
- Si la prueba cerrada usa Google Group, añadir el paso del grupo en la sección de acceso anticipado.
