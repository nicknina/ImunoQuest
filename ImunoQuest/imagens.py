import pygame


class Sprites():
    def __init__(self, imagem):
        self.folha = imagem

    def pegar_imagem(self, frame_x, lagura,altura, escala, cor):
        imagem = pygame.Surface((lagura, altura), pygame.SRCALPHA).convert_alpha()
        imagem.blit(self.folha, (0,0), ((frame_x * lagura), 0, lagura, altura))
        imagem = pygame.transform.scale(imagem, (lagura * escala, altura * escala))
        imagem.set_colorkey(cor)

        return imagem
