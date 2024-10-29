import pygame
import json
import threading
from client_side.player_client import PlayerClient


def main():
    """
    main function to run the game client.
    """
    pygame.init()  # initialize pygame

    WIDTH, HEIGHT = 1280, 720  # screen dimensions
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # screen creation
    pygame.display.set_caption("Hungry Client DEV")  # screen title

    WHITE = (255, 255, 255)  # white color
    BLACK = (0, 0, 0)  # black color

    font = pygame.font.Font(None, 24)  # font for the text

    client_logo = pygame.image.load("assets/server.png")  # client logo
    pygame.display.set_icon(client_logo)  # set the client logo
    client_logo = pygame.transform.scale(
        client_logo, (128, 128))  # scale the client logo

    clock = pygame.time.Clock()  # clock to control the fps
    with open('configs/host.json', 'r') as f:  # read the host configuration
        config = json.load(f)  # load the configuration
    ip = config.get('ip')
    port = config.get('port')
    client = PlayerClient(ip=ip, port=port)  # create the player client object

    # start the thread to receive updates from the server
    threading.Thread(target=client.receive_updates, daemon=True).start()

    running = True
    while running:  # main loop
        dt = clock.tick(120) / 1000  # get the delta time in seconds
        for event in pygame.event.get():  # get the events from pygame
            if event.type == pygame.QUIT:  # if the event is quit
                running = False  # stop the loop

        keys = pygame.key.get_pressed()  # controls of your player
        if keys[pygame.K_z]:
            client.position[1] -= client.speed * dt
        if keys[pygame.K_s]:
            client.position[1] += client.speed * dt
        if keys[pygame.K_q]:
            client.position[0] -= client.speed * dt
        if keys[pygame.K_d]:
            client.position[0] += client.speed * dt

        client.send_position()  # send the position of the player to the server

        screen.fill(WHITE)  # fill the background with white color
        for player in client.players.values():  # draw the players in the screen
            player.draw(screen, font, BLACK)  # draw the player

        pygame.display.flip()  # update the screen

    client.close()  # close the connection
    pygame.quit()  # quit pygame


if __name__ == "__main__":
    main()
