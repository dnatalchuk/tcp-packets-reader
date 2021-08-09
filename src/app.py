# importing required libraries
import struct
import time
import datetime

# defining polling path variable to read from locally in Docker container
POLLING_PATH="./tcp_connections"

def parse_addr_port(s):
    '''
    Function to parse ip address/port from the input and manage data coversion from hex.
    '''
    addr_str, port_str = s.split(":")
    addr_bytes = bytes.fromhex(addr_str)
    port_bytes = bytes.fromhex(port_str)
    (
        d,
        c,
        b,
        a,
    ) = struct.unpack("<BBBB", addr_bytes)
    (port,) = struct.unpack("<H", port_bytes)
    return [a, b, c, d], port


def parse_state(s):
    (s,) = struct.unpack("<B", bytes.fromhex(s))
    return s

def addr_str(ip, port):
    '''
    Function to present ip address and port combination in the app output
    '''
    return f"{ip[0]}.{ip[1]}.{ip[2]}.{ip[3]}:{port}"

def get_connections(path):
    '''
    Function to read/poll conections from location defined by "path" input parameter.
    Opening file to read to read each lines, itterating over enumrated lines, performing data formatting and parsing,
    indexing respective parameters of connections and agrregating in the returned resulted list.
    '''
    result = []
    with open(path) as file:
        lines = file.readlines()
    for index, line in enumerate(lines):
        if index > 0:
            id, local_addr_str, remote_addr_str, state_str, tmp = line.split(maxsplit=4)
            local = parse_addr_port(local_addr_str)
            remote = parse_addr_port(remote_addr_str)
            state = parse_state(state_str)
            result.append((local, remote, state))
    return result


def to_dict(connections):
    '''
    Function to index connections dictionary for respective key/value pairs.
    '''
    result = {}
    for (
        (local_ip, local_port),
        (remote_ip, remote_port),
        state,
    ) in connections:
        key = f"{addr_str(local_ip, local_port)}-{addr_str(remote_ip, remote_port)}"
        value = (
            (local_ip, local_port),
            (remote_ip, remote_port),
            state,
        )
        result[key] = value
    return result


def compare_connections(prev_connections, curr_connections):
    '''
    Function to managed opened/closed connections based on the previous and current connections.
    '''
    prev_dict = to_dict(prev_connections)
    curr_dict = to_dict(curr_connections)
    opened = []
    closed = []
    for key, conn in prev_dict.items():
        if not key in curr_dict:
            closed.append(conn)
    for key, conn in curr_dict.items():
        if not key in prev_dict:
            opened.append(conn)
    return (opened, closed)


def show_connections_diff(now, opened, closed):
    '''
    Function to indetify connections diff based on the input paramas for the curent date/time and opened/closed connections
    to output in the app execution logs.
    '''
    for (
        (local_ip, local_port),
        (remote_ip, remote_port),
        state,
    ) in opened:
        print(
            now,
            ": New connection: ",
            addr_str(local_ip, local_port),
            " -> ",
            addr_str(remote_ip, remote_port),
            sep="",
        )
    for (
        (local_ip, local_port),
        (remote_ip, remote_port),
        state,
    ) in closed:
        print(
            now,
            ": Closed connection: ",
            addr_str(local_ip, local_port),
            " -> ",
            addr_str(remote_ip, remote_port),
            sep="",
        )


def run(delay=5):
    '''
    Fucntion which consumes previously declared functions with the delay input param to poll connections.
    '''
    prev_connections = []
    while True:
        now = (
            datetime.datetime.utcnow()
            .replace(tzinfo=datetime.timezone.utc)
            .replace(microsecond=0)
        )
        curr_connections = get_connections(POLLING_PATH)
        opened, closed = compare_connections(prev_connections, curr_connections)
        show_connections_diff(now, opened, closed)
        prev_connections = curr_connections
        time.sleep(delay)


if __name__ == "__main__":
    run()