import socket
import picar_4wd as pc

from time import sleep
import subprocess
import multiprocessing as mp


HOST = "192.168.137.100" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

POWER = 15
def move(direction):
    if b'left' in direction:
        pc.turn_left(POWER)
    elif b'right' in direction:
        pc.turn_right(POWER)
    elif b'forward' in direction:
        pc.forward(POWER)
    elif b'backward' in direction:
        pc.backward(POWER)
    elif b'stop' in direction:
        pc.stop()
    else:
        pass


# sends data back to the web interface at a set rate
update_interval = 1
def worker(client):
    while True:
        # for temperature sensor data, we use lm-sensors package
        temperature_command = "sensors | grep temp1 | cut -d'+' -f2 | cut -d' ' -f1"
        temperature = subprocess.check_output(temperature_command, shell=True, text=True)
        client.sendall(("Temperature: " + temperature + "\n").encode("utf-8"))

        battery_command = "picar-4wd power-read | grep voltage | cut -d' ' -f3"
        battery_level = subprocess.check_output(battery_command, shell=True, text=True)
        client.sendall(("Battery voltage: " + battery_level + "\n").encode("utf-8"))

        sleep(update_interval)


def main():

    child : mp.Process

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        print("Starting server...")

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()

        try:
            client, clientInfo = s.accept()

            child = mp.Process(target = worker, args = (client,))
            child.start()

            print("server recv from: ", clientInfo)
            while 1:
                direction = client.recv(12)
                if direction != b"":
                    print(direction)    
                    move(direction)

        except Exception as e: 
            child.join()
            print("Closing socket: ", e)
            client.close()
            s.close()    


if __name__ == "__main__":
    main()