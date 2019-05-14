from src.animated_sprite import AnimatedSprite
import pygame
import src.game


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
            self.direction = AnimatedSprite.DOWN
            self.rect.y += 48
            pos_y -= 48
        if key[pygame.K_LEFT]:
            self.direction = AnimatedSprite.LEFT
            self.rect.x -= 48
            pos_x += 48
        if key[pygame.K_UP]:
            self.direction = AnimatedSprite.UP
            self.rect.y -= 48
            pos_y += 48
        if key[pygame.K_RIGHT]:
            self.direction = AnimatedSprite.RIGHT
            self.rect.x += 48
            pos_x -= 48

        # TODO: Handle internal wall sides collision.
        if self.rect.x < 0:  # Simple Sides Collision
            self.rect.x = 0  # Reset Player Rect Coord
            # pos_x = camera_pos[0]  # Reset Camera Pos Coord
        elif self.rect.x > int(src.game.Game.WIN_WIDTH - ((src.game.Game.WIN_WIDTH // 24) * 1.5)):
            self.rect.x = int(src.game.Game.WIN_WIDTH - ((src.game.Game.WIN_WIDTH // 24) * 1.5))
            # pos_x = camera_pos[0]
        if self.rect.y < 0:
            self.rect.y = 0
            # pos_y = camera_pos[1]
        elif self.rect.y > src.game.Game.WIN_HEIGHT - 48:
            self.rect.y = src.game.Game.WIN_HEIGHT - 48
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
