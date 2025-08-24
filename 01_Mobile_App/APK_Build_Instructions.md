# TriAxis Pro - APK Build Instructions

**Developer:** Amol M.  
**Company:** APEX PRECISION MECHATRONIX PVT. LTD.

## Prerequisites

### 1. Install Python 3.8+
```bash
# Download from python.org
# Ensure pip is installed
```

### 2. Install Java JDK 8
```bash
# Download Oracle JDK 8 or OpenJDK 8
# Set JAVA_HOME environment variable
```

### 3. Install Android SDK
```bash
# Download Android Studio or SDK Tools
# Set ANDROID_HOME environment variable
# Install SDK Platform 30 and Build Tools 30.0.3
```

### 4. Install Android NDK
```bash
# Download NDK r23b
# Set ANDROID_NDK_HOME environment variable
```

## Build Steps

### Method 1: Automated Build (Windows)
```bash
# Navigate to mobile app directory
cd "01_Mobile_App"

# Run build script
build_apk.bat
```

### Method 2: Manual Build
```bash
# Install dependencies
pip install kivy[base] kivymd buildozer cython

# Initialize buildozer (first time only)
buildozer init

# Build debug APK
buildozer android debug

# Build release APK (for distribution)
buildozer android release
```

## Build Configuration

The `buildozer.spec` file contains:
- **App Name:** TriAxis Pro
- **Package:** com.apexprecision.triaxispro
- **Version:** 1.0
- **Permissions:** Bluetooth, WiFi, Location
- **Target API:** Android 30 (Android 11)
- **Min API:** Android 21 (Android 5.0)

## Output Location

After successful build:
- **Debug APK:** `bin/triaxispro-1.0-debug.apk`
- **Release APK:** `bin/triaxispro-1.0-release.apk`

## Troubleshooting

### Common Issues:

**Build fails with "SDK not found":**
```bash
# Set environment variables:
set ANDROID_HOME=C:\Android\Sdk
set ANDROID_NDK_HOME=C:\Android\Sdk\ndk\23.1.7779620
set JAVA_HOME=C:\Program Files\Java\jdk1.8.0_XXX
```

**Python dependencies error:**
```bash
# Update pip and setuptools
pip install --upgrade pip setuptools wheel
```

**Cython compilation error:**
```bash
# Install specific Cython version
pip install Cython==0.29.33
```

**NDK version mismatch:**
```bash
# Edit buildozer.spec
android.ndk = 23b
```

## Alternative: Online APK Builder

If local build fails, use online services:
1. **Replit** - Upload code and build online
2. **GitHub Actions** - Automated CI/CD build
3. **Google Colab** - Cloud-based build environment

## File Structure
```
01_Mobile_App/
├── main.py              # Main Kivy app
├── buildozer.spec       # Build configuration
├── build_apk.bat        # Windows build script
├── icon.png             # App icon (create 512x512)
├── presplash.png        # Splash screen (create 1280x720)
└── bin/                 # Output APK files
```

## Testing APK

1. **Install on device:** Enable Developer Options and USB Debugging
2. **ADB install:** `adb install bin/triaxispro-1.0-debug.apk`
3. **Manual install:** Copy APK to device and install

## Distribution

For Google Play Store:
1. Build release APK: `buildozer android release`
2. Sign APK with keystore
3. Upload to Play Console
4. Complete store listing

---

**Support:** support@apexprecision.com  
**© 2024 APEX PRECISION MECHATRONIX PVT. LTD.**