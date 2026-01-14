# Installation Guide - Car Rental App

## Quick Start Guide

Follow these steps to get the Car Rental App running on your machine.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required Software

1. **Node.js** (v14 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **npm** (comes with Node.js) or **yarn**
   - Verify npm: `npm --version`
   - Or install yarn: `npm install -g yarn`

3. **Expo CLI**
   ```bash
   npm install -g expo-cli
   ```
   - Verify installation: `expo --version`

4. **Git** (optional, for version control)
   - Download from: https://git-scm.com/

### For iOS Development (Mac only)

5. **Xcode** (latest version)
   - Download from Mac App Store
   - Install Command Line Tools: `xcode-select --install`

6. **iOS Simulator**
   - Comes with Xcode
   - Open Xcode > Preferences > Components to download simulators

### For Android Development

7. **Android Studio**
   - Download from: https://developer.android.com/studio
   - Install Android SDK
   - Set up Android Virtual Device (AVD)

8. **Java Development Kit (JDK)**
   - JDK 11 or higher
   - Download from: https://www.oracle.com/java/technologies/downloads/

### For Testing on Physical Device

9. **Expo Go App**
   - iOS: Download from App Store
   - Android: Download from Google Play Store

---

## Step-by-Step Installation

### Step 1: Extract the Project

```bash
# Extract the ZIP file
unzip CarRentalApp.zip

# Navigate to the project directory
cd CarRentalApp
```

### Step 2: Install Dependencies

```bash
# Using npm
npm install

# OR using yarn
yarn install
```

This will install all required packages including:
- React Native
- React Navigation
- React Native Paper
- Firebase SDK
- And other dependencies

**Note**: This may take 5-10 minutes depending on your internet connection.

### Step 3: Set Up Firebase

#### 3.1 Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter project name: "car-rental-app" (or your preferred name)
4. Disable Google Analytics (optional for development)
5. Click "Create project"

#### 3.2 Register Web App

1. In Firebase Console, click the Web icon (</>)
2. Register app with nickname: "Car Rental App"
3. Copy the Firebase configuration object

#### 3.3 Configure Firebase in App

1. Open `src/config/firebase.js` in your code editor
2. Replace the placeholder values:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID",
  measurementId: "YOUR_MEASUREMENT_ID"
};
```

#### 3.4 Enable Authentication

1. In Firebase Console, go to "Authentication"
2. Click "Get Started"
3. Click "Email/Password"
4. Enable "Email/Password"
5. Click "Save"

#### 3.5 Create Firestore Database

1. In Firebase Console, go to "Firestore Database"
2. Click "Create database"
3. Select "Start in test mode"
4. Choose your preferred location
5. Click "Enable"

#### 3.6 Add Sample Car Data

1. In Firestore, click "Start collection"
2. Collection ID: `cars`
3. Add documents using the sample data from `DATABASE_SCHEMA.md`

Example first car:
```
Document ID: (auto-generated)
Fields:
  brand: "Toyota"
  model: "Camry"
  type: "Sedan"
  seatingCapacity: 5
  fuelType: "Petrol"
  transmission: "Automatic"
  pricePerDay: 45
  available: true
  features: ["Air Conditioning", "Bluetooth", "GPS"]
  images: []
  year: 2023
  color: "Silver"
  licensePlate: "ABC-1234"
  mileage: 15000
  location: "Downtown Branch"
```

Repeat for at least 5-8 cars to have a good catalog.

### Step 4: Start the Development Server

```bash
# Start Expo development server
npm start

# OR
expo start

