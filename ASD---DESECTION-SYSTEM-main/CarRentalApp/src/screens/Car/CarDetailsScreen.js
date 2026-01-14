import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Text,
  Chip,
  Divider,
} from 'react-native-paper';
import { colors } from '../../theme/theme';

const CarDetailsScreen = ({ navigation, route }) => {
  const { car, tripDetails } = route.params;
  const [estimatedDistance, setEstimatedDistance] = useState(0);
  const [estimatedDuration, setEstimatedDuration] = useState('');
  const [totalPrice, setTotalPrice] = useState(0);

  useEffect(() => {
    calculateEstimates();
  }, []);

  const calculateEstimates = () => {
    if (tripDetails) {
      const distance = Math.floor(Math.random() * 300) + 50;
      const hours = Math.floor(distance / 60);
      const minutes = Math.floor((distance % 60) * 0.6);
      
      setEstimatedDistance(distance);
      setEstimatedDuration(`${hours}h ${minutes}m`);
      setTotalPrice(car.pricePerDay * tripDetails.days);
    }
  };

  const handleBookNow = () => {
    if (!tripDetails) {
      Alert.alert(
        'Trip Details Required',
        'Please enter trip details first',
        [
          {
            text: 'OK',
            onPress: () => navigation.navigate('TripDetails'),
          },
        ]
      );
      return;
    }

    navigation.navigate('Booking', {
      car,
      tripDetails,
      estimatedDistance,
      estimatedDuration,
      totalPrice,
    });
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>
            {car.brand} {car.model}
          </Title>
          <Paragraph style={styles.type}>{car.type}</Paragraph>

          <View style={styles.priceContainer}>
            <Text style={styles.price}>${car.pricePerDay}</Text>
            <Text style={styles.priceLabel}>per day</Text>
          </View>

          <Divider style={styles.divider} />

          <Text style={styles.sectionTitle}>Specifications</Text>
          <View style={styles.specsContainer}>
            <View style={styles.specRow}>
              <Text style={styles.specLabel}>Seating Capacity:</Text>
              <Text style={styles.specValue}>{car.seatingCapacity} persons</Text>
            </View>
            <View style={styles.specRow}>
              <Text style={styles.specLabel}>Fuel Type:</Text>
              <Text style={styles.specValue}>{car.fuelType}</Text>
            </View>
            <View style={styles.specRow}>
              <Text style={styles.specLabel}>Transmission:</Text>
              <Text style={styles.specValue}>{car.transmission}</Text>
            </View>
            <View style={styles.specRow}>
              <Text style={styles.specLabel}>Availability:</Text>
              <Text
                style={[
                  styles.specValue,
                  car.available ? styles.available : styles.unavailable,
                ]}
              >
                {car.available ? 'Available' : 'Not Available'}
              </Text>
            </View>
          </View>

          {tripDetails && (
            <>
              <Divider style={styles.divider} />
              <Text style={styles.sectionTitle}>Trip Information</Text>
              <View style={styles.tripInfo}>
                <View style={styles.tripRow}>
                  <Text style={styles.tripLabel}>Route:</Text>
                  <Text style={styles.tripValue}>
                    {tripDetails.source} → {tripDetails.destination}
                  </Text>
                </View>
                <View style={styles.tripRow}>
                  <Text style={styles.tripLabel}>Passengers:</Text>
                  <Text style={styles.tripValue}>{tripDetails.passengers}</Text>
                </View>
                <View style={styles.tripRow}>
                  <Text style={styles.tripLabel}>Duration:</Text>
                  <Text style={styles.tripValue}>{tripDetails.days} days</Text>
                </View>
                <View style={styles.tripRow}>
                  <Text style={styles.tripLabel}>Est. Distance:</Text>
                  <Text style={styles.tripValue}>{estimatedDistance} km</Text>
                </View>
                <View style={styles.tripRow}>
                  <Text style={styles.tripLabel}>Est. Travel Time:</Text>
                  <Text style={styles.tripValue}>{estimatedDuration}</Text>
                </View>
              </View>

              <Divider style={styles.divider} />
              <View style={styles.totalPriceContainer}>
                <Text style={styles.totalPriceLabel}>Total Rental Cost:</Text>
                <Text style={styles.totalPrice}>${totalPrice}</Text>
              </View>
            </>
          )}

          <Divider style={styles.divider} />
          <Text style={styles.sectionTitle}>Features</Text>
          <View style={styles.featuresContainer}>
            <Chip icon="air-conditioner" style={styles.featureChip}>
              Air Conditioning
            </Chip>
            <Chip icon="airbag" style={styles.featureChip}>
              Airbags
            </Chip>
            <Chip icon="music" style={styles.featureChip}>
              Music System
            </Chip>
            <Chip icon="car-door" style={styles.featureChip}>
              Power Windows
            </Chip>
          </View>
        </Card.Content>
        <Card.Actions style={styles.actions}>
          <Button
            mode="contained"
            onPress={handleBookNow}
            disabled={!car.available}
            style={styles.bookButton}
            contentStyle={styles.bookButtonContent}
          >
            Book Now
          </Button>
        </Card.Actions>
      </Card>

      {tripDetails && car.seatingCapacity >= tripDetails.passengers && (
        <Card style={styles.recommendationCard}>
          <Card.Content>
            <Text style={styles.recommendationIcon}>✓</Text>
            <Title style={styles.recommendationTitle}>Perfect Match!</Title>
            <Paragraph>
              This car is recommended for your trip based on your passenger count
              and journey requirements.
            </Paragraph>
          </Card.Content>
        </Card>
      )}
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
    color: colors.primary,
  },
  type: {
    fontSize: 16,
    color: colors.gray,
    marginBottom: 15,
  },
  priceContainer: {
    alignItems: 'center',
    paddingVertical: 15,
    backgroundColor: colors.light,
    borderRadius: 8,
  },
  price: {
    fontSize: 36,
    fontWeight: 'bold',
    color: colors.primary,
  },
  priceLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  divider: {
    marginVertical: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: colors.dark,
  },
  specsContainer: {
    marginBottom: 10,
  },
  specRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  specLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  specValue: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.dark,
  },
  available: {
    color: colors.success,
  },
  unavailable: {
    color: colors.danger,
  },
  tripInfo: {
    backgroundColor: colors.light,
    padding: 15,
    borderRadius: 8,
  },
  tripRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 5,
  },
  tripLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  tripValue: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.dark,
  },
  totalPriceContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.primary,
    padding: 15,
    borderRadius: 8,
  },
  totalPriceLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.white,
  },
  totalPrice: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.white,
  },
  featuresContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  featureChip: {
    marginRight: 8,
    marginBottom: 8,
  },
  actions: {
    padding: 15,
  },
  bookButton: {
    flex: 1,
  },
  bookButtonContent: {
    paddingVertical: 8,
  },
  recommendationCard: {
    margin: 15,
    marginTop: 0,
    backgroundColor: colors.success,
    elevation: 3,
  },
  recommendationIcon: {
    fontSize: 40,
    textAlign: 'center',
    color: colors.white,
  },
  recommendationTitle: {
    textAlign: 'center',
    color: colors.white,
    marginBottom: 5,
  },
});

export default CarDetailsScreen;
