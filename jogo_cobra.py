import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui import UIManager
from random import randint

# Inicializa o Pygame
pygame.init()

pygame.display.set_caption("Jogo da Cobra")

# Inicializa o mixer de áudio do Pygame
pygame.mixer.init()
pygame.mixer.music.load('neon-gaming-128925.mp3')
pygame.mixer.music.set_volume(0.5)  # Ajustar o volume 
pygame.mixer.music.play(-1)  # -1 significa loop infinito

# Configurações iniciais do jogo
largura = 1280
altura = 720
screen = pygame.display.set_mode((largura, altura))
clock = pygame.time.Clock() # relógio do jogo
running = True # controlar a execução do loop principal

# Inicializa o gestor da interface
ui_manager = UIManager((largura, altura))

# Define as configurações do botão de início
button_start = pygame_gui.elements.UIButton(
    # Está centrado na largura e na metade da altura da tela.
    relative_rect=pygame.Rect((largura // 2 - 100, altura // 2 - 25), (200, 50)),
    text='Iniciar',
    manager=ui_manager
)

# Define as configurações do botão de sair do jogo
button_quit = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((largura // 2 - 100, 400), (200, 50)),
    text='Sair do Jogo',
    manager=ui_manager
)

# Variáveis do jogo
pontos = 0
x_cobra = largura / 2
y_cobra = altura / 2
velocidade = 4.5
x_controlo = velocidade  # Controle de movimento na direção x
y_controlo = 0  # Controle de movimento na direção y
x_maca = randint(200, 600)
y_maca = randint(200, 600)
lista_cobra = []  # Lista que armazena as coordenadas da cobra
comprimento_inicial = 5  # Comprimento inicial da cobra
morte = False  # Variável para controlar o estado de "Game Over"


# Configurações do campo
campo_largura = 800
campo_altura = 600
campo_x = (largura - campo_largura) // 2
campo_y = (altura - campo_altura) // 2

# Configura a fonte para exibir a pontuação
fonte = pygame.font.SysFont("Arial", 40, True, True)

# Função aumentarr a cobra na tela
def aumenta_cobra(lista_cobra):
    # Itera sobre cada ponto (x, y) na lista_cobra
    for x_y in lista_cobra:
        # Desenha um retângulo cinza na tela
        # screen: superfície onde o retângulo será desenhado
        # (128, 128, 128): cor cinza (RGB)
        # (x_y[0], x_y[1], 30, 30): coordenadas e dimensões do retângulo
        pygame.draw.rect(screen, (128, 128, 128), (x_y[0], x_y[1], 30, 30))


# Função para reiniciar o jogo
def reiniciar_jogo():
    global pontos, comprimento_inicial, x_cobra, y_cobra, lista_cobra, lista_cabeca, x_maca, y_maca, morte, jogo_pausado
    pontos = 0
    comprimento_inicial = 5
    x_cobra = largura / 2
    y_cobra = altura / 2
    lista_cobra = []
    lista_cabeca = []
    x_maca = randint(200, 600)
    y_maca = randint(200, 600)
    morte = False
    jogo_pausado = False  # Desativa a pausa ao reiniciar o jogo

# Função para voltar ao início
def voltar_ao_inicio():
    
    global jogo_iniciado, jogo_pausado, button_start, button_quit
    reiniciar_jogo()  # Chama a função de reinicializar
    jogo_iniciado = False
    jogo_pausado = False

    # Define as configurações do botão de início
    button_start = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((largura // 2 - 100, altura // 2 - 25), (200, 50)),
        text='Iniciar',
        manager=ui_manager)
    
    # Define as configurações do botão de sair do jogo
    button_quit = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((largura // 2 - 100, 400), (200, 50)),
        text='Sair do Jogo',
        manager=ui_manager)


# Sinalizador para verificar se o jogo foi iniciado
jogo_iniciado = False
jogo_pausado = False

# Loop principal do jogo
while running:

    # Captura as teclas pressionadas
    keys = pygame.key.get_pressed()

    # Limpa a tela com uma cor (background preto)
    screen.fill("black")

    # Desenha o campo retangular
    pygame.draw.rect(screen, (0, 255, 0), (campo_x, campo_y, campo_largura, campo_altura), 2)

    # Exibe a pontuação na tela
    mensagem = "Pontos: " + str(pontos)
    texto_formatado = fonte.render(mensagem, True, (255, 255, 255))

    # Atualiza a interface
    time_delta = clock.tick(60)
    ui_manager.update(time_delta)

    # Desenha o botão na tela
    ui_manager.draw_ui(screen)

    # Verifica se o jogo foi iniciado antes de atualizar o jogo
    if jogo_iniciado and not jogo_pausado:

        # Controle de volume da música no botão de maior para aumentar
        if keys[pygame.K_PLUS] or keys[pygame.K_KP_PLUS]:
            volume = pygame.mixer.music.get_volume()
            if volume < 1.0:
                volume += 0.05  # Aumenta o volume 
                pygame.mixer.music.set_volume(volume)

        # Controle de volume da música no botão de menor para diminuir
        if keys[pygame.K_MINUS] or keys[pygame.K_KP_MINUS]:
            volume = pygame.mixer.music.get_volume()
            if volume > 0.0:
                volume -= 0.05  # Diminui o volume 
                pygame.mixer.music.set_volume(volume)
        
        # Configura os valores de movimento com base nas teclas pressionadas
        move_left = keys[pygame.K_a]
        move_right = keys[pygame.K_d]
        move_up = keys[pygame.K_w]
        move_down = keys[pygame.K_s]

        # Atualiza a direção da cobra com base nas teclas pressionadas
        # Se a tecla para a esquerda estiver a ser pressionada, verifica se a cobra não está já a ir para a direita 
        if move_left:
            if x_controlo == velocidade:
                pass
            # Se Se não estiver a ir para a direita, atualiza a direção da cobra para a esquerda   
            else:
                x_controlo = -velocidade
                # A direção vertical é mantida como zero, indicando que a cobra não está a movimentar-se verticalmente.
                y_controlo = 0
        if move_right:
            if x_controlo == -velocidade:
                pass
            else:
                x_controlo = velocidade
                y_controlo = 0
        if move_up:
            if y_controlo == velocidade:
                pass
            else:
                y_controlo = -velocidade
                x_controlo = 0
        if move_down:
            if y_controlo == -velocidade:
                pass
            else:
                y_controlo = velocidade
                x_controlo = 0

        # Atualiza as coordenadas da cabeça da cobra
        # Estas variáveis determinam a direção na qual a cobra se está a mover. 
        x_cobra = x_cobra + x_controlo # Direção Horizontal
        y_cobra = y_cobra + y_controlo # Direção Vertical

        # Garante que a cobra não saia do campo
        # A cobra não pode ser menor que a borda esquerda e nem maior do que a borda direita
        x_cobra = max(campo_x, min(x_cobra, campo_x + campo_largura - 30))
        y_cobra = max(campo_y, min(y_cobra, campo_y + campo_altura - 30))

        # Renderiza a pontuação na tela
        screen.blit(texto_formatado, (1100, 40))

        # Desenha a cobra na tela
        cobra = pygame.draw.rect(screen, (128, 128, 128), (x_cobra, y_cobra, 30, 30))

        # Carrega a imagem da maçã
        maça_imagem = pygame.image.load('maça.png')

        # Desenha a maça com a imagem na tela
        largura_maca = 35
        altura_maca = 35

        # Redimensiona a imagem da maçã
        maça_imagem = pygame.transform.scale(maça_imagem, (largura_maca, altura_maca))
        maca = maça_imagem.get_rect(topleft=(x_maca, y_maca))
        screen.blit(maça_imagem, maca)

        # Verifica se a cobra colidiu com a maçã
        if cobra.colliderect(maca):
            x_maca = randint(campo_x, campo_x + campo_largura - 30)  # Reposiciona a maçã dentro dos limites da tela
            y_maca = randint(campo_y, campo_y + campo_altura - 30)  # Reposiciona a maçã dentro dos limites da tela
            pontos += 1
            comprimento_inicial += 1

        # Atualiza a lista de coordenadas da cobra
        lista_cabeca = [] # Coordenadas da cabeça da cobra no momento específico
        lista_cabeca.append(x_cobra) # Adiciona as coordenadas atuais da cabeça da cobra 
        lista_cabeca.append(y_cobra)
        lista_cobra.append(lista_cabeca) # Adiciona as coordenadas da cabeça atual na lista principal.
                                         # Isso atualiza a lista com as coordenadas mais recentes da cobra.

        # Verifica colisões com o próprio corpo da cobra
        if lista_cobra.count(lista_cabeca) > 1:
            fonte_2 = pygame.font.SysFont("arial", 40, True, True)
            mensagem = "Game Over! Clica R para jogar outra vez!"
            texto_formatado = fonte_2.render(mensagem, True, (0, 0, 0))
            ret_texto = texto_formatado.get_rect()

            morte = True
            while morte:
                # Tela fica branca
                screen.fill("white")
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_r:
                            reiniciar_jogo()

                ret_texto.center = (largura // 2, altura // 2)
                screen.blit(texto_formatado, ret_texto)
                pygame.display.update()

        # Remove as coordenadas mais antigas da cobra se for mais longa que o comprimento inicial
        if len(lista_cobra) > comprimento_inicial:
            del lista_cobra[0]

        # Aumenta e desenha a cobra na tela
        aumenta_cobra(lista_cobra)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Eventos do Pygame GUI
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == button_start:
                    # Botões ficam desativados
                    button_start.visible = False
                    button_quit.visible = False
                    reiniciar_jogo()
                    jogo_iniciado = True
                    jogo_pausado = False
                elif event.ui_element == button_quit:
                    # Encerra o jogo
                    pygame.quit()
                    exit()

        # Eventos de teclado
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if jogo_iniciado:
                    jogo_pausado = not jogo_pausado         
            elif event.key == pygame.K_r and jogo_pausado:
                reiniciar_jogo()
            elif event.key == pygame.K_i:
                voltar_ao_inicio()
                
        # Processa todos os eventos        
        ui_manager.process_events(event)

    # Se o jogo estiver pausado, exibe as mensagens
    if jogo_pausado:
        fonte_pausa = pygame.font.SysFont("arial", 40, True, True)
        mensagem_pausa = "Jogo Pausado"
        texto_formatado_pausa = fonte_pausa.render(mensagem_pausa, True, (255, 255, 255))
        ret_texto_pausa = texto_formatado_pausa.get_rect()
        ret_texto_pausa.center = (largura // 2, 200)
        screen.blit(texto_formatado_pausa, ret_texto_pausa)

        fonte_pausa = pygame.font.SysFont("arial", 40, True, True)
        mensagem_pausa = "Pressione P para Continuar"
        texto_formatado_pausa = fonte_pausa.render(mensagem_pausa, True, (255, 255, 255))
        ret_texto_pausa = texto_formatado_pausa.get_rect()
        ret_texto_pausa.center = (largura // 2, altura // 2)
        screen.blit(texto_formatado_pausa, ret_texto_pausa)

        fonte_pausa2 = pygame.font.SysFont("arial", 40, True, True)
        mensagem_pausa2 = "Pressione R para Reiniciar"
        texto_formatado_pausa2 = fonte_pausa2.render(mensagem_pausa2, True, (255, 255, 255))
        ret_texto_pausa2 = texto_formatado_pausa2.get_rect()
        ret_texto_pausa2.center = (largura // 2, 430)
        screen.blit(texto_formatado_pausa2, ret_texto_pausa2)

        fonte_pausa2 = pygame.font.SysFont("arial", 40, True, True)
        mensagem_pausa2 = "Pressione I para voltar ao Início "
        texto_formatado_pausa2 = fonte_pausa2.render(mensagem_pausa2, True, (255, 255, 255))
        ret_texto_pausa2 = texto_formatado_pausa2.get_rect()
        ret_texto_pausa2.center = (largura // 2, 500)
        screen.blit(texto_formatado_pausa2, ret_texto_pausa2)

    # Desenha os botões apenas se o jogo estiver iniciado
    # Verifica se o jogo não está iniciado (not jogo_iniciado) ou se está pausado (jogo_pausado)
    if not jogo_iniciado or jogo_pausado:
        ui_manager.draw_ui(screen)

    # Atualiza a tela
    pygame.display.flip()  

    # Atualiza partes específicas da tela
    # Este comando é utilizado para garantir que todas as alterações feitas na tela sejam visíveis para o jogador
    pygame.display.update()

pygame.quit()
