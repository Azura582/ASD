import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

import HomeScreen from '../screens/Home/HomeScreen';
import TripDetailsScreen from '../screens/Trip/TripDetailsScreen';
import CarCatalogScreen from '../screens/Car/CarCatalogScreen';
import CarDetailsScreen from '../screens/Car/CarDetailsScreen';
import BookingScreen from '../screens/Booking/BookingScreen';
import BookingHistoryScreen from '../screens/Booking/BookingHistoryScreen';
import BookingStatusScreen from '../screens/Booking/BookingStatusScreen';
import ProfileScreen from '../screens/Profile/ProfileScreen';
import { colors } from '../theme/theme';

const Tab = createBottomTabNavigator();
const Stack = createStackNavigator();

const HomeStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="HomeScreen" 
        component={HomeScreen}
        options={{ title: 'Car Rental' }}
      />
      <Stack.Screen 
        name="TripDetails" 
        component={TripDetailsScreen}
        options={{ title: 'Trip Details' }}
      />
      <Stack.Screen 
        name="CarCatalog" 
        component={CarCatalogScreen}
        options={{ title: 'Available Cars' }}
      />
      <Stack.Screen 
        name="CarDetails" 
        component={CarDetailsScreen}
        options={{ title: 'Car Details' }}
      />
      <Stack.Screen 
        name="Booking" 
        component={BookingScreen}
        options={{ title: 'Book Car' }}
      />
      <Stack.Screen 
        name="BookingStatus" 
        component={BookingStatusScreen}
        options={{ title: 'Booking Status' }}
      />
    </Stack.Navigator>
  );
};

const BookingsStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="BookingHistory" 
        component={BookingHistoryScreen}
        options={{ title: 'My Bookings' }}
      />
      <Stack.Screen 
        name="BookingStatus" 
        component={BookingStatusScreen}
        options={{ title: 'Booking Details' }}
      />
    </Stack.Navigator>
  );
};

const ProfileStack = () => {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="ProfileScreen" 
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </Stack.Navigator>
  );
};

const MainNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'Bookings') {
            iconName = focused ? 'calendar-check' : 'calendar-check-outline';
          } else if (route.name === 'Profile') {
            iconName = focused ? 'account' : 'account-outline';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.gray,
        headerShown: false,
      })}
    >
      <Tab.Screen name="Home" component={HomeStack} />
      <Tab.Screen name="Bookings" component={BookingsStack} />
      <Tab.Screen name="Profile" component={ProfileStack} />
    </Tab.Navigator>
  );
};

export default MainNavigator;
