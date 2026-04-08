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
            "sentence_type",
            "latitude",
            "longitude",
            "altitude",
            "num_sats",
            "speed_over_ground",
        ])

    return csvfile, writer


def main():
    ensure_output_dir()
    csvfile, writer = init_csv()
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)

    print(f"Logging GPS data to {OUTPUT_FILE}...")

    try:
        while True:
            line = ser.readline().decode("ascii", errors="replace").strip()
            if not line.startswith("$"):
                continue

            try:
                msg = pynmea2.parse(line)

                latitude = getattr(msg, "latitude", "")
                longitude = getattr(msg, "longitude", "")
                altitude = getattr(msg, "altitude", "")
                num_sats = getattr(msg, "num_sats", "")
                speed = getattr(msg, "spd_over_grnd", "")

                if latitude != "" and longitude != "":
                    timestamp = datetime.now(UTC).isoformat()

                    writer.writerow([
                        timestamp,
                        msg.sentence_type,
                        latitude,
                        longitude,
                        altitude,
                        num_sats,
                        speed,
                    ])
                    csvfile.flush()

                    print(
                        f"{timestamp} | {msg.sentence_type} | "
                        f"Lat: {latitude}, Lon: {longitude}"
                    )

            except pynmea2.ParseError:
                continue

    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
    finally:
        csvfile.close()
        ser.close()


if __name__ == "__main__":
    main()