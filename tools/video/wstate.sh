#!/bin/zsh
# usage: wstate.sh STATE  -> sets the watch app state and restarts its activity
W=(adb -s emulator-5556); PKG=io.github.manuel2f.wristnote.debug
$W shell am force-stop $PKG
$W shell "run-as $PKG sh -c 'mkdir -p shared_prefs && echo \"<?xml version=\\\"1.0\\\" encoding=\\\"utf-8\\\" standalone=\\\"yes\\\" ?><map><string name=\\\"state\\\">$1</string><string name=\\\"session\\\">1a2b3c4d-0007-4000-8000-000000000007</string></map>\" > shared_prefs/state.xml'"
$W shell am start -n $PKG/com.wearrecap.RecordingLauncherActivity >/dev/null
