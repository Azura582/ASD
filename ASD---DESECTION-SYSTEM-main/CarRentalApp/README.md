# Car Rental App - React Native

A comprehensive car rental application built with React Native and Firebase, featuring user authentication, car browsing, trip planning, booking management, and real-time status tracking.

## Features

### 🔐 Authentication Module
- User registration with email and password
- Secure login system
- Password validation
- Session management with AsyncStorage
- Firebase Authentication integration

### 🚗 Car Catalog Module
- Browse available rental cars
- Detailed car information (brand, model, type, price)
- Advanced filtering options:
  - Price range
  - Fuel type (Petrol, Diesel, Electric)
  - Transmission (Automatic, Manual)
  - Seating capacity
- Search functionality
- Real-time availability status

### 📍 Trip Details Module
- Enter pickup and drop-off locations
- Specify number of passengers
- Set rental duration (number of days)
- Distance and duration estimation
- Smart car recommendations based on trip requirements

### 💡 Recommendation Module
- Intelligent car suggestions based on:
  - Passenger count
  - Journey distance
  - Budget preferences
- Price estimation
- Availability checking

### 📅 Booking Module
- Interactive calendar for date selection
- Visual date range picker
- Booking validation
- Price breakdown display
- Additional notes option
- Booking confirmation

### 📊 Status & History Module
- Real-time booking status tracking:
  - Booking Confirmed
  - Ready for Pickup
  - Rental Ongoing
  - Rental Completed
  - Cancelled
- Booking history with detailed information
- Timeline view of booking progress
- Cancel booking option

### 👤 Profile Module
- User profile management
- Booking history access
- Settings and preferences
- Logout functionality

## Technology Stack

- **Frontend Framework**: React Native (Expo)
- **Navigation**: React Navigation (Stack & Bottom Tabs)
- **UI Components**: React Native Paper
- **Backend**: Firebase
  - Authentication
  - Firestore Database
  - Cloud Storage
- **State Management**: React Context API
- **Date Handling**: React Native Calendars
- **Icons**: React Native Vector Icons

## Project Structure

```
CarRentalApp/
├── App.js                      # Main app entry point
├── app.json                    # Expo configuration
├── package.json                # Dependencies
├── babel.config.js             # Babel configuration
├── src/
│   ├── config/
│   │   └── firebase.js         # Firebase configuration
│   ├── context/
│   │   └── AuthContext.js      # Authentication context
│   ├── navigation/
│   │   └── MainNavigator.js    # App navigation structure
│   ├── screens/
│   │   ├── Auth/
│   │   │   ├── LoginScreen.js
│   │   │   └── SignupScreen.js
│   │   ├── Home/
│   │   │   └── HomeScreen.js
│   │   ├── Trip/
│   │   │   └── TripDetailsScreen.js
│   │   ├── Car/
│   │   │   ├── CarCatalogScreen.js
│   │   │   └── CarDetailsScreen.js
│   │   ├── Booking/
│   │   │   ├── BookingScreen.js
│   │   │   ├── BookingHistoryScreen.js
│   │   │   └── BookingStatusScreen.js
│   │   └── Profile/
│   │       └── ProfileScreen.js
│   ├── services/
│   │   ├── carService.js       # Car data operations
│   │   └── bookingService.js   # Booking operations
│   └── theme/
│       └── theme.js            # App theme configuration
├── assets/                     # Images and static files
├── FIREBASE_SETUP.md          # Firebase setup instructions
├── DATABASE_SCHEMA.md         # Database structure documentation
└── README.md                  # This file
```

## Installation

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI (`npm install -g expo-cli`)
- iOS Simulator (for Mac) or Android Studio (for Android development)
- Firebase account

### Steps

1. **Extract the ZIP file**
   ```bash
   unzip CarRentalApp.zip
   cd CarRentalApp
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up Firebase**
   - Follow the instructions in `FIREBASE_SETUP.md`
   - Create a Firebase project
   - Enable Authentication (Email/Password)
   - Create Firestore database
   - Update `src/config/firebase.js` with your Firebase credentials

4. **Add sample car data**
   - Follow the instructions in `DATABASE_SCHEMA.md`
   - Add sample cars to your Firestore database

5. **Start the development server**
   ```bash
   npm start
   # or
   expo start
   ```

6. **Run on device/simulator**
   - Press `i` for iOS simulator
   - Press `a` for Android emulator
   - Scan QR code with Expo Go app on your physical device

## Firebase Configuration

1. Open `src/config/firebase.js`
2. Replace the placeholder values with your Firebase project credentials:

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

## Database Setup

The app uses three main Firestore collections:

1. **users** - User profile information
2. **cars** - Car inventory and details
3. **bookings** - Rental bookings and history

Refer to `DATABASE_SCHEMA.md` for detailed schema information and sample data.

## Usage

### For Users

1. **Sign Up / Login**
   - Create a new account or login with existing credentials

2. **Browse Cars**
   - View available cars from the home screen
   - Use filters to narrow down options

3. **Plan Your Trip**
   - Enter trip details (source, destination, passengers, days)
   - Get car recommendations

4. **Book a Car**
   - Select your preferred car
   - Choose rental dates
   - Confirm booking

5. **Track Booking**
   - View booking status in real-time
   - Access booking history
   - Cancel bookings if needed

### For Developers

#### Adding New Features

1. Create new screen components in `src/screens/`
2. Add routes in `src/navigation/MainNavigator.js`
3. Create service functions in `src/services/`
4. Update Firebase security rules as needed

#### Customizing Theme

Edit `src/theme/theme.js` to customize colors and styling:

```javascript
export const colors = {
  primary: '#2196F3',    // Change primary color
  secondary: '#FF9800',  // Change secondary color
  // ... other colors
};
```

## Building for Production

### Android

```bash
expo build:android
```

### iOS

```bash
expo build:ios
```

## Troubleshooting

### Common Issues

1. **Firebase Connection Error**
   - Verify Firebase configuration in `src/config/firebase.js`
   - Check internet connection
   - Ensure Firebase services are enabled

2. **Authentication Failed**
   - Verify Email/Password authentication is enabled in Firebase Console
   - Check security rules in Firestore

3. **App Won't Start**
   - Clear cache: `expo start -c`
   - Reinstall dependencies: `rm -rf node_modules && npm install`

4. **Build Errors**
   - Update Expo CLI: `npm install -g expo-cli`
   - Check for package version conflicts

## Future Enhancements

- [ ] Payment gateway integration
- [ ] Push notifications
- [ ] Google Maps integration for real-time tracking
- [ ] Car reviews and ratings
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Admin panel
- [ ] Advanced analytics
- [ ] Loyalty program
- [ ] Insurance options

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Check `FIREBASE_SETUP.md` for Firebase-related issues
- Check `DATABASE_SCHEMA.md` for database structure
- Review the code comments for implementation details

## Credits

Developed with ❤️ using React Native and Firebase

## Version History

- **v1.0.0** (2024) - Initial release
  - User authentication
  - Car catalog and filtering
  - Trip planning
  - Booking management
  - Status tracking
  - Profile management

---

**Note**: This app is configured to work with Firebase. Make sure to set up your Firebase project and update the configuration before running the app.
