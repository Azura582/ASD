import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import { TextInput, Button, Title, Text, Card } from 'react-native-paper';
import { colors } from '../../theme/theme';

const TripDetailsScreen = ({ navigation }) => {
  const [source, setSource] = useState('');
  const [destination, setDestination] = useState('');
  const [passengers, setPassengers] = useState('');
  const [days, setDays] = useState('');

  const handleSearch = () => {
    if (!source || !destination || !passengers || !days) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    const passengersNum = parseInt(passengers);
    const daysNum = parseInt(days);

    if (isNaN(passengersNum) || passengersNum < 1) {
      Alert.alert('Error', 'Please enter a valid number of passengers');
      return;
    }

    if (isNaN(daysNum) || daysNum < 1) {
      Alert.alert('Error', 'Please enter a valid number of days');
      return;
    }

    const tripDetails = {
      source,
      destination,
      passengers: passengersNum,
      days: daysNum,
    };

    navigation.navigate('CarCatalog', { tripDetails });
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Enter Trip Details</Title>
          <Text style={styles.subtitle}>
            Tell us about your journey to find the perfect car
          </Text>

          <TextInput
            label="Pickup Location"
            value={source}
            onChangeText={setSource}
            mode="outlined"
            style={styles.input}
            left={<TextInput.Icon icon="map-marker" />}
            placeholder="Enter pickup location"
          />

          <TextInput
            label="Drop-off Location"
            value={destination}
            onChangeText={setDestination}
            mode="outlined"
            style={styles.input}
            left={<TextInput.Icon icon="map-marker-check" />}
            placeholder="Enter drop-off location"
          />

          <TextInput
            label="Number of Passengers"
            value={passengers}
            onChangeText={setPassengers}
            mode="outlined"
            keyboardType="numeric"
            style={styles.input}
            left={<TextInput.Icon icon="account-group" />}
            placeholder="Enter number of passengers"
          />

          <TextInput
            label="Number of Days"
            value={days}
            onChangeText={setDays}
            mode="outlined"
            keyboardType="numeric"
            style={styles.input}
            left={<TextInput.Icon icon="calendar-range" />}
            placeholder="Enter rental duration"
          />

          <Button
            mode="contained"
            onPress={handleSearch}
            style={styles.button}
            contentStyle={styles.buttonContent}
          >
            Search Cars
          </Button>
        </Card.Content>
      </Card>

      <Card style={styles.infoCard}>
        <Card.Content>
          <Title style={styles.infoTitle}>Quick Tips</Title>
          <View style={styles.tipContainer}>
            <Text style={styles.tipIcon}>💡</Text>
            <Text style={styles.tipText}>
              We'll recommend cars based on your passenger count
            </Text>
          </View>
          <View style={styles.tipContainer}>
            <Text style={styles.tipIcon}>📍</Text>
            <Text style={styles.tipText}>
              Distance will be calculated for accurate pricing
            </Text>
          </View>
          <View style={styles.tipContainer}>
            <Text style={styles.tipIcon}>⏰</Text>
            <Text style={styles.tipText}>
              Longer rentals may qualify for discounts
            </Text>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.light,
  },
  card: {
    margin: 15,
    elevation: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
    color: colors.primary,
  },
  subtitle: {
    fontSize: 14,
    marginBottom: 20,
    color: colors.gray,
  },
  input: {
    marginBottom: 15,
  },
  button: {
    marginTop: 10,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  infoCard: {
    margin: 15,
    marginTop: 0,
    elevation: 2,
  },
  infoTitle: {
    fontSize: 18,
    marginBottom: 15,
  },
  tipContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  tipIcon: {
    fontSize: 24,
    marginRight: 10,
  },
  tipText: {
    flex: 1,
    fontSize: 14,
    color: colors.dark,
  },
});

export default TripDetailsScreen;
