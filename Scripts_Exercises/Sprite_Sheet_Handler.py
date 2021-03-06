import pygame


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)

    def image_at(self, rectangle, colourkey=None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colourkey is not None:
            if colourkey is -1:
                colourkey = image.get_at((0, 0))
            image.set_colorkey(colourkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colourkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colourkey) for rect in rects]

    def load_strip(self, rect, image_count, colourkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colourkey)
