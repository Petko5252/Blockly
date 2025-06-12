[app]

# (str) Title of your application
title = Blockly

# (str) Package name
package.name = Blockly

# (str) Package domain (used for the package namespace)
package.domain = com.petkodev.blockly

# (str) Source code directory
source.dir = .

# (str) List of allowed extensions to include (separated by comma)
source.include_exts = py,png,kv,atlas

# (str) Application versioning
version = 1.0

# (str) Requirements for the app, separated by comma
requirements = kivy==2.1.0,requests

# (str) Icon file for the app
icon.filename = Blockly.png

# (str) Screen orientation ('portrait', 'landscape' or 'all')
orientation = portrait

# (int) Fullscreen mode (1 = yes, 0 = no)
fullscreen = 1

# (str) Permissions required by the app (comma separated)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, VIBRATE

# (str) The entry point filename (your main Python file)
entrypoint = main.py

# (int) Hide the Android status bar (1 = yes, 0 = no)
android.hide_statusbar = 1

# (str) Presplash image shown while loading app
android.presplash = Blockly.png

# (int) Minimum Android API level
android.api = 30

# (str) Android NDK version
android.ndk = 25b

# (int) Android SDK version
android.sdk = 26

# (str) Package format to use ('gradle' recommended)
android.packaging = gradle

# (str) Supported Android CPU architectures (comma separated)
android.archs = arm64-v8a, armeabi-v7a


[buildozer]

# (int) Log level (0=debug, 1=info, 2=warning, 3=error, 4=critical)
log_level = 2

# (int) Warn if running as root user (1=yes, 0=no)
warn_on_root = 1
