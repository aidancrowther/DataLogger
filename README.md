# Arduino Data Logger

Description:
  This project is designed to allow an arduino based data logger to collect weather data outdoors, while actively updating a local database to provide real time weather data. Data is collected, and uploaded to a DataBase server using a raspberry Pi as an intermediary.
  
  Current Features:
  
  - Support for DHT series of humidity sensors
  - Support for BMP085 pressure sensor
  - Light level reading using photo-resistor
  - Battery level monitoring
  - Low power consumption
  - Store data on MySQL DB
  - Specify DB credentials manually
  - Verbose logging of received data and functions in logger.py
  - Supports a range of RF links using virtual wire library
  
  Requirements:
  
  - Arduino Pro Mini with sensors for measuring wanted data
  - RF link receiver/transmitter pair
  - Raspberry Pi with pigpio, MySQLdb, and virtual wire libraries installed
  - Database server with an appropriate table
  
  Install:
  
   - Raspberry Pi Install:
      - Clone repository using `git clone https://www.github.com/aidancrowther/DataLogger`
      - Navigate to the installation folder, and install [piVirtualWire](https://github.com/DzikuVx/piVirtualWire)
      - Download and install pigpio and MySQLDB using `sudo apt-get install python3-pigpio python3-MySQLdb`
      - Enable pigpio on boot by using `sudo systemctl enable pigpiod`
