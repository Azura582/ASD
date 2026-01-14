# Firebase Setup Guide

## Prerequisites
- A Google account
- Node.js installed on your machine

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project"
3. Enter your project name (e.g., "car-rental-app")
4. Follow the setup wizard
5. Enable Google Analytics (optional)

## Step 2: Register Your App

1. In the Firebase Console, click on the Web icon (</>) to add a web app
2. Register your app with a nickname (e.g., "Car Rental App")
3. Copy the Firebase configuration object

## Step 3: Configure Firebase in Your App

1. Open `src/config/firebase.js`
2. Replace the placeholder values with your Firebase configuration:

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

## Step 4: Enable Authentication

1. In Firebase Console, go to "Authentication"
2. Click "Get Started"
3. Enable "Email/Password" sign-in method
4. Click "Save"

## Step 5: Create Firestore Database

1. In Firebase Console, go to "Firestore Database"
2. Click "Create database"
3. Choose "Start in test mode" (for development)
4. Select a location for your database
5. Click "Enable"

## Step 6: Set Up Firestore Security Rules

Replace the default rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users collection
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
    }
    
    // Cars collection
    match /cars/{carId} {
      allow read: if request.auth != null;
      allow write: if request.auth != null && request.auth.token.admin == true;
    }
    
    // Bookings collection
    match /bookings/{bookingId} {
      allow read: if request.auth != null && 
        (resource.data.userId == request.auth.uid || 
         request.auth.token.admin == true);
      allow create: if request.auth != null && 
        request.resource.data.userId == request.auth.uid;
      allow update: if request.auth != null && 
        (resource.data.userId == request.auth.uid || 
         request.auth.token.admin == true);
      allow delete: if request.auth != null && 
        request.auth.token.admin == true;
    }
  }
}
```

## Step 7: Enable Storage (Optional)

1. In Firebase Console, go to "Storage"
2. Click "Get Started"
3. Accept the default security rules
4. Click "Done"

## Step 8: Create Firestore Collections

You need to create the following collections in Firestore:

### 1. users
- Stores user profile information
- Auto-created when users sign up

### 2. cars
- Stores car information
- You need to manually add car documents (see DATABASE_SCHEMA.md)

### 3. bookings
- Stores booking information
- Auto-created when users make bookings

## Step 9: Add Sample Car Data

1. Go to Firestore Database in Firebase Console
2. Click "Start collection"
3. Collection ID: `cars`
4. Add documents with the structure defined in DATABASE_SCHEMA.md

## Step 10: Test Your Setup

1. Run your React Native app
2. Try to sign up with a new account
3. Check Firebase Console to verify:
   - User is created in Authentication
   - User document is created in Firestore (if implemented)

## Troubleshooting

### Authentication Issues
- Verify Email/Password is enabled in Firebase Console
- Check that your Firebase config is correct
- Ensure you're using the correct Firebase SDK version

### Firestore Issues
- Check security rules allow your operations
- Verify collection names match your code
- Check browser console for detailed error messages

### Network Issues
- Ensure you have internet connection
- Check if Firebase services are operational: https://status.firebase.google.com/

## Additional Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [React Native Firebase](https://rnfirebase.io/)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Authentication](https://firebase.google.com/docs/auth)
