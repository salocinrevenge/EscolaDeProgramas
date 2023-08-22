import pygame
import sys
import time




class Coracao():
    timetick = 1/60

    def __init__(self) -> None:
        # Inicialização do Pygame
        pygame.init()

        # Configurações da tela
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("SmartSnake")

        self.scale = 10
        self.estado = "inicio"
        self.objects = []

        self.run()


    def run(self):
        # Loop principal
        running = True
        last_time = time.time()
        while running:
            actual_time = time.time()
            # Calcular dt
            dt = actual_time - last_time

            # Limitar a 60 fps
            while dt >= self.timetick:
                last_time = actual_time
                dt -= self.timetick
                # Tick
                self.tick()

            # Input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.render()
            

            

            

        # Encerrar o Pygame
        pygame.quit()
        sys.exit()

    def tick(self):
        self.controlador()
        for obj in self.objects:
            obj.tick()

    def render(self):
        # Preencher a tela com a cor preta
        self.screen.fill((255, 255, 255))

        # Render objects
        for obj in self.objects:
            obj.render()
            
        # Atualizar a tela
        pygame.display.flip()

    def controlador(self):
        if self.estado == "inicio":
            self.objects.append(Snake(self))
            self.objects.append(Food(self))
            self.estado = "jogando"
        elif self.estado == "jogando":
            pass
        elif self.estado == "gameover":
            pass

class Snake():
    def __init__(self) -> None:
        self.body = []

    def render(self):
        # Desenhar o corpo
        pygame.draw.rect(self.screen, self.cor, (self.pos[0], self.pos[1], self.tamanho, self.tamanho))

class SnakePart():
    def __init__(self, tamanho, pos) -> None:
        self.tamanho = tamanho
        self.cor = (0,255,0)
        self.pos = pos

    def render(self):
        # Desenhar o corpo
        pygame.draw.rect(self.screen, self.cor, (self.pos[0], self.pos[1], self.tamanho, self.tamanho))


class Food():
    def __init__(self) -> None:
        pass