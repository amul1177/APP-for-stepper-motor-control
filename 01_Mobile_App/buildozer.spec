[app]
title = TriAxis Pro
package.name = triaxispro
package.domain = com.apexprecision

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0
requirements = python3,kivy

[buildozer]
log_level = 2

[app]
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

orientation = portrait
fullscreen = 0

android.permissions = BLUETOOTH,BLUETOOTH_ADMIN,ACCESS_COARSE_LOCATION,ACCESS_FINE_LOCATION,INTERNET,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE

android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.gradle_dependencies = 

android.add_src = 
android.add_aars = 

[buildozer]
warn_on_root = 1