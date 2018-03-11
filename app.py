import socket
import sys

from apistar import Include, Route
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar import environment, typesystem
from apistar import Settings


class Env(environment.Environment):
    properties = {
        'DEBUG': typesystem.boolean(default=False),
        'UDP_IP': typesystem.string(default='91.84.242.209'),
        'UDP_PORT': typesystem.integer(default=10001)
    }

env = Env()

class IsOn(typesystem.Boolean):
    default = False
    description = 'Should the lighting be on'


def send_message(message, settings: Settings):
    try:
        print('Sending message: {}'.format(message))
        print('ip: {} port: {}'.format(settings['UDP_IP'], settings['UDP_PORT']))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (settings['UDP_IP'], settings['UDP_PORT']))
    finally:
        print('Closing socket...')
        sock.close()


def all_zones(on: IsOn, settings: Settings):
    if on:
        send_message('all_on\r\n', settings)
        return {'all_zones': 'on'}
    else:
        send_message('all_off\r\n', settings)
        return {'all_zones': 'off'}


routes = [
    Route('/all_zones', 'GET', all_zones),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

settings = {
    'UDP_IP': env['UDP_IP'],
    'UDP_PORT': env['UDP_PORT']
}

app = App(routes=routes, settings=settings)


if __name__ == '__main__':
    app.main()
