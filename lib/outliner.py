import pygame


class Outliner:
    def __init__(self):
        self.convolution_mask = pygame.mask.Mask((3, 3), fill = True)
        self.convolution_mask.set_at((0, 0), value = 0)
        self.convolution_mask.set_at((2, 0), value = 0)
        self.convolution_mask.set_at((0, 2), value = 0)
        self.convolution_mask.set_at((2, 2), value = 0)
    
    def outline_surface(self, surface, color = 'black', outline_only = False):
        mask = pygame.mask.from_surface(surface)
        surface_outline = mask.convolve(self.convolution_mask).to_surface(setcolor = color, unsetcolor = None)
        
        if outline_only:
            mask_surface = mask.to_surface()
            mask_surface.set_colorkey('black')
            surface_outline.blit(mask_surface, (1, 1))
            
        else:
            surface_outline.blit(surface, (2, 2))
        
        return surface_outline
