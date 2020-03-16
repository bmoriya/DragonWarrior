import pygame

from src import maps
from src.animated_sprite import AnimatedSprite
from src.common import Direction, play_sound, bump_sfx
from src.config import TILE_SIZE


class Player(AnimatedSprite):

    def __init__(self, center_point, down_img, left_img, up_img, right_img, direction=Direction.DOWN.value):
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

    # def render(self, display):
    # display.blit(self.image, (self.rect.x, self.rect.y))

    # TODO: Move only if button is pressed for 0.5 seconds.

    def move(self, camera_pos, current_map_width, current_map_height, current_map_layout, current_map_impassable_tiles):
        # TODO: Smooth out movement.
        key = pygame.key.get_pressed()
        pos_x, pos_y = camera_pos
        current_hero_layout_x_pos = self.rect.y // TILE_SIZE
        current_hero_layout_y_pos = self.rect.x // TILE_SIZE
        if key[pygame.K_DOWN]:
            self.direction = Direction.DOWN.value
            if self.get_tile_by_value(
                    current_map_layout[current_hero_layout_x_pos + 1][
                        current_hero_layout_y_pos]) not in current_map_impassable_tiles:
                self.rect.y += TILE_SIZE
                pos_y -= TILE_SIZE
        if key[pygame.K_LEFT]:
            self.direction = Direction.LEFT.value
            if self.get_tile_by_value(current_map_layout[current_hero_layout_x_pos][
                                          current_hero_layout_y_pos - 1]) not in current_map_impassable_tiles:
                self.rect.x -= TILE_SIZE
                pos_x += TILE_SIZE
        if key[pygame.K_UP]:
            self.direction = Direction.UP.value
            if self.get_tile_by_value(
                    current_map_layout[current_hero_layout_x_pos - 1][
                        current_hero_layout_y_pos]) not in current_map_impassable_tiles:
                self.rect.y -= TILE_SIZE
                pos_y += TILE_SIZE
        if key[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT.value
            if self.get_tile_by_value(
                    current_map_layout[current_hero_layout_x_pos][
                        current_hero_layout_y_pos + 1]) not in current_map_impassable_tiles:
                self.rect.x += TILE_SIZE
                pos_x -= TILE_SIZE

        # bump_sound = pygame.mixer.Sound(bump_sound_dir)
        pos_x, pos_y = self.handle_map_edge_side_collision(camera_pos, current_map_height, current_map_width, pos_x,
                                                           pos_y)

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

    @staticmethod
    def get_tile_by_value(position):
        return maps.tile_key_keys[maps.tile_key_values.index(position)]

    def handle_map_edge_side_collision(self, camera_pos, current_map_height, current_map_width, pos_x, pos_y):
        if self.rect.x < 0:  # Simple Sides Collision
            self.rect.x = 0  # Reset Player Rect Coord
            play_sound(bump_sfx)
            pos_x = camera_pos[0]  # Reset Camera Pos Coord
        elif self.rect.x > current_map_width - TILE_SIZE:
            self.rect.x = current_map_width - TILE_SIZE
            play_sound(bump_sfx)
            pos_x = camera_pos[0]
        if self.rect.y < 0:
            self.rect.y = 0
            play_sound(bump_sfx)
            pos_y = camera_pos[1]
        elif self.rect.y > current_map_height - TILE_SIZE:
            self.rect.y = current_map_height - TILE_SIZE
            play_sound(bump_sfx)
            pos_y = camera_pos[1]
        return int(pos_x), int(pos_y)
        # for reference:
        # current_map_height - TILE_SIZE is equal to WIN_HEIGHT - ((WIN_HEIGHT // 23) * 1.5)
