from src.config import TILE_SIZE


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
        """
        Gets the position of a particular rectangle.
        """
        return self.x, self.y

    def set_pos(self, coord):
        """
        Sets the position of a particular rectangle.
        """
        self.x = coord[0]
        self.y = coord[1]
        # TODO: Investigate Python getters/setters (prop and props live templates?)

    def move(self, direction):
        # TODO: Migrate game move method here.
        pass
