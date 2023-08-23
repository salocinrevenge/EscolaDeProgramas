import pygame
import sys
import time
import random

class Coracao():
    timetick = 1/60

    def __init__(self) -> None:
        # Inicialização do Pygame
        pygame.init()

        # Configurações da tela
        self.screen_dimension = 800
        self.screen = pygame.display.set_mode((self.screen_dimension, self.screen_dimension))
        pygame.display.set_caption("SmartSnake")

        self.tamanhoMapa = 10 * 2
        self.estado = "inicio"
        self.mapa = []
        self.scale = self.screen_dimension // self.tamanhoMapa
        self.objects = []
        self.run()


    def run(self):
        # Loop principal
        self.running = True
        last_time = time.time()
        while self.running:
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
            self.input()
            

            self.render()            

        # Encerrar o Pygame
        pygame.quit()
        sys.exit()

    def input(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.player.vel=(0,-1)
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.player.vel=(0,1)
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.player.vel=(-1,0)
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.player.vel=(1,0)

    def tick(self):
        self.controlador()
        for obj in self.objects:
            retorno = obj.tick()
            if retorno != None:
                # verifica se retorno é uma instancia de Food
                if isinstance(retorno, Food):
                    self.objects.remove(retorno)
                    if len(self.player.body)+1 == self.tamanhoMapa**2:
                        self.estado = "gameover"
                        print("Você ganhou!")
                        self.running = False
                        return
                    self.adicionarComida()
                elif isinstance(retorno, SnakePart):
                    self.estado = "gameover"
                    self.running = False
                    print("Você perdeu!")
                    return

    def desenhaTabuleiro(self):
        for i in range(len(self.mapa)):
            for j in range(len(self.mapa[0])):
                if self.mapa[i][j] == None:
                    pygame.draw.rect(self.screen, (0,0,0), (i*self.scale, j*self.scale, self.scale, self.scale))
                elif isinstance(self.mapa[i][j], Snake):
                    pygame.draw.rect(self.screen, (0,255,0), (i*self.scale, j*self.scale, self.scale, self.scale))
                elif isinstance(self.mapa[i][j], SnakePart):
                    pygame.draw.rect(self.screen, (20,170,20), (i*self.scale, j*self.scale, self.scale, self.scale))
                elif isinstance(self.mapa[i][j], Food):
                    pygame.draw.rect(self.screen, (255,0,0), (i*self.scale, j*self.scale, self.scale, self.scale))

    def render(self):
        # Preencher a tela com a cor preta
        self.screen.fill((0, 0, 0))

        self.desenhaTabuleiro()

        # Render objects
        for obj in self.objects:
            obj.render(self.screen)
            
        # Atualizar a tela
        pygame.display.flip()

    def iniciarMapa(self):
        for i in range(self.tamanhoMapa):
            self.mapa.append([])
            for j in range(self.tamanhoMapa):
                self.mapa[i].append(None)

    def adicionarComida(self):
        x = random.randint(0,self.tamanhoMapa-1)
        y = random.randint(0,self.tamanhoMapa-1)
        while self.mapa[x][y] != None:
            x = random.randint(0,self.tamanhoMapa-1)
            y = random.randint(0,self.tamanhoMapa-1)
        comida = Food(self,(x,y))
        self.mapa[x][y] = comida
        self.objects.append(comida)
        self.comida = comida

    def controlador(self):
        if self.estado == "inicio":
            self.iniciarMapa()
            self.player = Snake(self, (self.tamanhoMapa//2,self.tamanhoMapa//2) )
            self.objects.append(self.player)
            self.mapa[self.tamanhoMapa//2][self.tamanhoMapa//2] = self.player
            self.adicionarComida()
            self.estado = "jogando"
        elif self.estado == "jogando":
            pass
        elif self.estado == "gameover":
            pass

class Snake():
    def __init__(self, jogo, pos) -> None:
        self.body = []
        self.escala = jogo.scale
        self.pos = pos
        self.jogo = jogo
        self.cor = (0,255,0)
        self.vel = [0,0]
        self.contador = 0

    decisao = {(0,0):[(1,0), (0,-1)], (1,0):[(0,1), (1,0)], (0,1):[(-1,0), (0,-1)], (1,1):[(0,1), (-1,0)]}
    def brain(self):
        opcoes = self.decisao[(self.pos[0]%2, self.pos[1]%2)].copy()
        # calcula a distancia de manhattan entre a cabeca e a comida de todas opcoes
        for i in range(len(opcoes)):
            distancia = abs(self.jogo.comida.pos[0]-(self.pos[0]+opcoes[i][0])) + abs(self.jogo.comida.pos[1]-(self.pos[1]+opcoes[i][1]))
            opcoes[i] = (opcoes[i], distancia)
        
        # verifica quais opcoes sao validas
        validos = []
        for opcao in opcoes:
            if self.pos[0]+opcao[0][0] >= 0 and self.pos[0]+opcao[0][0] < self.jogo.tamanhoMapa and self.pos[1]+opcao[0][1] >= 0 and self.pos[1]+opcao[0][1] < self.jogo.tamanhoMapa:
                if self.jogo.mapa[self.pos[0]+opcao[0][0]][self.pos[1]+opcao[0][1]] == None or isinstance(self.jogo.mapa[self.pos[0]+opcao[0][0]][self.pos[1]+opcao[0][1]], Food):
                    validos.append(opcao)
        


        # guarda a menor distancia e se alguem possuir uma distancia maior que ela, é removido.
        menor = validos[0][1]
        for i in range(len(validos)):
            if validos[i][1] < menor:
                menor = validos[i][1]
        for i in range(len(validos)-1,-1,-1):
            if validos[i][1] > menor:
                validos.pop(i)
        
        # se ainda houver mais de uma opcao valida, escolhe uma aleatoria
        if len(validos) == 0:
            return
        if len(validos) == 1:
            self.vel = validos[0][0]
            return
        
        self.vel = validos[random.randint(0,len(validos)-1)][0]
        

    def mover(self, direcao, comeu=False):
        # se direcao for (0,0) nao faz nada
        if direcao[0] == 0 and direcao[1] == 0:
            return
        # Atualiza a posicao da cabeca no mapa
        self.jogo.mapa[self.pos[0]][self.pos[1]] = None
        if comeu:
            self.body.insert(0, SnakePart(self.jogo, (self.pos[0], self.pos[1])))
            self.jogo.mapa[self.pos[0]][self.pos[1]] = self.body[0]
            self.pos = (self.pos[0] + direcao[0], self.pos[1] + direcao[1])
            self.jogo.mapa[self.pos[0]][self.pos[1]] = self
        else:
            if len(self.body) > 0:
                # Atualiza a posicao do rabo
                rabo = self.body.pop()
                self.jogo.mapa[rabo.pos[0]][rabo.pos[1]] = None
                rabo.pos = (self.pos[0], self.pos[1])
                self.body.insert(0, rabo)
                self.jogo.mapa[self.pos[0]][self.pos[1]] = self.body[0]
            # Atualiza a posicao da cabeca
            self.pos = (self.pos[0] + direcao[0], self.pos[1] + direcao[1])

            # Atualiza a posicao da cabeca no mapa
            self.jogo.mapa[self.pos[0]][self.pos[1]] = self


    def tick(self):
        self.contador+=1
        if self.contador < 4:
            return None
        self.contador = 0
        self.brain()
        posAlvo = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        # se posAlvo for fora do mapa
        if posAlvo[0] < 0 or posAlvo[0] >= self.jogo.tamanhoMapa or posAlvo[1] < 0 or posAlvo[1] >= self.jogo.tamanhoMapa:
            return None
        atual = self.jogo.mapa[posAlvo[0]][posAlvo[1]]
        self.mover(self.vel, True if isinstance(atual, Food) else False)
        for parte in self.body:
            parte.tick()
        return atual

    def render(self, tela):
        # Desenhar o corpo
        pygame.draw.rect(tela, self.cor, (self.pos[0]*self.jogo.scale, self.pos[1]*self.jogo.scale, self.escala, self.escala))
        for i in range(len(self.body)):
            self.body[i].render(tela,(i,len(self.body)))

class SnakePart():
    def __init__(self, jogo, pos) -> None:
        self.escala = jogo.scale
        self.jogo = jogo
        self.corbase = (20,170,20)
        self.pos = pos

    def render(self, tela, corI): # corI = (index, maxIndex)
        # Desenhar o corpo
        cor = (self.corbase[0] + (255-self.corbase[0])*(corI[0]/corI[1]), self.corbase[1] + (255-self.corbase[1])*(corI[0]/corI[1]), self.corbase[2] + (255-self.corbase[2])*(corI[0]/corI[1]))
        pygame.draw.rect(tela, cor, (self.pos[0]*self.jogo.scale, self.pos[1]*self.jogo.scale, self.escala, self.escala))
    
    def tick(self):
        pass


class Food():
    def __init__(self, jogo, pos) -> None:
        self.jogo = jogo
        self.pos = pos
        self.escala = jogo.scale
        self.cor = (255,0,0)
        pass

    def tick(self):
        pass

    def render(self, tela):
        # Desenhar a maca
        pygame.draw.rect(tela, self.cor, (self.pos[0]*self.jogo.scale, self.pos[1]*self.jogo.scale, self.escala, self.escala))
        pass

if __name__ == "__main__":
    Coracao()