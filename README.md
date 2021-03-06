# Arduino Data Logger

Description:
  This project is designed to allow an Arduino based data logger to collect weather data outdoors, while actively updating a local database to provide real time weather data. Data is collected, and uploaded to a DataBase server using a raspberry Pi as an intermediary. The Arduino has been modified to operate between 3.0-4.2V in order to run directly off of an 18650 Li-Ion battery; this allows the logger to run for many months just off of the battery level. The Arduino has also been setup to minimize power draw, consuming less than ~1mA between measurements, and never exceeding ~15mA while transmitting for a few seconds.
  
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

   - Arduino Install:
      - Install libraries for [LowPower](https://github.com/rocketscream/Low-Power), [BMP085](https://github.com/adafruit/Adafruit-BMP085-Library), [DHT](https://github.com/RobTillaart/Arduino/tree/master/libraries/DHTlib), and [VirtualWire](https://www.pjrc.com/teensy/td_libs_VirtualWire.html)
      - Modify transmitter.ino for your sensors
      - Upload transmitter.ino to you Arduino
      
  Usage:
  
   - Run the logger using `python3 logger.py`
    - Use `-v` to enable verbose output
    - Use `-c` to specify a file containing db permissions
   - Run the data logger and ensure it is within range of the receiver
   
   The format for the permissions file should follow:
   ```
   dbuser='username'
   dbpass='password'
   dbname='database name'
   dbhost='IP/name of database server'
   table='table to write to'
   ```

  If a permissions file is not specified at run time, the default filename `certs.txt` will be used. If no appropriate permissions file can be found, the program will not run.
  
  The assumed format of the database table is as follows:
  
  created | temperature | pressure | humidex | light | battery
  ------- | ------- | ------- | ------- | ------- | -------
  automatically incrementing datetime element | measured temperature | measured pressure | measured humidity | measured light level | logger battery level
