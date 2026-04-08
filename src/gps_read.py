import serial
import pynmea2

PORT = "/dev/serial0"
BAUDRATE = 9600

def main():
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    print(f"Reading GPS data from {PORT} at {BAUDRATE} baud...")

    try:
        while True:
            line = ser.readline().decode("ascii", errors="replace").strip()
            if not line.startswith("$"):
                continue

            try:
                msg = pynmea2.parse(line)

                if msg.sentence_type == "RMC":
                    print(
                        f"Type: {msg.sentence_type} | "
                        f"Lat: {msg.latitude} | Lon: {msg.longitude}"
                    )
            except pynmea2.ParseError:
                continue
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()