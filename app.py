import socket
import sys
import os

from apistar import App, Include, Route, types, validators, http, server

class Env(types.Type):
    debug = validators.Boolean(default=True),
    udp_ip = validators.String(default=os.environ['UDP_IP'] if os.environ['UDP_IP'] else '172.17.10.20')
    udp_port = validators.Number(default=int(os.environ['UDP_PORT']) if os.environ['UDP_PORT'] else 10001)


env = Env()
print(env)

class LightState(types.Type):
    is_on = validators.Boolean(default=False, description="Should the lights be on")

def send_message(message):
    try:
        print('Sending message: {}'.format(message))
        print('ip: {} port: {}'.format(env.udp_ip, env.udp_port))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (env.udp_ip, env.udp_port))
    finally:
        print('Closing socket...')
        sock.close()

def all_zones(lightState: LightState):
    if lightState.is_on:
        send_message('all_on\r\n')
        print(env.keys())
        print(os.environ.keys())
        return {'all_zones': 'on'}
    else:
        send_message('all_off\r\n')
        return {'all_zones': 'off'}

routes = [
    Route('/all_zones', 'POST', all_zones)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('0.0.0.0', 5000, debug=True)
