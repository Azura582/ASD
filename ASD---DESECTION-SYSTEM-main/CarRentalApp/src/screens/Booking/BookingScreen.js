import React, { useState } from 'react';
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
  TextInput,
  Divider,
} from 'react-native-paper';
import { Calendar } from 'react-native-calendars';
import { colors } from '../../theme/theme';
import { bookingService } from '../../services/bookingService';
import { useAuth } from '../../context/AuthContext';

const BookingScreen = ({ navigation, route }) => {
  const { car, tripDetails, estimatedDistance, estimatedDuration, totalPrice } = route.params;
  const { user } = useAuth();
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [markedDates, setMarkedDates] = useState({});
  const [loading, setLoading] = useState(false);
  const [notes, setNotes] = useState('');

  const onDayPress = (day) => {
    if (!startDate || (startDate && endDate)) {
      setStartDate(day.dateString);
      setEndDate('');
      setMarkedDates({
        [day.dateString]: {
          startingDay: true,
          color: colors.primary,
          textColor: 'white',
        },
      });
    } else {
      if (day.dateString < startDate) {
        Alert.alert('Error', 'End date cannot be before start date');
        return;
      }
      setEndDate(day.dateString);
      const range = getDateRange(startDate, day.dateString);
      setMarkedDates(range);
    }
  };

  const getDateRange = (start, end) => {
    const dates = {};
    const startDateObj = new Date(start);
    const endDateObj = new Date(end);
    
    dates[start] = { startingDay: true, color: colors.primary, textColor: 'white' };
    
    let currentDate = new Date(startDateObj);
    currentDate.setDate(currentDate.getDate() + 1);
    
    while (currentDate < endDateObj) {
      const dateString = currentDate.toISOString().split('T')[0];
      dates[dateString] = { color: colors.primary, textColor: 'white' };
      currentDate.setDate(currentDate.getDate() + 1);
    }
    
    dates[end] = { endingDay: true, color: colors.primary, textColor: 'white' };
    
    return dates;
  };

  const calculateDays = () => {
    if (!startDate || !endDate) return 0;
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays || 1;
  };

  const handleConfirmBooking = async () => {
    if (!startDate || !endDate) {
      Alert.alert('Error', 'Please select rental dates');
      return;
    }

    const days = calculateDays();
    const finalPrice = car.pricePerDay * days;

    Alert.alert(
      'Confirm Booking',
      `Total: $${finalPrice} for ${days} day(s)\n\nConfirm this booking?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Confirm',
          onPress: async () => {
            setLoading(true);
            const booking = {
              userId: user.uid,
              carId: car.id,
              carDetails: {
                brand: car.brand,
                model: car.model,
                type: car.type,
              },
              tripDetails: {
                ...tripDetails,
                estimatedDistance,
                estimatedDuration,
              },
              startDate,
              endDate,
              days,
              totalPrice: finalPrice,
              notes,
              status: 'confirmed',
              createdAt: new Date().toISOString(),
            };

            const result = await bookingService.createBooking(booking);
            setLoading(false);

            if (result.success) {
              navigation.navigate('BookingStatus', { bookingId: result.bookingId });
            } else {
              Alert.alert('Error', result.error || 'Failed to create booking');
            }
          },
        },
      ]
    );
  };

  const days = calculateDays();
  const finalPrice = days > 0 ? car.pricePerDay * days : totalPrice;

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Booking Details</Title>
          
          <View style={styles.carInfo}>
            <Text style={styles.carName}>
              {car.brand} {car.model}
            </Text>
            <Text style={styles.carType}>{car.type}</Text>
          </View>

          <Divider style={styles.divider} />

          <Text style={styles.sectionTitle}>Trip Information</Text>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Route:</Text>
            <Text style={styles.infoValue}>
              {tripDetails.source} → {tripDetails.destination}
            </Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Passengers:</Text>
            <Text style={styles.infoValue}>{tripDetails.passengers}</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Est. Distance:</Text>
            <Text style={styles.infoValue}>{estimatedDistance} km</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Est. Duration:</Text>
            <Text style={styles.infoValue}>{estimatedDuration}</Text>
          </View>

          <Divider style={styles.divider} />

          <Text style={styles.sectionTitle}>Select Rental Dates</Text>
          <Calendar
            onDayPress={onDayPress}
            markedDates={markedDates}
            markingType={'period'}
            minDate={new Date().toISOString().split('T')[0]}
            theme={{
              selectedDayBackgroundColor: colors.primary,
              todayTextColor: colors.primary,
              arrowColor: colors.primary,
            }}
          />

          {startDate && endDate && (
            <View style={styles.dateInfo}>
              <Text style={styles.dateText}>
                From: {startDate} To: {endDate}
              </Text>
              <Text style={styles.daysText}>{days} day(s)</Text>
            </View>
          )}

          <Divider style={styles.divider} />

          <TextInput
            label="Additional Notes (Optional)"
            value={notes}
            onChangeText={setNotes}
            mode="outlined"
            multiline
            numberOfLines={3}
            style={styles.notesInput}
            placeholder="Any special requests or notes..."
          />

          <Divider style={styles.divider} />

          <View style={styles.priceBreakdown}>
            <Text style={styles.breakdownTitle}>Price Breakdown</Text>
            <View style={styles.breakdownRow}>
              <Text style={styles.breakdownLabel}>Price per day:</Text>
              <Text style={styles.breakdownValue}>${car.pricePerDay}</Text>
            </View>
            <View style={styles.breakdownRow}>
              <Text style={styles.breakdownLabel}>Number of days:</Text>
              <Text style={styles.breakdownValue}>{days || tripDetails.days}</Text>
            </View>
            <Divider style={styles.divider} />
            <View style={styles.totalRow}>
              <Text style={styles.totalLabel}>Total Amount:</Text>
              <Text style={styles.totalValue}>${finalPrice}</Text>
            </View>
          </View>
        </Card.Content>
        <Card.Actions style={styles.actions}>
          <Button
            mode="contained"
            onPress={handleConfirmBooking}
            loading={loading}
            disabled={loading || !startDate || !endDate}
            style={styles.confirmButton}
            contentStyle={styles.confirmButtonContent}
          >
            Confirm Booking
          </Button>
        </Card.Actions>
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
    color: colors.primary,
    marginBottom: 15,
  },
  carInfo: {
    backgroundColor: colors.light,
    padding: 15,
    borderRadius: 8,
  },
  carName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.dark,
  },
  carType: {
    fontSize: 14,
    color: colors.gray,
  },
  divider: {
    marginVertical: 15,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: colors.dark,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 5,
  },
  infoLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  infoValue: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.dark,
  },
  dateInfo: {
    marginTop: 15,
    padding: 15,
    backgroundColor: colors.light,
    borderRadius: 8,
  },
  dateText: {
    fontSize: 14,
    color: colors.dark,
    marginBottom: 5,
  },
  daysText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.primary,
  },
  notesInput: {
    marginTop: 10,
  },
  priceBreakdown: {
    backgroundColor: colors.light,
    padding: 15,
    borderRadius: 8,
  },
  breakdownTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: colors.dark,
  },
  breakdownRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 5,
  },
  breakdownLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  breakdownValue: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.dark,
  },
  totalRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingTop: 10,
  },
  totalLabel: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.dark,
  },
  totalValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.primary,
  },
  actions: {
    padding: 15,
  },
  confirmButton: {
    flex: 1,
  },
  confirmButtonContent: {
    paddingVertical: 8,
  },
});

export default BookingScreen;
