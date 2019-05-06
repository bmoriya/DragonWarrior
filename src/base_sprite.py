from pygame.sprite import Sprite


class BaseSprite(Sprite):
    """
    All sprites in this game need this basic functionality.
    """

    def __init__(self, center_pt, image):
        """
        Constructor
        """
        Sprite.__init__(self)

        # Set up the image and rect for the image.
        self.image = image
        self.rect = image.get_rect()

        # Ensure rect is centered, makes it image size independent.
        self.rect.center = center_pt
