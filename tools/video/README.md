# Vídeo de demostración

Genera `assets/video/demo-{es,en}.{mp4,webm}` y `poster-{es,en}.jpg`: un vídeo de 25 s (1920×1080) con el reloj y el móvil grabados en los emuladores.

Requisitos: `adb`, `ffmpeg` (con `libx264` y `libvpx-vp9`), Python 3 con Pillow y la fuente del sistema `/System/Library/Fonts/SFNS.ttf` (macOS).

## 1. Emuladores

- **Móvil:** AVD `WristNote_Video` (Pixel 7), arrancado **con audio** (sin `-no-audio`, o el cronómetro de grabación no avanza). Con la app debug instalada y las 4 notas de demo (`1a2b3c4d-000[1-4]`) en `files/recordings`.
- **Reloj:** AVD Wear OS redondo grande (454×454), por ejemplo `AmpereLab_Wear`, con `wear-debug.apk`.

Deben ser `emulator-5554` (móvil) y `emulator-5556` (reloj).

## 2. Capturar

```bash
./capture.sh
```

El reloj no se empareja con el móvil: `wstate.sh` escribe cada estado en las preferencias de la app debug y la reabre. La transcripción real no funciona en el emulador, así que el paso 4 enseña una nota de demo.

## 3. Componer

```bash
python3 -I make_assets.py ../../assets/img/icon.png   # fondo, marcos, máscaras, textos
./render.sh es demo-es.mp4
./render.sh en demo-en.mp4
for l in es en; do
  cp demo-$l.mp4 ../../assets/video/
  ffmpeg -y -i demo-$l.mp4 -c:v libvpx-vp9 -b:v 0 -crf 36 -row-mt 1 -an ../../assets/video/demo-$l.webm
  ffmpeg -y -ss 7 -i demo-$l.mp4 -frames:v 1 -q:v 4 ../../assets/video/poster-$l.jpg
done
```

Los textos de cada paso están en `make_assets.py` (`CAPTIONS`) y los tiempos en `render.sh` / `graph.tmpl`. Si vuelves a capturar, revisa los cortes: el toque en el reloj (~3,06 s en `w_idle.mp4`) y el fotograma blanco del enlace en `p_rec.mp4` (entre 1,9 y 2,6 s).
