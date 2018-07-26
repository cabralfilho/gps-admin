from django.core.management import BaseCommand
from django.utils.timezone import now

from gps.parser import parse_message
from gps import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        import asyncio

        async def handle_msg(reader, writer):
            try:
                keep_connection = True
                while keep_connection:
                    data = await reader.read()
                    if data:
                        message = data.decode('ascii')
                        addr = writer.get_extra_info('peername')
                        print(f'Received ({message}) from {addr}')

                        try:
                            self.process_message(message)
                        except:
                            print(f'Failed processing message. Disconnecting client {addr}')
                            keep_connection = False
                    else:
                        print(f'Client {addr} disconnected')
                        keep_connection = False
                        writer.close()
            except:
                print(f'Failed processing message. Disconnecting client.')

        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(handle_msg, '0.0.0.0', 4444, loop=loop)
        server = loop.run_until_complete(coro)

        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    def process_message(self, raw_msg):
        msg = parse_message(raw_msg)

        print(msg)

        device, _ = models.Device.objects.get_or_create(imei=msg['imei'])

        models.Position.objects.create(
            device=device,
            latitude=msg['latitude'],
            longitude=msg['longitude'],
            datetime=now(),
        )
