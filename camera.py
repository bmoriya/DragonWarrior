from config import TILE_SIZE
from maps import TantegelThroneRoom, TantegelCourtyard, TestMap


class Camera:
    def __init__(self, hero_position, current_map, speed):
        self.current_map = current_map
        self.x = None
        self.y = None
        self.set_camera_position(hero_position)
        Camera.speed = speed

    def set_camera_position(self, hero_position: tuple):
        """
        Sets the camera position.
        :type hero_position: tuple
        :param hero_position: Position of the hero, in (column, row) format.
        """
        self.x = (-hero_position[0] + 8) * TILE_SIZE
        self.y = (-hero_position[1] + 7) * TILE_SIZE

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, coord):
        self.x = coord[0]
        self.y = coord[1]
        # TODO: Investigate Python getters/setters (prop and props live templates?)

        # width_midpoint = len(self.current_map.layout[0]) / 2
        # height_midpoint = len(self.current_map.layout) / 2
        # if self.hero_layout_row <= height_midpoint and self.hero_layout_column <= width_midpoint:
        #     self.camera_pos = Camera.set_camera_position((int((self.hero_layout_column - width_midpoint) * 10),
        #                                                   (int(self.hero_layout_row - height_midpoint) * 2)))
        # elif self.hero_layout_row <= height_midpoint and self.hero_layout_column >= width_midpoint:
        #     self.camera_pos = Camera.set_camera_position(
        #         (int(self.hero_layout_row - width_midpoint), int(self.hero_layout_column - width_midpoint)))
        # elif self.hero_layout_row >= height_midpoint and self.hero_layout_column <= width_midpoint:
        #     self.camera_pos = Camera.set_camera_position(
        #         (int(self.hero_layout_row - width_midpoint), int(self.hero_layout_column - width_midpoint)))
        # elif self.hero_layout_row >= height_midpoint and self.hero_layout_column >= width_midpoint:
        #     self.camera_pos = Camera.set_camera_position(
        #         (int(self.hero_layout_row - width_midpoint), int(self.hero_layout_column - width_midpoint)))
        # else:
        #     self.camera_pos = Camera.set_camera_position((width_midpoint - self.hero_layout_row,
        #                                                   height_midpoint - self.hero_layout_column))

        # AIMING FOR -5, -3 (or -160, -96 when multiplied by TILE_SIZE) for Tantegel Throne Room
        # self.camera_pos = 2 * TILE_SIZE, 4 * TILE_SIZE

    def move(self, direction):
        # TODO: Migrate game move method here.
        pass
