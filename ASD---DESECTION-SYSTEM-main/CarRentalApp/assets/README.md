# Assets Directory

This directory contains static assets for the Car Rental App.

## Required Assets

To complete the app setup, you need to add the following image files:

### App Icons

1. **icon.png** (1024x1024 px)
   - Main app icon
   - Used for app stores and home screen

2. **adaptive-icon.png** (1024x1024 px)
   - Android adaptive icon
   - Foreground layer for Android

3. **splash.png** (1242x2436 px)
   - Splash screen image
   - Shown when app is loading

4. **favicon.png** (48x48 px)
   - Web favicon
   - Used for web version

## Generating Assets

You can use the following tools to generate app icons:

1. **Expo Asset Generator**
   - Use `expo-asset-generator` package
   - Automatically generates all required sizes

2. **Online Tools**
   - https://appicon.co/
   - https://makeappicon.com/
   - https://icon.kitchen/

## Adding Custom Assets

### Car Images

To add car images:

1. Create a `cars/` subdirectory
2. Add car images with descriptive names
3. Update car data in Firestore with image URLs
4. Or use Firebase Storage to host images

### User Avatars

To add default avatars:

1. Create an `avatars/` subdirectory
2. Add default avatar images
3. Reference in user profile screens

## Asset Guidelines

- **Format**: PNG with transparency
- **Quality**: High resolution for better display
- **Size**: Optimize for mobile (compress images)
- **Naming**: Use lowercase with hyphens (e.g., `car-sedan.png`)

## Current Status

This is a placeholder directory. Add your actual assets here before building for production.
