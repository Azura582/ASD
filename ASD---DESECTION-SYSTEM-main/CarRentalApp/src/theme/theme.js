import { DefaultTheme } from 'react-native-paper';

export const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#2196F3',
    accent: '#FF9800',
    background: '#F5F5F5',
    surface: '#FFFFFF',
    text: '#212121',
    error: '#F44336',
    success: '#4CAF50',
    warning: '#FFC107',
    disabled: '#BDBDBD',
    placeholder: '#9E9E9E',
    backdrop: 'rgba(0, 0, 0, 0.5)',
  },
  roundness: 8,
};

export const colors = {
  primary: '#2196F3',
  secondary: '#FF9800',
  success: '#4CAF50',
  danger: '#F44336',
  warning: '#FFC107',
  info: '#00BCD4',
  light: '#F5F5F5',
  dark: '#212121',
  white: '#FFFFFF',
  gray: '#9E9E9E',
};
