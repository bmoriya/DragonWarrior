class BaseMap(object):

    def __init__(self, animated_sprites=[], static_sprites=[]):
        self.animated_sprites = animated_sprites
        self.static_sprites = static_sprites

    def get_layout(self):
        pass

    def animate_sprites(self, surface):
        for sprite in self.animated_sprites:
            sprite.animate(surface)
