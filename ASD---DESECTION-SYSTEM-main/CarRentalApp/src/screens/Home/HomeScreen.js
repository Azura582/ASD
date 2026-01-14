import React from 'react';
import { View, StyleSheet, ScrollView, Image } from 'react-native';
import { Card, Title, Paragraph, Button, Text } from 'react-native-paper';
import { colors } from '../../theme/theme';

const HomeScreen = ({ navigation }) => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Title style={styles.headerTitle}>Welcome to Car Rental</Title>
        <Paragraph style={styles.headerSubtitle}>
          Find the perfect car for your journey
        </Paragraph>
      </View>

      <Card style={styles.card}>
        <Card.Content>
          <Title>Start Your Journey</Title>
          <Paragraph>Book a car in just a few simple steps</Paragraph>
        </Card.Content>
        <Card.Actions>
          <Button
            mode="contained"
            onPress={() => navigation.navigate('TripDetails')}
            style={styles.primaryButton}
          >
            Book Now
          </Button>
        </Card.Actions>
      </Card>

      <View style={styles.featuresContainer}>
        <Text style={styles.sectionTitle}>Why Choose Us?</Text>
        
        <Card style={styles.featureCard}>
          <Card.Content style={styles.featureContent}>
            <Text style={styles.featureIcon}>🚗</Text>
            <View style={styles.featureText}>
              <Title style={styles.featureTitle}>Wide Selection</Title>
              <Paragraph>Choose from a variety of cars</Paragraph>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.featureCard}>
          <Card.Content style={styles.featureContent}>
            <Text style={styles.featureIcon}>💰</Text>
            <View style={styles.featureText}>
              <Title style={styles.featureTitle}>Best Prices</Title>
              <Paragraph>Competitive rates for all budgets</Paragraph>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.featureCard}>
          <Card.Content style={styles.featureContent}>
            <Text style={styles.featureIcon}>⚡</Text>
            <View style={styles.featureText}>
              <Title style={styles.featureTitle}>Quick Booking</Title>
              <Paragraph>Book in minutes, drive in hours</Paragraph>
            </View>
          </Card.Content>
        </Card>

        <Card style={styles.featureCard}>
          <Card.Content style={styles.featureContent}>
            <Text style={styles.featureIcon}>🛡️</Text>
            <View style={styles.featureText}>
              <Title style={styles.featureTitle}>Safe & Secure</Title>
              <Paragraph>All cars are insured and verified</Paragraph>
            </View>
          </Card.Content>
        </Card>
      </View>

      <Card style={styles.card}>
        <Card.Content>
          <Title>Browse All Cars</Title>
          <Paragraph>Explore our complete collection</Paragraph>
        </Card.Content>
        <Card.Actions>
          <Button
            mode="outlined"
            onPress={() => navigation.navigate('CarCatalog')}
          >
            View Catalog
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
  header: {
    padding: 20,
    backgroundColor: colors.primary,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 16,
    color: colors.white,
  },
  card: {
    margin: 15,
    elevation: 4,
  },
  primaryButton: {
    flex: 1,
  },
  featuresContainer: {
    padding: 15,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: colors.dark,
  },
  featureCard: {
    marginBottom: 10,
    elevation: 2,
  },
  featureContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  featureIcon: {
    fontSize: 40,
    marginRight: 15,
  },
  featureText: {
    flex: 1,
  },
  featureTitle: {
    fontSize: 16,
    marginBottom: 2,
  },
});

export default HomeScreen;
