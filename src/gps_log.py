import csv
import os
from datetime import datetime, UTC

import pynmea2
import serial

PORT = "/dev/serial0"
BAUDRATE = 9600
OUTPUT_FILE = "data/gps_log.csv"


def ensure_output_dir():
    os.makedirs("data", exist_ok=True)


def init_csv():
    file_exists = os.path.isfile(OUTPUT_FILE)
    csvfile = open(OUTPUT_FILE, "a", newline="")
    writer = csv.writer(csvfile)

    if not file_exists:
        writer.writerow([
            "timestamp_utc",
            "latitude",
            "longitude",
            "speed_kmh",
        ])

    return csvfile, writer


def knots_to_kmh(knots):
    return float(knots) * 1.852 if knots else 0.0


def main():
    ensure_output_dir()
    csvfile, writer = init_csv()
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)

    print("Logging clean GPS data...")

    last_timestamp = None

    try:
        while True:
            line = ser.readline().decode("ascii", errors="replace").strip()
            if not line.startswith("$"):
                continue

            try:
                msg = pynmea2.parse(line)

                # Only use RMC
                if msg.sentence_type != "RMC":
                    continue

                # Skip invalid fixes
                if msg.status != "A":
                    continue

                # Avoid duplicates (same second)
                if msg.timestamp == last_timestamp:
                    continue

                last_timestamp = msg.timestamp

                lat = msg.latitude
                lon = msg.longitude
                speed_kmh = knots_to_kmh(msg.spd_over_grnd)

                timestamp = datetime.now(UTC).isoformat()

                writer.writerow([
                    timestamp,
                    lat,
                    lon,
                    round(speed_kmh, 2),
                ])
                csvfile.flush()

                print(
                    f"{timestamp} | Lat: {lat}, Lon: {lon}, Speed: {round(speed_kmh,2)} km/h"
                )

            except pynmea2.ParseError:
                continue

    except KeyboardInterrupt:
        print("\nStopped logging.")
    finally:
        csvfile.close()
        ser.close()


if __name__ == "__main__":
    main()