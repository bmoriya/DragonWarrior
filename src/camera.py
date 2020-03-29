class Camera:
    def __init__(self, hero_position, map_width, map_height, speed):
        self.map_width = map_width
        self.map_height = map_height
        self.x = None
        self.y = None
        self.set_camera_position(hero_position)
        Camera.speed = speed

    def set_camera_position(self, hero_location):
        # TODO(ELF): move into Camera class.
        # top_left_x = hero_location[0] * TILE_SIZE
        # top_left_y = hero_location[1] * TILE_SIZE
        # return WIN_WIDTH // TILE_SIZE, WIN_HEIGHT // TILE_SIZE

        # TODO: Fix the initial camera_pos calculation.
        # width_midpoint = self.map_width / 2
        # height_midpoint = self.map_height / 2

        # self.x = int((hero_location[0] - self.map_width) * TILE_SIZE)
        # self.y = int((hero_location[1] - self.map_height) * TILE_SIZE)
        # TODO: Figure out math and remove these hardcoded values.
        self.x = -160
        self.y = -96

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
