from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json
import logger
import payloadparser
import gamestate
import provider


class GSIServer(HTTPServer):
    def __init__(self, server_address, token, RequestHandler):
        self.provider = provider.Provider()
        self.auth_token = token
        self.gamestatemanager = gamestate.GameStateManager()

        super(GSIServer, self).__init__(server_address, RequestHandler)

        self.setup_log_file()
        self.payload_parser = payloadparser.PayloadParser()

    def setup_log_file(self):
        self.log_file = logger.LogFile(time.asctime())


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers["Content-Length"])
        body = self.rfile.read(length).decode("utf-8")

        payload = json.loads(body)
        # Ignore unauthenticated payloads
        if not self.authenticate_payload(payload):
            return None

        self.server.log_file.log_event(time.asctime(), payload)
        self.server.payload_parser.parse_payload(payload, self.server.gamestatemanager)

        self.send_header("Content-type", "text/html")
        self.send_response(200)
        self.end_headers()

    def authenticate_payload(self, payload):
        if "auth" in payload and "token" in payload["auth"]:
            return payload["auth"]["token"] == server.auth_token
        else:
            return False

    def parse_payload(self, payload):

        self.server.log_file.log_event(time.asctime(), payload)

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


server = GSIServer(("localhost", 3000), "MYTOKENHERE", RequestHandler)
