[app]

# (str) Title of your application
title = Blocly

# (str) Package name
package.name = blockly

# (str) Package domain (reverse DNS)
package.domain = com.petkodev.blockly

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let Buildozer detect)
source.include_exts = py,png,kv,atlas,jpg,jpeg,ttf,otf,xml

# (list) Application requirements
# Include kivy and dependencies used for your game
requirements = python3,kivy

# (str) Supported architectures
android.arch = armeabi-v7a, arm64-v8a

# (str) Presplash image (splash screen)
presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the app
icon.filename = Blockly.png

# (str) Orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (list) Permissions your app needs
android.permissions = INTERNET

# (bool) Copy libs inside APK instead of using system installed ones
android.copy_libs = 1

# (bool) Use SDL2 windowing backend (recommended)
android.use_sdl2 = 1

# (int) Android API level (numeric)
android.api = 33

# (int) Minimum API your app supports
android.minapi = 21

# (int) Target API your app supports
android.sdk = 33

# (str) Android NDK version to use (automatic default)
# android.ndk = 25b

# (bool) Enable Android logcat (debugging)
log_level = 2

# (bool) Sign your APK automatically (for release, requires keystore)
# android.release = 0

# (str) Entry point of app (default 'main.py' with 'app' class)
# You can leave as default if your main file is 'main.py'
entrypoint = main.py


[buildozer]

# (str) Path to build artifact cache (default .buildozer)
build_dir = .buildozer

# (list) Buildozer commands to run before compilation
# For cleaning before new build use: clean

# (str) Log level (0=debug, 1=info, 2=warning)
log_level = 2

# (int) Number of concurrent build jobs
num_jobs = 4
