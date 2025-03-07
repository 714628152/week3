import socket
import platform 

def get_machine_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_machine_name():
    machine_name = platform.node()
    return machine_name

if __name__ == "__main__":
    ip = get_machine_ip()
    name = get_machine_name()
    print("Machine IP:{ip}",ip)
    print("Machine Name:{name}",name)
    print('my name is Friday')