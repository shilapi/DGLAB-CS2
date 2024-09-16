import pydglab

# from gsi_server import *

from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json, tomllib
import logger
import payloadparser
import gamestate
import provider
import logging
import asyncio
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor
from http.server import HTTPServer, BaseHTTPRequestHandler

config = tomllib.load(open("config.toml", "rb"))

logging.basicConfig(
    format="[%(levelname)s]: %(message)s",
    level=logging.DEBUG if config["debug"] else logging.INFO,
)

BASE_STRENGTH = config["dglab"]["base_strength"]


class GSIServer(HTTPServer):
    def __init__(self, server_address, token, RequestHandler):
        self.provider = provider.Provider()
        self.auth_token = token
        self.gamestatemanager = gamestate.GameStateManager()

        super(GSIServer, self).__init__(server_address, RequestHandler)

        self.payload_parser = payloadparser.PayloadParser()


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        payload = json.loads(body)
        # Ignore unauthenticated payloads
        if not self.authenticate_payload(payload):
            return None

        self.server.payload_parser.parse_payload(payload, self.server.gamestatemanager)

        self.send_header("Content-type", "text/html")
        self.send_response(200)
        self.end_headers()

    def authenticate_payload(self, payload):
        if "auth" in payload and "token" in payload["auth"]:
            return payload["auth"]["token"] == server.auth_token
        else:
            return False

    # def parse_payload(self, payload):
    # round_phase = self.get_round_phase(payload)

    # if round_phase != self.server.round_phase:
    #     self.server.round_phase = round_phase
    #     print('New round phase: %s' % round_phase)

    def get_round_phase(self, payload):
        if "round" in payload and "phase" in payload["round"]:
            return payload["round"]["phase"]
        else:
            return None

    def get_kill(self, payload):
        if (
            "player" in payload
            and "state" in payload["player"]
            and "rounds_kills" in payload["player"]["state"]
        ):
            return payload["player"]["rounds_kills"]
        else:
            return None

    def log_message(self, format, *args):
        """
        Prevents requests from printing into the console
        """
        return


server = GSIServer(("localhost", 3000), "DGLAB", RequestHandler)


async def fetch_data():
    dglab_instance = pydglab.dglab_v3()
    try:
        await dglab_instance.create()
    except TimeoutError:
        print("Timeout connecting to dglab, retrying...")
        dglab_instance = pydglab.dglab_v3()
        await dglab_instance.create()
    await asyncio.sleep(2)
    await dglab_instance.set_strength_sync(BASE_STRENGTH, 0)
    await dglab_instance.set_wave_sync(1, 9, 20, 5, 35, 20)
    logging.info("Connected! Ready to go!")
    hp = [100, 100]
    burning = 0  # 0-255, 燃烧强度
    while True:
        await asyncio.sleep(0.25)
        burning = server.gamestatemanager.gamestate.player.state.burning
        hp.insert(0, server.gamestatemanager.gamestate.player.state.health)
        hp.pop()
        burning_offset = 1 + (config["dglab"]["burning_multiplier"] * (burning / 255))
        hp_offset = (100 - hp[0]) * config["dglab"]["strength_per_hp"]
        strength_offset = int(hp_offset * burning_offset)
        if hp[0] == 100 and not config["dglab"]["keep_strength_while_not_injured"]:
            await dglab_instance.set_strength_sync(0, 0)
        elif hp[0] == 100 and config["dglab"]["keep_strength_while_not_injured"]:
            await dglab_instance.set_strength_sync(BASE_STRENGTH + strength_offset, 0)
        if hp[0] < hp[1]:
            logging.info(
                f"You're injured! Current HP {hp[0]}. Setting strength to {BASE_STRENGTH + strength_offset}"
            )
        if hp[0] > hp[1]:
            logging.info(
                f"You're healed! Current HP {hp[0]}. Setting strength to {BASE_STRENGTH + strength_offset}"
            )
        if burning > 0:
            logging.info(
                f"Burning! Burning strength: {burning}. Setting strength with offset {burning_offset}"
            )
        # print(hp)

        # await dglab_instance.set_wave_sync(5,95,20,5,95,20)


def start_http_server(started_evt, server=server):
    logging.info("CS:GO GSI server starting")
    started_evt.set()
    server.serve_forever()


def start_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


if __name__ == "__main__":
    # Start HTTP server in a separate thread
    started_evt = Event()
    http_thread = Thread(target=start_http_server, daemon=True, args=(started_evt,))
    http_thread.start()

    # Start asyncio event loop in the main thread
    # loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(fetch_data())
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        loop.call_soon_threadsafe(loop.stop)
        http_thread.join()
        print(time.asctime(), "-", "CS:GO GSI server stopped")