# OR with cache cleared
expo start -c
```

This will:
- Start the Metro bundler
- Open Expo DevTools in your browser
- Display a QR code

### Step 5: Run the App

#### Option A: iOS Simulator (Mac only)

```bash
# Press 'i' in the terminal
# OR
npm run ios
```

#### Option B: Android Emulator

```bash
# Make sure Android emulator is running
# Press 'a' in the terminal
# OR
npm run android
```

#### Option C: Physical Device

1. Install "Expo Go" app on your phone
2. Scan the QR code from the terminal
   - iOS: Use Camera app
   - Android: Use Expo Go app

---

## Verification

### Test the Installation

1. **App Launches**: The app should open to the login screen
2. **Create Account**: Try signing up with a test email
3. **Login**: Login with your test account
4. **Browse Cars**: Navigate to the car catalog
5. **View Details**: Click on a car to see details

### Check Firebase Connection

1. Go to Firebase Console > Authentication
2. Verify your test user appears in the users list
3. Go to Firestore Database
4. Check if any data is being created

---

## Troubleshooting

### Issue: Dependencies Won't Install

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: Expo Won't Start

**Solution:**
```bash
# Update Expo CLI
npm install -g expo-cli

# Clear Expo cache
expo start -c
```

### Issue: Firebase Connection Error

**Solution:**
1. Verify Firebase config in `src/config/firebase.js`
2. Check if Authentication is enabled
3. Check if Firestore is created
4. Verify internet connection

### Issue: Android Build Fails

**Solution:**
1. Check Android Studio is installed
2. Verify ANDROID_HOME environment variable
3. Accept Android SDK licenses:
   ```bash
   cd ~/Library/Android/sdk/tools/bin
   ./sdkmanager --licenses
   ```

### Issue: iOS Build Fails

**Solution:**
1. Update Xcode to latest version
2. Install CocoaPods:
   ```bash
   sudo gem install cocoapods
   ```
3. Clear iOS build:
   ```bash
   cd ios
   pod install
   cd ..
   ```

### Issue: "Unable to resolve module"

**Solution:**
```bash
# Clear Metro bundler cache
expo start -c

# OR
npx react-native start --reset-cache
```

---

## Environment Setup (Optional)

### Setting Up Environment Variables

Create a `.env` file in the root directory:

```env
FIREBASE_API_KEY=your_api_key
FIREBASE_AUTH_DOMAIN=your_auth_domain
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_STORAGE_BUCKET=your_storage_bucket
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
```

Then install dotenv:
```bash
npm install react-native-dotenv
```

---

## Next Steps

After successful installation:

1. **Read the Documentation**
   - `README.md` - Overview and features
   - `DATABASE_SCHEMA.md` - Database structure
   - `FIREBASE_SETUP.md` - Detailed Firebase guide

2. **Customize the App**
   - Update theme in `src/theme/theme.js`
   - Add more car data
   - Customize screens

3. **Test Features**
   - User authentication
   - Car browsing and filtering
   - Trip planning
   - Booking creation
   - Status tracking

4. **Prepare for Production**
   - Update Firebase security rules
   - Add proper error handling
   - Implement analytics
   - Test on multiple devices

---

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review Firebase Console for errors
3. Check Expo DevTools for warnings
4. Review the code comments
5. Check React Native and Expo documentation

---

## System Requirements

### Minimum Requirements
- **OS**: macOS 10.13+, Windows 10, or Linux
- **RAM**: 8GB
- **Storage**: 10GB free space
- **Internet**: Stable connection required

### Recommended Requirements
- **OS**: macOS 11+, Windows 11, or Ubuntu 20.04+
- **RAM**: 16GB
- **Storage**: 20GB free space
- **Internet**: High-speed connection

---

## Development Tools (Recommended)

- **Code Editor**: Visual Studio Code
- **VS Code Extensions**:
  - React Native Tools
  - ES7+ React/Redux/React-Native snippets
  - Prettier - Code formatter
  - ESLint
  - Firebase

---

## Success Checklist

- [ ] Node.js and npm installed
- [ ] Expo CLI installed
- [ ] Project dependencies installed
- [ ] Firebase project created
- [ ] Firebase configuration updated
- [ ] Authentication enabled
- [ ] Firestore database created
- [ ] Sample car data added
- [ ] Development server starts successfully
- [ ] App runs on simulator/device
- [ ] Can create user account
- [ ] Can login successfully
- [ ] Can browse cars
- [ ] Firebase connection verified

---

**Congratulations!** 🎉 Your Car Rental App is now ready for development!
