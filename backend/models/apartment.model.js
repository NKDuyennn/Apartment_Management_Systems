const { DataTypes } = require('sequelize');
const sequelize = require('../config/db.config');

const Apartment = sequelize.define('Apartment', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  apartmentNumber: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true
  },
  floor: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  building: {
    type: DataTypes.STRING,
    allowNull: false
  },
  area: {
    type: DataTypes.FLOAT,
    allowNull: false
  },
  bedrooms: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  bathrooms: {
    type: DataTypes.INTEGER,
    allowNull: false
  },
  status: {
    type: DataTypes.ENUM('available', 'occupied', 'maintenance'),
    defaultValue: 'available'
  },
  monthlyRent: {
    type: DataTypes.DECIMAL(10, 2),
    allowNull: false
  }
}, {
  timestamps: true
});

module.exports = Apartment;
