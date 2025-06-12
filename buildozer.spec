[app]
# (str) Title of your application
title = Blockly

# (str) Package name
package.name = blockly

# (str) Package domain (unique, in reverse DNS notation)
package.domain = com.petkodev.blockly

# (str) Icon file name (ensure this image exists in the root directory)
icon.filename = Blockly.png

# (str) Application version
version = 1.0

# (str) Source code directory
source.dir = .

# (list) Source file extensions to include
source.include_exts = py,png,kv,atlas,jpg,jpeg,ttf,otf,xml

# (list) Application requirements
requirements = python3,kivy

# ✅ Use the updated key for architecture support
android.archs = armeabi-v7a, arm64-v8a

# (str) Supported orientation
orientation = portrait

# (int) Fullscreen mode (1 to enable)
fullscreen = 1

# (list) Permissions required by the app
android.permissions = INTERNET

# (bool) Copy internal Python libraries to APK
android.copy_libs = 1

# (bool) Use SDL2 (required by Kivy)
android.use_sdl2 = 1

# (int) Target Android API level
android.api = 33

# (int) Minimum Android API level
android.minapi = 21

# (int) Android target API level
android.target = 33

# (str) NDK version
android.ndk = 25b

# (int) Log level (0 = error, 1 = warn, 2 = info, 3 = debug, 4 = trace)
log_level = 2

# (str) Main Python file
entrypoint = main.py

[buildozer]
# (str) Build directory
build_dir = .buildozer

# (int) Log level for buildozer itself
log_level = 2

# (int) Number of parallel jobs (helps speed up builds)
num_jobs = 4
