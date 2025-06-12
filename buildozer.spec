[app]
title = Blockly
package.name = blockly
package.domain = com.petkodev.blockly
icon.filename = Blockly.png  # <-- make sure the file exists

version = 1.0

source.dir = .
source.include_exts = py,png,kv,atlas,jpg,jpeg,ttf,otf,xml

requirements = python3,kivy

android.arch = armeabi-v7a, arm64-v8a

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.copy_libs = 1
android.use_sdl2 = 1

android.api = 33
android.minapi = 21
android.target = 33
android.ndk = 25b

log_level = 2

entrypoint = main.py

[buildozer]
build_dir = .buildozer
log_level = 2
num_jobs = 4
