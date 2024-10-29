import uuid

class Player:
    def __init__(self, conn, addr, player_id):
        """
        class to represent a player in the game (a client connected to the server)
        """
        self.conn = conn # connection object to communicate with the client
        self.addr = addr # address of the client
        self.id = player_id # unique id of the player (generated by the server)
        self.uuid = str(uuid.uuid4())  # unique identifier for the player (generated by the server)
        self.state = {'x': 0, 'y': 0}  # initial position of the player (received by the client)