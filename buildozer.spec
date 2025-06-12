[app]

title = Blockly
package.name = Blockly
package.domain = com.petkodev.blockly
source.dir = .
source.include_exts = py,png,kv,atlas
version = 1.0
requirements = python3,kivy
icon.filename = Blockly.png
orientation = portrait
fullscreen = 1

# Uncomment if your app uses Android permissions (camera, internet, etc.)
android.permissions = INTERNET

# Entry point for your app
entrypoint = main.py

# Hide the status bar (optional)
android.hide_statusbar = 1

# Include .png and other media
android.presplash = Blockly.png

# Minimum API level
android.minapi = 21
android.target = 30

# Package format (debug APK)
android.packaging = gradle

# Supported architectures (reduce if needed)
android.archs = arm64-v8a, armeabi-v7a

# Keep these blank if unsure
# android.ndk = 
# android.sdk = 
# android.ndk_path = 
# android.sdk_path = 

[buildozer]
log_level = 2
warn_on_root = 1
