@echo off
echo TriAxis Pro APK Builder
echo Developed by: Amol M.
echo Company: APEX PRECISION MECHATRONIX PVT. LTD.
echo.

echo Step 1: Installing Python dependencies...
pip install kivy[base] kivymd buildozer cython

echo.
echo Step 2: Installing Android build tools...
echo Please install Android SDK and NDK manually if not already installed

echo.
echo Step 3: Building APK...
buildozer android debug

echo.
echo Step 4: APK Location
echo The APK will be created in: bin\triaxispro-1.0-debug.apk

echo.
echo Build complete!
pause