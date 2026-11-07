#!/bin/zsh
# Records the raw clips for the demo video from two running emulators.
#   Phone: WristNote_Video (emulator-5554), started WITH audio (no -no-audio), debug app seeded with demo notes.
#   Watch: a Wear OS round emulator (emulator-5556) with the wear debug APK installed.
# Output: clips/{w_idle.mp4,w_rec.png,w_proc.mp4,w_done.png,p_rec.mp4,p_note.mp4}
set -e
cd "${0:A:h}"
mkdir -p clips
PK=io.github.manuel2f.wristnote.debug
P() { adb -s emulator-5554 "$@"; }
W() { adb -s emulator-5556 "$@"; }

# --- Phone setup: dark mode, Spanish app locale, clean status bar (9:41, full battery)
P shell cmd uimode night yes >/dev/null
P shell cmd locale set-app-locales $PK --locales es-ES
W shell cmd locale set-app-locales $PK --locales es-ES
P shell settings put global sysui_demo_allowed 1
demo() { P shell am broadcast -a com.android.systemui.demo -e command "$@" >/dev/null; }
demo enter; demo clock -e hhmm 0941; demo battery -e level 100 -e plugged false
demo network -e wifi show -e level 4; demo network -e mobile hide; demo notifications -e visible false

# Remove any recordings that are not the seeded demo notes (ids 1a2b3c4d-000[1-4])
clean() { for f in $(P shell run-as $PK ls files/recordings | tr -d '\r' | grep -v '1a2b3c4d-000[1-4]'); do P shell run-as $PK rm files/recordings/$f; done; }
open_list() {
  P shell am force-stop $PK; P shell am start -n $PK/com.wearrecap.ui.MainActivity >/dev/null
  until P exec-out uiautomator dump /dev/tty 2>/dev/null | grep -q "Tus grabaciones"; do sleep 1; done; sleep 1
}

# --- Watch clips (state forced through the app's SharedPreferences, see wstate.sh)
wrec() { # name state seconds [tap_at]
  ./wstate.sh $2; sleep 6
  W shell screenrecord --time-limit $3 /sdcard/$1.mp4 &
  if [ -n "$4" ]; then sleep $4; W shell input tap 227 350; fi
  wait; W pull /sdcard/$1.mp4 clips/$1.mp4 >/dev/null
}
wrec w_idle IDLE 7 3          # real tap on "Iniciar" at ~3 s (render cuts before the connection error)
wrec w_proc PROCESSING 5
./wstate.sh RECORDING; sleep 6; W exec-out screencap -p > clips/w_rec.png
./wstate.sh COMPLETED; sleep 6; W exec-out screencap -p > clips/w_done.png
./wstate.sh IDLE

# --- Phone clip 1: recording starts (same deep link the watch sends) and is stopped
clean; open_list
P shell screenrecord --bit-rate 12000000 --time-limit 16 /sdcard/p_rec.mp4 &
sleep 2; P shell am start -a android.intent.action.VIEW -c android.intent.category.BROWSABLE \
  -d "wearrecap://record?sessionId=1a2b3c4d-0009-4000-8000-000000000009" $PK >/dev/null
sleep 9; P shell input tap 810 480   # "Detener" in the recording banner
wait; P pull /sdcard/p_rec.mp4 clips/p_rec.mp4 >/dev/null

# --- Phone clip 2: scroll through a finished note down to its summary
clean; open_list
P shell screenrecord --bit-rate 12000000 --time-limit 12 /sdcard/p_note.mp4 &
sleep 1.5; P shell input swipe 540 1900 540 1150 2200; sleep 1.8; P shell input swipe 540 1900 540 1250 2200
wait; P pull /sdcard/p_note.mp4 clips/p_note.mp4 >/dev/null
clean
echo "clips ready in ${0:A:h}/clips — check the cut points in render.sh (tap, white flash) before rendering"
