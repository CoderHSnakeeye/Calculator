[app]

title = Calculator
package.name = calculator
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt
version = 1.0.0
requirements = python3,kivy
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.3.0
android.archs = arm64-v8a, armeabi-v7a
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
p4a.branch = master
p4a.bootstrap = sdl2
android.entrypoint = calculator_kivy.py
android.icon.filename = %(source.dir)s/icon.png
android.presplash.filename = %(source.dir)s/presplash.png

[buildozer]

log_level = 2
warn_on_root = 1