"""Static layers for the WristNote demo video (1920x1080)."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = os.path.dirname(os.path.abspath(__file__)) + "/assets"
os.makedirs(OUT, exist_ok=True)
W, H = 1920, 1080
FONT = "/System/Library/Fonts/SFNS.ttf"
ICON = sys.argv[1]  # 512px app icon


def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    f.set_variation_by_name(weight)
    return f


# Layout (shared with render.sh)
PHONE_W, PHONE_H = 396, 880          # screen size (1080x2400 scaled)
PHONE_X, PHONE_Y = 1290, (H - PHONE_H) // 2
BODY_PAD, PHONE_R = 14, 54
WATCH_D = 400
WATCH_CX, WATCH_CY = 930, 560
WATCH_X, WATCH_Y = WATCH_CX - WATCH_D // 2, WATCH_CY - WATCH_D // 2

# Background: dark indigo radial gradient + soft glows behind the devices
bg = Image.new("RGB", (W, H))
px = bg.load()
for y in range(H):
    for x in range(W):
        d = math.hypot((x - 1150) / 1300, (y - 540) / 900)
        t = min(1.0, d)
        c0, c1 = (62, 74, 128), (13, 16, 32)
        px[x, y] = tuple(int(c0[i] * (1 - t) + c1[i] * t) for i in range(3))
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
g = ImageDraw.Draw(glow)
g.ellipse([WATCH_CX - 330, WATCH_CY - 330, WATCH_CX + 330, WATCH_CY + 330], fill=(255, 107, 107, 34))
g.ellipse([PHONE_X - 160, 160, PHONE_X + PHONE_W + 160, H - 160], fill=(138, 155, 230, 46))
glow = glow.filter(ImageFilter.GaussianBlur(120))
bg = Image.alpha_composite(bg.convert("RGBA"), glow)

# Drop shadows for both devices
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
s = ImageDraw.Draw(sh)
s.rounded_rectangle([PHONE_X - BODY_PAD + 10, PHONE_Y - BODY_PAD + 30, PHONE_X + PHONE_W + BODY_PAD + 10, PHONE_Y + PHONE_H + BODY_PAD + 30], PHONE_R + BODY_PAD, fill=(0, 0, 0, 150))
s.ellipse([WATCH_X - 22 + 8, WATCH_Y - 22 + 26, WATCH_X + WATCH_D + 22 + 8, WATCH_Y + WATCH_D + 22 + 26], fill=(0, 0, 0, 150))
bg = Image.alpha_composite(bg, sh.filter(ImageFilter.GaussianBlur(28)))

# Watch strap stubs (behind the case)
st = ImageDraw.Draw(bg)
for y0, y1 in ((WATCH_Y - 150, WATCH_Y + 40), (WATCH_Y + WATCH_D - 40, WATCH_Y + WATCH_D + 150)):
    st.rounded_rectangle([WATCH_CX - 125, y0, WATCH_CX + 125, y1], 40, fill=(30, 33, 44))
bg.convert("RGB").save(f"{OUT}/bg.png")

# Phone body: frame with a transparent rounded hole for the screen
frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
f = ImageDraw.Draw(frame)
f.rounded_rectangle([PHONE_X - BODY_PAD - 3, PHONE_Y - BODY_PAD - 3, PHONE_X + PHONE_W + BODY_PAD + 3, PHONE_Y + PHONE_H + BODY_PAD + 3], PHONE_R + BODY_PAD + 3, fill=(70, 76, 92, 255))
f.rounded_rectangle([PHONE_X - BODY_PAD, PHONE_Y - BODY_PAD, PHONE_X + PHONE_W + BODY_PAD, PHONE_Y + PHONE_H + BODY_PAD], PHONE_R + BODY_PAD, fill=(14, 15, 20, 255))
hole = Image.new("L", (W, H), 0)
ImageDraw.Draw(hole).rounded_rectangle([PHONE_X, PHONE_Y, PHONE_X + PHONE_W, PHONE_Y + PHONE_H], PHONE_R, fill=255)
frame.putalpha(Image.eval(Image.composite(Image.new("L", (W, H), 0), frame.getchannel("A"), hole), lambda v: v))
# side buttons
f = ImageDraw.Draw(frame)
f.rounded_rectangle([PHONE_X + PHONE_W + BODY_PAD + 2, PHONE_Y + 170, PHONE_X + PHONE_W + BODY_PAD + 7, PHONE_Y + 250], 3, fill=(70, 76, 92, 255))
f.rounded_rectangle([PHONE_X + PHONE_W + BODY_PAD + 2, PHONE_Y + 290, PHONE_X + PHONE_W + BODY_PAD + 7, PHONE_Y + 430], 3, fill=(70, 76, 92, 255))

# Watch case: bezel ring + crown, transparent circle for the display
f.rounded_rectangle([WATCH_X + WATCH_D + 16, WATCH_CY - 34, WATCH_X + WATCH_D + 40, WATCH_CY + 34], 10, fill=(88, 94, 112, 255))
f.ellipse([WATCH_X - 24, WATCH_Y - 24, WATCH_X + WATCH_D + 24, WATCH_Y + WATCH_D + 24], fill=(88, 94, 112, 255))
f.ellipse([WATCH_X - 18, WATCH_Y - 18, WATCH_X + WATCH_D + 18, WATCH_Y + WATCH_D + 18], fill=(22, 24, 30, 255))
alpha = frame.getchannel("A")
cut = Image.new("L", (W, H), 0)
ImageDraw.Draw(cut).ellipse([WATCH_X, WATCH_Y, WATCH_X + WATCH_D, WATCH_Y + WATCH_D], fill=255)
frame.putalpha(Image.composite(Image.new("L", (W, H), 0), alpha, cut))
frame.save(f"{OUT}/frame.png")

# Screen masks (size of the scaled screens)
m = Image.new("L", (PHONE_W, PHONE_H), 0)
ImageDraw.Draw(m).rounded_rectangle([0, 0, PHONE_W - 1, PHONE_H - 1], PHONE_R, fill=255)
m.save(f"{OUT}/phone_mask.png")
m = Image.new("L", (WATCH_D, WATCH_D), 0)
ImageDraw.Draw(m).ellipse([0, 0, WATCH_D - 1, WATCH_D - 1], fill=255)
m.save(f"{OUT}/watch_mask.png")

# Tap ripple (drawn over the watch "Iniciar" button)
r = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
d = ImageDraw.Draw(r)
d.ellipse([10, 10, 110, 110], fill=(255, 255, 255, 70), outline=(255, 255, 255, 200), width=4)
d.ellipse([42, 42, 78, 78], fill=(255, 255, 255, 210))
r.save(f"{OUT}/tap.png")

# Captions: step number, title, subtitle; left column
CAPTIONS = {
    "es": [
        ("1", "Toca tu reloj", "Un toque en WristNote\ndesde la muñeca."),
        ("2", "Tu móvil graba", "Con su micrófono, aunque\nesté en el bolsillo."),
        ("3", "Se transcribe\nen el teléfono", "Sin la nube, sin cuentas."),
        ("4", "Nota y resumen,\nlistos", "Para buscar, editar\no compartir."),
    ],
    "en": [
        ("1", "Tap your watch", "One tap on WristNote\nfrom your wrist."),
        ("2", "Your phone records", "With its microphone, even\nin your pocket."),
        ("3", "Transcribed\non the phone", "No cloud, no account."),
        ("4", "Note and summary,\nready", "To search, edit\nor share."),
    ],
}
END = {"es": "Notas de voz desde tu muñeca", "en": "Voice notes from your wrist"}
X0 = 130
for lang, caps in CAPTIONS.items():
    for i, (num, title, sub) in enumerate(caps):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        tf, sf, nf = font(64, "Bold"), font(32, "Regular"), font(28, "Bold")
        tb = d.multiline_textbbox((0, 0), title, font=tf, spacing=10)
        sb = d.multiline_textbbox((0, 0), sub, font=sf, spacing=10)
        total = 56 + 36 + (tb[3] - tb[1]) + 28 + (sb[3] - sb[1])
        y = (H - total) // 2
        d.ellipse([X0, y, X0 + 56, y + 56], fill=(138, 155, 230, 60), outline=(166, 180, 240, 255), width=2)
        d.text((X0 + 28, y + 28), num, font=nf, fill=(220, 226, 255, 255), anchor="mm")
        y += 56 + 36
        d.multiline_text((X0, y - tb[1]), title, font=tf, fill=(244, 246, 255, 255), spacing=10)
        y += (tb[3] - tb[1]) + 28
        d.multiline_text((X0, y - sb[1]), sub, font=sf, fill=(178, 188, 222, 255), spacing=10)
        im.save(f"{OUT}/cap_{lang}_{i + 1}.png")

    # End card
    im = Image.open(f"{OUT}/bg.png").convert("RGBA")
    dark = Image.new("RGBA", (W, H), (10, 12, 26, 150))
    im = Image.alpha_composite(im, dark)
    icon = Image.open(ICON).convert("RGBA").resize((200, 200), Image.LANCZOS)
    m = Image.new("L", (200, 200), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, 199, 199], 46, fill=255)
    icon.putalpha(Image.composite(icon.getchannel("A"), m, m))
    im.alpha_composite(icon, ((W - 200) // 2, 280))
    d = ImageDraw.Draw(im)
    d.text((W // 2, 590), "WristNote", font=font(96, "Bold"), fill=(244, 246, 255, 255), anchor="mm")
    d.text((W // 2, 680), END[lang], font=font(40, "Regular"), fill=(178, 188, 222, 255), anchor="mm")
    d.text((W // 2, 760), "Android · Wear OS", font=font(28, "Semibold"), fill=(138, 155, 230, 255), anchor="mm")
    im.convert("RGB").save(f"{OUT}/end_{lang}.png")

print("ok")
