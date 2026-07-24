[app]
title = Miner
package.name = miner
package.domain = com.brenninho

source.dir = .
source.include_exts = py,png,jpg,kv,json,atlas

version = 0.1.0

requirements = python3,kivy,psutil,requests,watchdog

orientation = portrait
fullscreen = 0

icon.filename = %(source.dir)s/data/icon.png

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
