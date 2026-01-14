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

// Sample bookings for demonstration
let sampleBookings = [];

export const bookingService = {
  // Create a new booking
  createBooking: async (bookingData) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const bookingsRef = collection(db, 'bookings');
      // const docRef = await addDoc(bookingsRef, bookingData);
      // return { success: true, bookingId: docRef.id };
      
      // For now, use local storage
      const bookingId = `booking-${Date.now()}`;
      const newBooking = {
        id: bookingId,
        ...bookingData,
      };
      sampleBookings.push(newBooking);
      return { success: true, bookingId };
    } catch (error) {
      console.error('Error creating booking:', error);
      return { success: false, error: error.message };
    }
  },

  // Get booking by ID
  getBookingById: async (bookingId) => {
    try {
      // TODO: Replace with actual Firebase query
      // const bookingRef = doc(db, 'bookings', bookingId);
      // const bookingDoc = await getDoc(bookingRef);
      // if (bookingDoc.exists()) {
      //   return { success: true, booking: { id: bookingDoc.id, ...bookingDoc.data() } };
      // }
      // return { success: false, error: 'Booking not found' };
      
      // For now, return from sample data
      const booking = sampleBookings.find(b => b.id === bookingId);
      if (booking) {
        return { success: true, booking };
      }
      return { success: false, error: 'Booking not found' };
    } catch (error) {
      console.error('Error fetching booking:', error);
      return { success: false, error: error.message };
    }
  },

  // Get all bookings for a user
  getUserBookings: async (userId) => {
    try {
      // TODO: Replace with actual Firebase query
      // const bookingsRef = collection(db, 'bookings');
      // const q = query(
      //   bookingsRef,
      //   where('userId', '==', userId),
      //   orderBy('createdAt', 'desc')
      // );
      // const snapshot = await getDocs(q);
      // const bookings = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      // return { success: true, bookings };
      
      // For now, return from sample data
      const userBookings = sampleBookings
        .filter(b => b.userId === userId)
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      return { success: true, bookings: userBookings };
    } catch (error) {
      console.error('Error fetching user bookings:', error);
      return { success: false, error: error.message, bookings: [] };
    }
  },

  // Get all bookings (Admin function)
  getAllBookings: async () => {
    try {
      // TODO: Replace with actual Firebase query
      // const bookingsRef = collection(db, 'bookings');
      // const q = query(bookingsRef, orderBy('createdAt', 'desc'));
      // const snapshot = await getDocs(q);
      // const bookings = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      // return { success: true, bookings };
      
      // For now, return sample data
      return { success: true, bookings: sampleBookings };
    } catch (error) {
      console.error('Error fetching all bookings:', error);
      return { success: false, error: error.message, bookings: [] };
    }
  },

  // Update booking status
  updateBookingStatus: async (bookingId, status) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const bookingRef = doc(db, 'bookings', bookingId);
      // await updateDoc(bookingRef, { status, updatedAt: new Date().toISOString() });
      // return { success: true };
      
      // For now, update in sample data
      const bookingIndex = sampleBookings.findIndex(b => b.id === bookingId);
      if (bookingIndex !== -1) {
        sampleBookings[bookingIndex].status = status;
        sampleBookings[bookingIndex].updatedAt = new Date().toISOString();
        return { success: true };
      }
      return { success: false, error: 'Booking not found' };
    } catch (error) {
      console.error('Error updating booking status:', error);
      return { success: false, error: error.message };
    }
  },

  // Update booking details
  updateBooking: async (bookingId, updates) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const bookingRef = doc(db, 'bookings', bookingId);
      // await updateDoc(bookingRef, { ...updates, updatedAt: new Date().toISOString() });
      // return { success: true };
      
      // For now, update in sample data
      const bookingIndex = sampleBookings.findIndex(b => b.id === bookingId);
      if (bookingIndex !== -1) {
        sampleBookings[bookingIndex] = {
          ...sampleBookings[bookingIndex],
          ...updates,
          updatedAt: new Date().toISOString(),
        };
        return { success: true };
      }
      return { success: false, error: 'Booking not found' };
    } catch (error) {
      console.error('Error updating booking:', error);
      return { success: false, error: error.message };
    }
  },

  // Cancel booking
  cancelBooking: async (bookingId) => {
    try {
      return await bookingService.updateBookingStatus(bookingId, 'cancelled');
    } catch (error) {
      console.error('Error cancelling booking:', error);
      return { success: false, error: error.message };
    }
  },

  // Delete booking (Admin function)
  deleteBooking: async (bookingId) => {
    try {
      // TODO: Replace with actual Firebase operation
      // const bookingRef = doc(db, 'bookings', bookingId);
      // await deleteDoc(bookingRef);
      // return { success: true };
      
      // For now, delete from sample data
      sampleBookings = sampleBookings.filter(b => b.id !== bookingId);
      return { success: true };
    } catch (error) {
      console.error('Error deleting booking:', error);
      return { success: false, error: error.message };
    }
  },

  // Get bookings for a specific car
  getCarBookings: async (carId) => {
    try {
      // TODO: Replace with actual Firebase query
      // const bookingsRef = collection(db, 'bookings');
      // const q = query(
      //   bookingsRef,
      //   where('carId', '==', carId),
      //   orderBy('startDate', 'asc')
      // );
      // const snapshot = await getDocs(q);
      // const bookings = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      // return { success: true, bookings };
      
      // For now, return from sample data
      const carBookings = sampleBookings
        .filter(b => b.carId === carId)
        .sort((a, b) => new Date(a.startDate) - new Date(b.startDate));
      return { success: true, bookings: carBookings };
    } catch (error) {
      console.error('Error fetching car bookings:', error);
      return { success: false, error: error.message, bookings: [] };
    }
  },

  // Check if dates are available for a car
  checkDateAvailability: async (carId, startDate, endDate) => {
    try {
      const result = await bookingService.getCarBookings(carId);
      if (!result.success) {
        return { available: false, error: result.error };
      }

      const start = new Date(startDate);
      const end = new Date(endDate);

      const hasConflict = result.bookings.some(booking => {
        if (booking.status === 'cancelled') return false;
        
        const bookingStart = new Date(booking.startDate);
        const bookingEnd = new Date(booking.endDate);

        return (start <= bookingEnd && end >= bookingStart);
      });

      return { available: !hasConflict };
    } catch (error) {
      console.error('Error checking date availability:', error);
      return { available: false, error: error.message };
    }
  },
};
