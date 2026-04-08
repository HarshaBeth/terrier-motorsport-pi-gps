# Terrier Motorsport Pi GPS

Raspberry Pi GPS logger for BU Terrier Motorsport.

## What this does

- reads GPS data from a SparkFun u-blox MAX-M10S module over UART
- parses NMEA sentences
- prints useful GPS fields
- logs GPS data to CSV

## Hardware

- Raspberry Pi 4 Model B
- SparkFun MAX-M10S GPS module
- GNSS antenna
- UART wiring:
  - GPS 3V3 -> Pi 3.3V
  - GPS GND -> Pi GND
  - GPS TX -> Pi RX
  - GPS RX -> Pi TX

## Setup

Install dependencies:

```bash
pip3 install -r requirements.txt
```
