#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Romà Mendoza"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "roma.mendoza@institutjoanmiro.cat"
__status__ = "Production"

# ================================================================
"""
Moving the ball in the Pong game

license > See https://www.gnu.org/licenses/gpl-3.0.html
"""
# ================================================================
# Import the pygame module
import pygame
from settings import *
from object import Group, Paddle, Ball
from game_over import GameOver  # TASK 3
from time import sleep # TASK 4

# ================================================================
# constants

# ================================================================
# code


class Game:
    def __init__(self):
        """ Set up the game """

        # Initialize pygame
        pygame.init()

        # Create a clock to set a specific FPS
        self.clock = pygame.time.Clock()

        # Create the screen object
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Create GameOver object
        self.game_over = GameOver()  # TASK 3
        # TASK 3
        # Create GameOver object
        # WRITE YOUR CODE HERE

        # Create group with all visible objects
        self.paddle = Paddle("player1", (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.9)),
                             (PLAYER_WIDTH, PLAYER_HEIGHT), STEP, PLAYER_COLOR)
        self.ball = Ball("ball1", (SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.1)), RADIUS,
                         0, BALL_COLOR)
        self.objects = Group()
        self.objects.add(self.paddle)
        self.objects.add(self.ball)
        self.balls = Group()  # Group of balls
        self.balls.add(self.ball)

        # At the beginning the game is running
        self.running = True

        # Pause control
        self.paused = False

    def __bounce_paddle(self):
        hit_ball = self.balls.collision(self.paddle)
        if hit_ball:
            if (self.paddle.rect.left < hit_ball.rect.centerx < self.paddle.rect.right) and \
                    (self.paddle.rect.top < hit_ball.rect.bottom < self.paddle.rect.bottom):
                hit_ball.horizontal_bounce()
            else:
                hit_ball.vertical_bounce()

    def __check_game_over(self):
        for ball in self.balls.elements:
            if ball.rect.bottom >= SCREEN_HEIGHT:
                self.running = False
                break

    def __update(self):
        """ Update objects """
        if not self.paused:
            self.objects.update()

            self.__bounce_paddle()

            # Is game over? Check whether any ball touches the bottom edge
            self.__check_game_over()

    def __check_events(self):
        """ Poll and handle events """
        # Check for event if user has pushed any event in queue
        for event in pygame.event.get():
            # if event is of type quit then set running boolean to false
            if event.type == QUIT:  # Window close button clicked?
                self.running = False
                break
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                    break
                if event.key == K_p:
                    self.paused = not self.paused

            if not self.paused:
                self.paddle.check_event(event)

    def __draw(self):
        """ Draw game objects """
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        self.screen.fill(BG_COLOR)
        self.objects.draw(self.screen)

    def run(self):
        """ Run the main game loop """
        # creating a bool value which checks if game is running

        while self.running:
            # STEP 1 >> Poll and handle events  ------------------
            self.__check_events()

            # STEP 2 >> Update game objects
            self.__update()

            # STEP 3 >> Draw game objects ----------------------------------
            self.__draw()

            # STEP 4 >> Show screen ----------------------------------------
            # The whole screen is updated (fill method affects the whole surface)
            pygame.display.update()

            # Set the frame rate
            self.clock.tick(60)

        # Once we leave the loop, close the window.
        #print("GAME IS OVER")
        self.game_over.draw(self.screen)
        sleep(5)


        pygame.quit()
