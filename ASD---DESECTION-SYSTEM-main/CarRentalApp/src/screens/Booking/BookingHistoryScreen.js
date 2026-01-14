import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Text,
  Chip,
  ActivityIndicator,
} from 'react-native-paper';
import { colors } from '../../theme/theme';
import { bookingService } from '../../services/bookingService';
import { useAuth } from '../../context/AuthContext';

const BookingHistoryScreen = ({ navigation }) => {
  const { user } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadBookings();
  }, []);

  const loadBookings = async () => {
    setLoading(true);
    const result = await bookingService.getUserBookings(user.uid);
    if (result.success) {
      setBookings(result.bookings);
    }
    setLoading(false);
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadBookings();
    setRefreshing(false);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return colors.success;
      case 'ready':
        return colors.info;
      case 'ongoing':
        return colors.warning;
      case 'completed':
        return colors.primary;
      case 'cancelled':
        return colors.danger;
      default:
        return colors.gray;
    }
  };

  const getStatusLabel = (status) => {
    switch (status) {
      case 'confirmed':
        return 'Booking Confirmed';
      case 'ready':
        return 'Ready for Pickup';
      case 'ongoing':
        return 'Rental Ongoing';
      case 'completed':
        return 'Rental Completed';
      case 'cancelled':
        return 'Cancelled';
      default:
        return status;
    }
  };

  const renderBookingCard = (booking) => (
    <TouchableOpacity
      key={booking.id}
      onPress={() => navigation.navigate('BookingStatus', { bookingId: booking.id })}
    >
      <Card style={styles.bookingCard}>
        <Card.Content>
          <View style={styles.cardHeader}>
            <View style={styles.carInfo}>
              <Title style={styles.carTitle}>
                {booking.carDetails.brand} {booking.carDetails.model}
              </Title>
              <Paragraph style={styles.carType}>{booking.carDetails.type}</Paragraph>
            </View>
            <Chip
              style={[styles.statusChip, { backgroundColor: getStatusColor(booking.status) }]}
              textStyle={styles.statusText}
            >
              {getStatusLabel(booking.status)}
            </Chip>
          </View>

          <View style={styles.bookingDetails}>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>📍 Route:</Text>
              <Text style={styles.detailValue}>
                {booking.tripDetails.source} → {booking.tripDetails.destination}
              </Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>📅 Dates:</Text>
              <Text style={styles.detailValue}>
                {booking.startDate} to {booking.endDate}
              </Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>⏱️ Duration:</Text>
              <Text style={styles.detailValue}>{booking.days} days</Text>
            </View>
            <View style={styles.detailRow}>
              <Text style={styles.detailLabel}>💰 Total:</Text>
              <Text style={styles.priceValue}>${booking.totalPrice}</Text>
            </View>
          </View>
        </Card.Content>
      </Card>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.loadingText}>Loading bookings...</Text>
      </View>
    );
  }

  if (bookings.length === 0) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyIcon}>📋</Text>
        <Title style={styles.emptyTitle}>No Bookings Yet</Title>
        <Paragraph style={styles.emptyText}>
          Your booking history will appear here
        </Paragraph>
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      <View style={styles.header}>
        <Title style={styles.headerTitle}>My Bookings</Title>
        <Text style={styles.headerSubtitle}>
          {bookings.length} booking{bookings.length !== 1 ? 's' : ''}
        </Text>
      </View>
      {bookings.map(renderBookingCard)}
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
  emptyIcon: {
    fontSize: 64,
    marginBottom: 15,
  },
  emptyTitle: {
    fontSize: 20,
    marginBottom: 10,
  },
  emptyText: {
    textAlign: 'center',
    color: colors.gray,
  },
  header: {
    padding: 15,
    backgroundColor: colors.white,
    borderBottomWidth: 1,
    borderBottomColor: colors.light,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  headerSubtitle: {
    fontSize: 14,
    color: colors.gray,
  },
  bookingCard: {
    margin: 15,
    marginTop: 10,
    elevation: 3,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 15,
  },
  carInfo: {
    flex: 1,
  },
  carTitle: {
    fontSize: 18,
    marginBottom: 2,
  },
  carType: {
    fontSize: 14,
    color: colors.gray,
  },
  statusChip: {
    marginLeft: 10,
  },
  statusText: {
    color: colors.white,
    fontSize: 12,
    fontWeight: 'bold',
  },
  bookingDetails: {
    backgroundColor: colors.light,
    padding: 12,
    borderRadius: 8,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 4,
  },
  detailLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.dark,
    textAlign: 'right',
    flex: 1,
    marginLeft: 10,
  },
  priceValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.primary,
  },
});

export default BookingHistoryScreen;
