import pygame

import src.game
from src.animated_sprite import AnimatedSprite
from src.common import Direction, TILE_SIZE


class Player(AnimatedSprite):

    def __init__(self, center_point, direction, down_img, left_img, up_img,
                 right_img):
        AnimatedSprite.__init__(self, center_point, direction, down_img,
                                left_img, up_img, right_img)
        self.index = 0

    def update(self, wall_group):
        pass
        # self.index += 1
        # if self.index >= len(self.image):
        #    self.index = 0
        # self.image = self.image[self.index]

    def set_center_point(self, center_point):
        self.center_point = center_point

    #def render(self, display):
        #display.blit(self.image, (self.rect.x, self.rect.y))

    def move(self, camera_pos):
        # TODO: Smooth out movement.
        pos_x, pos_y = camera_pos
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            self.direction = Direction.DOWN.value
            self.rect.y += TILE_SIZE
            pos_y -= TILE_SIZE
        if key[pygame.K_LEFT]:
            self.direction = Direction.LEFT.value
            self.rect.x -= TILE_SIZE
            pos_x += TILE_SIZE
        if key[pygame.K_UP]:
            self.direction = Direction.UP.value
            self.rect.y -= TILE_SIZE
            pos_y += TILE_SIZE
        if key[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT.value
            self.rect.x += TILE_SIZE
            pos_x -= TILE_SIZE

        # TODO: Handle internal wall sides collision.
        if self.rect.x < 0:  # Simple Sides Collision
            self.rect.x = 0  # Reset Player Rect Coord
            # pos_x = camera_pos[0]  # Reset Camera Pos Coord
        elif self.rect.x > src.game.Game.WIN_WIDTH - TILE_SIZE:
            self.rect.x = src.game.Game.WIN_WIDTH - TILE_SIZE
            # pos_x = camera_pos[0]
        if self.rect.y < 0:
            self.rect.y = 0
            # pos_y = camera_pos[1]
        elif self.rect.y > src.game.Game.WIN_HEIGHT - TILE_SIZE:
            self.rect.y = src.game.Game.WIN_HEIGHT - TILE_SIZE
        # elif self.rect.y > self.WIN_HEIGHT - ((self.WIN_HEIGHT // 23) * 1.5):
        #    self.rect.y = self.WIN_HEIGHT - ((self.WIN_HEIGHT // 23) * 1.5)

        # pos_y = camera_pos[1]
        # TODO: implement actual function of B, A, Start, Select buttons.
        if key[pygame.K_z]:
            # B button
            print("You pressed the z key.")
        if key[pygame.K_y]:
            # A button
            print("You pressed the y key.")
        if key[pygame.K_SPACE]:
            # Start button
            print("You pressed the space bar.")
        if key[pygame.K_ESCAPE]:
            # Select button
            print("You pressed the escape key.")
        return pos_x, pos_y
