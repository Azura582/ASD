import { db } from '../config/firebase';
import {
  collection,
  getDocs,
  getDoc,
  doc,
  query,
  where,
  orderBy,
  addDoc,
  updateDoc,
  deleteDoc,
} from 'firebase/firestore';

// Sample car data for demonstration
const sampleCars = [
  {
    id: '1',
    brand: 'Toyota',
    model: 'Camry',
    type: 'Sedan',
    seatingCapacity: 5,
    fuelType: 'Petrol',
    transmission: 'Automatic',
    pricePerDay: 45,
    available: true,
  },
  {
    id: '2',
    brand: 'Honda',
    model: 'CR-V',
    type: 'SUV',
    seatingCapacity: 7,
    fuelType: 'Diesel',
    transmission: 'Automatic',
    pricePerDay: 65,
    available: true,
  },
  {
    id: '3',
    brand: 'Ford',
    model: 'Mustang',
    type: 'Sports',
    seatingCapacity: 4,
    fuelType: 'Petrol',
    transmission: 'Manual',
    pricePerDay: 85,
    available: true,
  },
  {
    id: '4',
    brand: 'Tesla',
    model: 'Model 3',
    type: 'Electric',
    seatingCapacity: 5,
    fuelType: 'Electric',
    transmission: 'Automatic',
    pricePerDay: 95,
    available: true,
  },
  {
    id: '5',
    brand: 'BMW',
    model: 'X5',
    type: 'SUV',
    seatingCapacity: 7,
    fuelType: 'Diesel',
    transmission: 'Automatic',
    pricePerDay: 120,
    available: true,
  },
  {
    id: '6',
    brand: 'Hyundai',
    model: 'i20',
    type: 'Hatchback',
    seatingCapacity: 5,
    fuelType: 'Petrol',
    transmission: 'Manual',
    pricePerDay: 30,
    available: true,
  },
  {
    id: '7',
    brand: 'Mercedes',
    model: 'E-Class',
    type: 'Luxury',
    seatingCapacity: 5,
    fuelType: 'Diesel',
    transmission: 'Automatic',
    pricePerDay: 150,
    available: false,
  },
  {
    id: '8',
    brand: 'Volkswagen',
    model: 'Polo',
    type: 'Hatchback',
    seatingCapacity: 5,
    fuelType: 'Petrol',
    transmission: 'Manual',
    pricePerDay: 35,
    available: true,
  },
];

export const carService = {
  // Get all cars
  getAllCars: async () => {
    try {
      // TODO: Replace with actual Firebase query
      // const carsRef = collection(db, 'cars');
      // const snapshot = await getDocs(carsRef);
      // const cars = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      // return cars;
      
      // For now, return sample data
      return sampleCars;
    } catch (error) {
      console.error('Error fetching cars:', error);
      return [];
    }
  },

  // Get car by ID
  getCarById: async (carId) => {
    try {
      // TODO: Replace with actual Firebase query
      // const carRef = doc(db, 'cars', carId);
      // const carDoc = await getDoc(carRef);
      // if (carDoc.exists()) {
      //   return { id: carDoc.id, ...carDoc.data() };
      // }
      // return null;
      
      // For now, return from sample data
      return sampleCars.find(car => car.id === carId) || null;
    } catch (error) {
      console.error('Error fetching car:', error);
      return null;
    }
  },

  // Filter cars by criteria
  filterCars: async (filters) => {
    try {
      // TODO: Implement Firebase query with filters
      let filtered = [...sampleCars];

      if (filters.fuelType) {
        filtered = filtered.filter(car => car.fuelType === filters.fuelType);
      }

      if (filters.transmission) {
        filtered = filtered.filter(car => car.transmission === filters.transmission);
      }

      if (filters.minPrice !== undefined && filters.maxPrice !== undefined) {
        filtered = filtered.filter(
          car => car.pricePerDay >= filters.minPrice && car.pricePerDay <= filters.maxPrice
        );
      }

      if (filters.seatingCapacity) {
        filtered = filtered.filter(car => car.seatingCapacity >= filters.seatingCapacity);
      }

      if (filters.available !== undefined) {
        filtered = filtered.filter(car => car.available === filters.available);
      }

      return filtered;
    } catch (error) {
      console.error('Error filtering cars:', error);
      return [];
    }
  },

  // Add a new car (Admin function)
  addCar: async (carData) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const carsRef = collection(db, 'cars');
      // const docRef = await addDoc(carsRef, carData);
      // return { success: true, carId: docRef.id };
      
      return { success: true, carId: 'new-car-id' };
    } catch (error) {
      console.error('Error adding car:', error);
      return { success: false, error: error.message };
    }
  },

  // Update car details (Admin function)
  updateCar: async (carId, updates) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const carRef = doc(db, 'cars', carId);
      // await updateDoc(carRef, updates);
      // return { success: true };
      
      return { success: true };
    } catch (error) {
      console.error('Error updating car:', error);
      return { success: false, error: error.message };
    }
  },

  // Delete car (Admin function)
  deleteCar: async (carId) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const carRef = doc(db, 'cars', carId);
      // await deleteDoc(carRef);
      // return { success: true };
      
      return { success: true };
    } catch (error) {
      console.error('Error deleting car:', error);
      return { success: false, error: error.message };
    }
  },

  // Check car availability for specific dates
  checkAvailability: async (carId, startDate, endDate) => {
    try {
      // TODO: Implement availability check against bookings
      // Query bookings collection for overlapping dates
      return { available: true };
    } catch (error) {
      console.error('Error checking availability:', error);
      return { available: false };
    }
  },
};
