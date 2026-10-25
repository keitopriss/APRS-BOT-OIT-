import aprslib
import threading
import time
import importlib
import inspect
import itertools
import os

# APRS login details
CALLSIGN = "YD3ADB-7"
PASSCODE = "23973"  # passcode untuk callsign dasar YD3ADB (tanpa SSID)

# APRS server settings
SERVER = "asia.aprs2.net"
PORT = 14580

# Folder berisi modul perintah (relatif terhadap main.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMMANDS_FOLDER = "commands"

received_msgs = set()
command_functions = {}
client = None

# Nomor pesan dimulai dari angka berbasis waktu supaya tidak bentrok setelah bot restart
_msg_counter = itertools.count(int(time.time()) % 50000)


def load_commands():
    """Muat semua modul di folder commands secara dinamis."""
    folder = os.path.join(BASE_DIR, COMMANDS_FOLDER)
    for filename in os.listdir(folder):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"{COMMANDS_FOLDER}.{module_name}")
            if hasattr(module, "handle_command"):
                command_functions[module_name.lower()] = module.handle_command
                print(f"Loaded command: {module_name}")
            else:
                print(f"Module {module_name} tidak punya fungsi 'handle_command'.")


def send_ack(client, msgNo, to_call):
    """Kirim ACK. Format APRS: ack<msgNo>."""
    to_call_padded = f"{to_call:<9}"
    ack_message = f"{CALLSIGN}>APRS::{to_call_padded}:ack{msgNo}"
    try:
        client.sendall(ack_message)
        print(f"ACK sent: {ack_message}")
    except Exception as e:
        print(f"Error sending ACK: {e}")


def split_message(message, max_length):
    """Pecah pesan di spasi agar tiap bagian <= max_length."""
    words = message.split()
    messages = []
    current = ""
    for word in words:
        if current and len(current) + len(word) + 1 > max_length:
            messages.append(current)
            current = word
        else:
            current = f"{current} {word}" if current else word
    if current:
        messages.append(current)
    return messages


def send_response(client, to_call, response_message):
    """Kirim balasan; tiap potongan diberi nomor pesan unik ({id})."""
    to_call_padded = f"{to_call:<9}"
    for msg in split_message(response_message, 60):
        msg_id = (next(_msg_counter) % 99999) + 1
        response = f"{CALLSIGN}>APRS::{to_call_padded}:{msg}{{{msg_id}"
        try:
            client.sendall(response)
            print(f"Response sent: {response}")
        except Exception as e:
            print(f"Error sending response: {e}")
        time.sleep(3)


def handle_packet(packet):
    """Proses paket yang masuk."""
    print(f"Received packet: {packet}")
    if "message_text" not in packet:
        return

    addressee = (packet.get("addresse") or "").strip().upper()
    if addressee != CALLSIGN.upper():
        return

    from_call = packet.get("from")
    msgNo = packet.get("msgNo")
    message_text = (packet.get("message_text") or "").strip()

    # ACK setiap pesan yang punya nomor (termasuk kiriman ulang)
    if msgNo:
        threading.Thread(target=send_ack, args=(client, msgNo, from_call)).start()

        # Jangan proses pesan yang sama dua kali
        key = (from_call, msgNo)
        if key in received_msgs:
            return
        received_msgs.add(key)

    print(f"Received message: '{message_text}' from {from_call}")

    command_function = command_functions.get(message_text.lower())
    if command_function:
        try:
            # Kirim callsign pengirim kalau fungsinya menerima argumen (mis. ping.py)
            if len(inspect.signature(command_function).parameters) >= 1:
                response_message = command_function(from_call)
            else:
                response_message = command_function()
        except Exception as e:
            response_message = f"Error: {e}"

        if response_message:
            threading.Thread(
                target=send_response, args=(client, from_call, response_message)
            ).start()
    else:
        print(f"Perintah tidak dikenal: '{message_text}'")


def keepalive(c):
    """Kirim komentar berkala agar koneksi tidak dianggap idle oleh server."""
    while True:
        time.sleep(60)
        try:
            c.sendall("# keepalive")
        except Exception:
            return


def connect_to_aprs():
    global client
    while True:
        try:
            client = aprslib.IS(CALLSIGN, passwd=PASSCODE, host=SERVER, port=PORT)
            client.set_filter(f"g/{CALLSIGN}")
            print(f"Connecting to APRS-IS server {SERVER}:{PORT} as {CALLSIGN}")
            client.connect(blocking=True)
            print("Connected to APRS-IS server successfully")
            threading.Thread(target=keepalive, args=(client,), daemon=True).start()
            client.consumer(handle_packet, raw=False)
        except KeyboardInterrupt:
            print("Bot dihentikan.")
            break
        except Exception as e:
            print(f"Connection lost: {e}. Reconnecting in 15 seconds...")
        try:
            client.close()
        except Exception:
            pass
        time.sleep(15)


if __name__ == "__main__":
    load_commands()
    connect_to_aprs()