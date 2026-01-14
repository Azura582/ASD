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
  Divider,
  ActivityIndicator,
  Chip,
} from 'react-native-paper';
import { colors } from '../../theme/theme';
import { bookingService } from '../../services/bookingService';

const BookingStatusScreen = ({ navigation, route }) => {
  const { bookingId } = route.params;
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadBooking();
  }, []);

  const loadBooking = async () => {
    setLoading(true);
    const result = await bookingService.getBookingById(bookingId);
    if (result.success) {
      setBooking(result.booking);
    }
    setLoading(false);
  };

  const handleCancelBooking = () => {
    Alert.alert(
      'Cancel Booking',
      'Are you sure you want to cancel this booking?',
      [
        { text: 'No', style: 'cancel' },
        {
          text: 'Yes, Cancel',
          style: 'destructive',
          onPress: async () => {
            const result = await bookingService.updateBookingStatus(bookingId, 'cancelled');
            if (result.success) {
              Alert.alert('Success', 'Booking cancelled successfully');
              loadBooking();
            } else {
              Alert.alert('Error', 'Failed to cancel booking');
            }
          },
        },
      ]
    );
  };

  const getStatusInfo = (status) => {
    switch (status) {
      case 'confirmed':
        return {
          color: colors.success,
          icon: '✓',
          title: 'Booking Confirmed',
          description: 'Your booking has been confirmed. The car will be ready for pickup on the start date.',
        };
      case 'ready':
        return {
          color: colors.info,
          icon: '🚗',
          title: 'Ready for Pickup',
          description: 'Your car is ready! Please visit the pickup location to collect your vehicle.',
        };
      case 'ongoing':
        return {
          color: colors.warning,
          icon: '🔄',
          title: 'Rental Ongoing',
          description: 'Enjoy your ride! Please return the car by the end date.',
        };
      case 'completed':
        return {
          color: colors.primary,
          icon: '✔',
          title: 'Rental Completed',
          description: 'Thank you for choosing us! We hope you had a great experience.',
        };
      case 'cancelled':
        return {
          color: colors.danger,
          icon: '✗',
          title: 'Booking Cancelled',
          description: 'This booking has been cancelled.',
        };
      default:
        return {
          color: colors.gray,
          icon: '?',
          title: 'Unknown Status',
          description: '',
        };
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>Loading booking details...</Text>
      </View>
    );
  }

  if (!booking) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.errorIcon}>⚠️</Text>
        <Title>Booking Not Found</Title>
        <Button mode="contained" onPress={() => navigation.goBack()} style={styles.backButton}>
          Go Back
        </Button>
      </View>
    );
  }

  const statusInfo = getStatusInfo(booking.status);

  return (
    <ScrollView style={styles.container}>
      <Card style={[styles.statusCard, { backgroundColor: statusInfo.color }]}>
        <Card.Content>
          <Text style={styles.statusIcon}>{statusInfo.icon}</Text>
          <Title style={styles.statusTitle}>{statusInfo.title}</Title>
          <Paragraph style={styles.statusDescription}>{statusInfo.description}</Paragraph>
        </Card.Content>
      </Card>

      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.sectionTitle}>Booking Information</Title>
          
          <View style={styles.infoSection}>
            <Text style={styles.label}>Booking ID:</Text>
            <Text style={styles.value}>{booking.id}</Text>
          </View>

          <View style={styles.infoSection}>
            <Text style={styles.label}>Booking Date:</Text>
            <Text style={styles.value}>
              {new Date(booking.createdAt).toLocaleDateString()}
            </Text>
          </View>

          <Divider style={styles.divider} />

          <Title style={styles.sectionTitle}>Car Details</Title>
          <View style={styles.carDetails}>
            <Text style={styles.carName}>
              {booking.carDetails.brand} {booking.carDetails.model}
            </Text>
            <Text style={styles.carType}>{booking.carDetails.type}</Text>
          </View>

          <Divider style={styles.divider} />

          <Title style={styles.sectionTitle}>Trip Details</Title>
          <View style={styles.infoSection}>
            <Text style={styles.label}>Route:</Text>
            <Text style={styles.value}>
              {booking.tripDetails.source} → {booking.tripDetails.destination}
            </Text>
          </View>
          <View style={styles.infoSection}>
            <Text style={styles.label}>Passengers:</Text>
            <Text style={styles.value}>{booking.tripDetails.passengers}</Text>
          </View>
          <View style={styles.infoSection}>
            <Text style={styles.label}>Est. Distance:</Text>
            <Text style={styles.value}>{booking.tripDetails.estimatedDistance} km</Text>
          </View>
          <View style={styles.infoSection}>
            <Text style={styles.label}>Est. Duration:</Text>
            <Text style={styles.value}>{booking.tripDetails.estimatedDuration}</Text>
          </View>

          <Divider style={styles.divider} />

          <Title style={styles.sectionTitle}>Rental Period</Title>
          <View style={styles.infoSection}>
            <Text style={styles.label}>Start Date:</Text>
            <Text style={styles.value}>{booking.startDate}</Text>
          </View>
          <View style={styles.infoSection}>
            <Text style={styles.label}>End Date:</Text>
            <Text style={styles.value}>{booking.endDate}</Text>
          </View>
          <View style={styles.infoSection}>
            <Text style={styles.label}>Duration:</Text>
            <Text style={styles.value}>{booking.days} days</Text>
          </View>

          {booking.notes && (
            <>
              <Divider style={styles.divider} />
              <Title style={styles.sectionTitle}>Additional Notes</Title>
              <Text style={styles.notes}>{booking.notes}</Text>
            </>
          )}

          <Divider style={styles.divider} />

          <View style={styles.totalContainer}>
            <Text style={styles.totalLabel}>Total Amount:</Text>
            <Text style={styles.totalValue}>${booking.totalPrice}</Text>
          </View>
        </Card.Content>

        {booking.status === 'confirmed' && (
          <Card.Actions style={styles.actions}>
            <Button
              mode="outlined"
              onPress={handleCancelBooking}
              textColor={colors.danger}
              style={styles.cancelButton}
            >
              Cancel Booking
            </Button>
          </Card.Actions>
        )}
      </Card>

      <Card style={styles.timelineCard}>
        <Card.Content>
          <Title style={styles.sectionTitle}>Booking Timeline</Title>
          
          <View style={styles.timelineItem}>
            <View style={[styles.timelineDot, { backgroundColor: colors.success }]} />
            <View style={styles.timelineContent}>
              <Text style={styles.timelineTitle}>Booking Confirmed</Text>
              <Text style={styles.timelineDate}>
                {new Date(booking.createdAt).toLocaleString()}
              </Text>
            </View>
          </View>

          {booking.status !== 'cancelled' && (
            <>
              <View style={styles.timelineItem}>
                <View
                  style={[
                    styles.timelineDot,
                    {
                      backgroundColor:
                        booking.status === 'ready' ||
                        booking.status === 'ongoing' ||
                        booking.status === 'completed'
                          ? colors.info
                          : colors.gray,
                    },
                  ]}
                />
                <View style={styles.timelineContent}>
                  <Text style={styles.timelineTitle}>Ready for Pickup</Text>
                  <Text style={styles.timelineDate}>
                    {booking.status === 'confirmed' ? 'Pending' : 'Completed'}
                  </Text>
                </View>
              </View>

              <View style={styles.timelineItem}>
                <View
                  style={[
                    styles.timelineDot,
                    {
                      backgroundColor:
                        booking.status === 'ongoing' || booking.status === 'completed'
                          ? colors.warning
                          : colors.gray,
                    },
                  ]}
                />
                <View style={styles.timelineContent}>
                  <Text style={styles.timelineTitle}>Rental Ongoing</Text>
                  <Text style={styles.timelineDate}>
                    {booking.status === 'ongoing' || booking.status === 'completed'
                      ? 'In Progress'
                      : 'Pending'}
                  </Text>
                </View>
              </View>

              <View style={styles.timelineItem}>
                <View
                  style={[
                    styles.timelineDot,
                    {
                      backgroundColor:
                        booking.status === 'completed' ? colors.primary : colors.gray,
                    },
                  ]}
                />
                <View style={styles.timelineContent}>
                  <Text style={styles.timelineTitle}>Rental Completed</Text>
                  <Text style={styles.timelineDate}>
                    {booking.status === 'completed' ? 'Completed' : 'Pending'}
                  </Text>
                </View>
              </View>
            </>
          )}

          {booking.status === 'cancelled' && (
            <View style={styles.timelineItem}>
              <View style={[styles.timelineDot, { backgroundColor: colors.danger }]} />
              <View style={styles.timelineContent}>
                <Text style={styles.timelineTitle}>Booking Cancelled</Text>
                <Text style={styles.timelineDate}>Cancelled</Text>
              </View>
            </View>
          )}
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
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: colors.light,
    padding: 20,
  },
  loadingText: {
    marginTop: 10,
    color: colors.gray,
  },
  errorIcon: {
    fontSize: 64,
    marginBottom: 15,
  },
  backButton: {
    marginTop: 20,
  },
  statusCard: {
    margin: 15,
    elevation: 4,
  },
  statusIcon: {
    fontSize: 48,
    textAlign: 'center',
    color: colors.white,
  },
  statusTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
    color: colors.white,
    marginTop: 10,
  },
  statusDescription: {
    textAlign: 'center',
    color: colors.white,
    marginTop: 5,
  },
  card: {
    margin: 15,
    marginTop: 0,
    elevation: 4,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: colors.dark,
  },
  infoSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  label: {
    fontSize: 14,
    color: colors.gray,
  },
  value: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.dark,
    textAlign: 'right',
    flex: 1,
    marginLeft: 10,
  },
  carDetails: {
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
  notes: {
    fontSize: 14,
    color: colors.dark,
    fontStyle: 'italic',
    backgroundColor: colors.light,
    padding: 10,
    borderRadius: 8,
  },
  divider: {
    marginVertical: 15,
  },
  totalContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: colors.primary,
    padding: 15,
    borderRadius: 8,
  },
  totalLabel: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
  },
  totalValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.white,
  },
  actions: {
    padding: 15,
  },
  cancelButton: {
    flex: 1,
    borderColor: colors.danger,
  },
  timelineCard: {
    margin: 15,
    marginTop: 0,
    elevation: 3,
  },
  timelineItem: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  timelineDot: {
    width: 16,
    height: 16,
    borderRadius: 8,
    marginRight: 15,
    marginTop: 2,
  },
  timelineContent: {
    flex: 1,
  },
  timelineTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.dark,
  },
  timelineDate: {
    fontSize: 12,
    color: colors.gray,
    marginTop: 2,
  },
});

export default BookingStatusScreen;
