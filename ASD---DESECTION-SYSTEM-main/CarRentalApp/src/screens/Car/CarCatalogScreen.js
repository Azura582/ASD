import React, { useState, useEffect } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Text,
  Chip,
  Searchbar,
  Menu,
  Divider,
} from 'react-native-paper';
import { colors } from '../../theme/theme';
import { carService } from '../../services/carService';

const CarCatalogScreen = ({ navigation, route }) => {
  const [cars, setCars] = useState([]);
  const [filteredCars, setFilteredCars] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterMenuVisible, setFilterMenuVisible] = useState(false);
  const [selectedFuelType, setSelectedFuelType] = useState('All');
  const [selectedTransmission, setSelectedTransmission] = useState('All');
  const [priceRange, setPriceRange] = useState('All');
  
  const tripDetails = route.params?.tripDetails;

  useEffect(() => {
    loadCars();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [cars, searchQuery, selectedFuelType, selectedTransmission, priceRange]);

  const loadCars = async () => {
    const carsData = await carService.getAllCars();
    setCars(carsData);
    setFilteredCars(carsData);
  };

  const applyFilters = () => {
    let filtered = [...cars];

    if (searchQuery) {
      filtered = filtered.filter(
        (car) =>
          car.model.toLowerCase().includes(searchQuery.toLowerCase()) ||
          car.brand.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    if (selectedFuelType !== 'All') {
      filtered = filtered.filter((car) => car.fuelType === selectedFuelType);
    }

    if (selectedTransmission !== 'All') {
      filtered = filtered.filter((car) => car.transmission === selectedTransmission);
    }

    if (priceRange !== 'All') {
      const [min, max] = priceRange.split('-').map(Number);
      filtered = filtered.filter((car) => {
        if (max) {
          return car.pricePerDay >= min && car.pricePerDay <= max;
        }
        return car.pricePerDay >= min;
      });
    }

    if (tripDetails?.passengers) {
      filtered = filtered.filter((car) => car.seatingCapacity >= tripDetails.passengers);
    }

    setFilteredCars(filtered);
  };

  const clearFilters = () => {
    setSelectedFuelType('All');
    setSelectedTransmission('All');
    setPriceRange('All');
    setSearchQuery('');
  };

  const renderCarCard = (car) => (
    <Card key={car.id} style={styles.carCard}>
      <Card.Content>
        <View style={styles.carHeader}>
          <View style={styles.carInfo}>
            <Title style={styles.carTitle}>{car.brand} {car.model}</Title>
            <Paragraph style={styles.carType}>{car.type}</Paragraph>
          </View>
          <View style={styles.priceContainer}>
            <Text style={styles.price}>${car.pricePerDay}</Text>
            <Text style={styles.priceLabel}>per day</Text>
          </View>
        </View>

        <View style={styles.chipsContainer}>
          <Chip icon="car-seat" style={styles.chip} textStyle={styles.chipText}>
            {car.seatingCapacity} Seats
          </Chip>
          <Chip icon="gas-station" style={styles.chip} textStyle={styles.chipText}>
            {car.fuelType}
          </Chip>
          <Chip icon="car-shift-pattern" style={styles.chip} textStyle={styles.chipText}>
            {car.transmission}
          </Chip>
        </View>

        <View style={styles.availabilityContainer}>
          <Text
            style={[
              styles.availabilityText,
              car.available ? styles.available : styles.unavailable,
            ]}
          >
            {car.available ? '✓ Available' : '✗ Not Available'}
          </Text>
        </View>
      </Card.Content>
      <Card.Actions>
        <Button
          mode="contained"
          onPress={() => navigation.navigate('CarDetails', { car, tripDetails })}
          disabled={!car.available}
        >
          View Details
        </Button>
      </Card.Actions>
    </Card>
  );

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Searchbar
          placeholder="Search cars..."
          onChangeText={setSearchQuery}
          value={searchQuery}
          style={styles.searchbar}
        />
      </View>

      <View style={styles.filterContainer}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          <Chip
            selected={selectedFuelType !== 'All'}
            onPress={() => setSelectedFuelType(selectedFuelType === 'All' ? 'Petrol' : 'All')}
            style={styles.filterChip}
          >
            Fuel: {selectedFuelType}
          </Chip>
          <Chip
            selected={selectedTransmission !== 'All'}
            onPress={() =>
              setSelectedTransmission(selectedTransmission === 'All' ? 'Automatic' : 'All')
            }
            style={styles.filterChip}
          >
            Transmission: {selectedTransmission}
          </Chip>
          <Chip
            selected={priceRange !== 'All'}
            onPress={() => setPriceRange(priceRange === 'All' ? '0-50' : 'All')}
            style={styles.filterChip}
          >
            Price: {priceRange === 'All' ? 'All' : `$${priceRange}`}
          </Chip>
          <Button mode="text" onPress={clearFilters} compact>
            Clear All
          </Button>
        </ScrollView>
      </View>

      {tripDetails && (
        <Card style={styles.tripCard}>
          <Card.Content>
            <Text style={styles.tripTitle}>Trip Details</Text>
            <Text style={styles.tripText}>
              {tripDetails.source} → {tripDetails.destination}
            </Text>
            <Text style={styles.tripText}>
              {tripDetails.passengers} passengers • {tripDetails.days} days
            </Text>
          </Card.Content>
        </Card>
      )}

      <ScrollView style={styles.carsList}>
        <Text style={styles.resultsText}>
          {filteredCars.length} car{filteredCars.length !== 1 ? 's' : ''} found
        </Text>
        {filteredCars.map(renderCarCard)}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.light,
  },
  searchContainer: {
    padding: 15,
    paddingBottom: 10,
  },
  searchbar: {
    elevation: 2,
  },
  filterContainer: {
    paddingHorizontal: 15,
    paddingBottom: 10,
  },
  filterChip: {
    marginRight: 8,
  },
  tripCard: {
    margin: 15,
    marginTop: 0,
    backgroundColor: colors.primary,
  },
  tripTitle: {
    color: colors.white,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  tripText: {
    color: colors.white,
    fontSize: 12,
  },
  carsList: {
    flex: 1,
    padding: 15,
    paddingTop: 0,
  },
  resultsText: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 10,
  },
  carCard: {
    marginBottom: 15,
    elevation: 3,
  },
  carHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 10,
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
  priceContainer: {
    alignItems: 'flex-end',
  },
  price: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.primary,
  },
  priceLabel: {
    fontSize: 12,
    color: colors.gray,
  },
  chipsContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: 10,
  },
  chip: {
    marginRight: 8,
    marginBottom: 8,
  },
  chipText: {
    fontSize: 12,
  },
  availabilityContainer: {
    marginTop: 5,
  },
  availabilityText: {
    fontSize: 14,
    fontWeight: 'bold',
  },
  available: {
    color: colors.success,
  },
  unavailable: {
    color: colors.danger,
  },
});

export default CarCatalogScreen;
