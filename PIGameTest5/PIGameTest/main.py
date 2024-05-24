# Colocar perguntas no Banco de dados
# Jutar a tela de dificuldade com o inicio do jogo
# Fazer a tela de fugir voltar para a tela de dificuldade
# Fazer depois da tela de vitoria voltar para a tela de dificuldade
# Criar aba do professor com lista de perguntas, adicionar pergunta e remover pergunta


import pygame
import random
from imagens import Sprites
from perguntas import questions

# Escolha da dificuldade
dificuldade = int(input("Escolha a sua dificuldade (1/2/3): "))

# Inicialização do Pygame
pygame.init()

# Definições de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 0, 0)

# Definições de tela
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Quiz_Imunoquest')
background_image = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\background_quiz.png').convert()
BG = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\background.png').convert()

# Definições de fonte
font = pygame.font.Font("C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\font.ttf", 25)
font_textos = pygame.font.Font("C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\font.ttf", 10)

# Mudanças por dificuldade
if dificuldade == 1:    
    imagem_inimigo = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\inimigo_facil.png').convert_alpha()
    vida_inimigo = 10
    tamanho = 0.4
elif dificuldade == 2:
    imagem_inimigo = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\inimigo_medio.png').convert_alpha()
    vida_inimigo = 15
    tamanho = 0.3
elif dificuldade == 3:
    imagem_inimigo = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\inimigo_dificil.png').convert_alpha()
    vida_inimigo = 20
    tamanho = 0.4

imagens = Sprites(imagem_inimigo)

# Lista de animação do inimigo
lista_animacao = []
etapas_animacao = [6]  # Lista de frames para cada animação
acao = 0  # Ação realizada
# 0 idle
ultima_atualizacao = pygame.time.get_ticks()
cooldown_animacao = 150
frame = 0
contador_etapa = 0

# Loop que gera animação do inimigo
for animacao in etapas_animacao:
    lista_temporaria_img = []
    for _ in range(animacao):
        lista_temporaria_img.append(imagens.pegar_imagem(contador_etapa, 1000, 1000, tamanho, RED))
        contador_etapa += 1
    lista_animacao.append(lista_temporaria_img)

# Função para desenhar a tela de introdução
def draw_intro_screen():
    global frame, ultima_atualizacao

    screen.blit(background_image, (0, 0))

    # Apresenta o inimigo junto com sua animação
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultima_atualizacao >= cooldown_animacao:
        frame += 1
        ultima_atualizacao = tempo_atual
        if frame >= len(lista_animacao[acao]):
            frame = 0

    # Exibir animação
    if dificuldade == 2:
       screen.blit(lista_animacao[acao][frame], (800, 100))
    else:
        screen.blit(lista_animacao[acao][frame], (750, -10))

    # Desenha o texto de introdução
    intro_text = font.render("Um vírus selvagem se aproxima", True, BLACK)
    intro_rect = intro_text.get_rect(bottomleft=(10, SCREEN_HEIGHT - 50))
    screen.blit(intro_text, intro_rect)

    # Desenha o botão de batalha
    button_width = 250
    button_height = 50
    button_x = SCREEN_WIDTH - 300
    button_y = SCREEN_HEIGHT - 100
    battle_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GRAY, battle_button_rect)
    battle_text = font.render("Batalhar", True, BLACK)
    battle_text_rect = battle_text.get_rect(center=battle_button_rect.center)
    screen.blit(battle_text, battle_text_rect)

    pygame.display.flip()

# Função para desenhar a tela da pergunta com botões de resposta e de fugir
def draw_question_screen(question_data, vida_inimigo, max_vida_inimigo, mostrar_dano_critico, mostrar_penalidade):
    screen.fill(GRAY)

    # Desenha a pergunta
    question_text = font_textos.render(question_data["question"], True, BLACK)
    question_rect = question_text.get_rect(center=(600, SCREEN_HEIGHT - 650))
    screen.blit(question_text, question_rect)

    # Desenha os botões de resposta
    button_width = 1000
    button_height = 60
    button_spacing = 25
    total_button_height = button_height + button_spacing
    button_x = SCREEN_WIDTH / 2 - button_width / 2
    button_y = 200

    for i, answer in enumerate(question_data["answers"]):
        button_rect = pygame.Rect(button_x, button_y + i * total_button_height, button_width, button_height)
        pygame.draw.rect(screen, RED, button_rect)

        text_surface = font_textos.render(f"{answer['option'].upper()}: {answer['text']}", True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    # Desenha o botão de fugir
    flee_button_rect = pygame.Rect(button_x, button_y + (i + 1) * total_button_height, button_width, button_height)
    pygame.draw.rect(screen, RED, flee_button_rect)
    flee_text = font.render("Fugir", True, BLACK)
    flee_text_rect = flee_text.get_rect(center=flee_button_rect.center)
    screen.blit(flee_text, flee_text_rect)

    # Desenha a barra de vida do inimigo
    life_bar_width = 400
    life_bar_height = 30
    life_bar_x = SCREEN_WIDTH // 2 - life_bar_width // 2
    life_bar_y = SCREEN_HEIGHT - 100
    life_ratio = vida_inimigo / max_vida_inimigo
    current_life_width = life_bar_width * life_ratio

    pygame.draw.rect(screen, BLACK, (life_bar_x, life_bar_y, life_bar_width, life_bar_height))
    pygame.draw.rect(screen, RED, (life_bar_x, life_bar_y, current_life_width, life_bar_height))

    # Desenha a mensagem de dano crítico
    if mostrar_dano_critico:
        crit_text = font.render("Dano Crítico!", True, RED)
        crit_rect = crit_text.get_rect(center=(SCREEN_WIDTH // 2, life_bar_y + 60))
        screen.blit(crit_text, crit_rect)

    # Desenha a mensagem de penalidade
    if mostrar_penalidade:
        penalty_text = font.render("+5 seg", True, RED)
        penalty_rect = penalty_text.get_rect(center=(life_bar_x + life_bar_width + 80, life_bar_y + life_bar_height // 2))
        screen.blit(penalty_text, penalty_rect)

    pygame.display.flip()

# Função para desenhar a tela de fuga
def draw_flee_screen():
    global frame, ultima_atualizacao

    screen.blit(background_image, (0, 0))

    # Apresenta o inimigo junto com sua animação
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultima_atualizacao >= cooldown_animacao:
        frame += 1
        ultima_atualizacao = tempo_atual
        if frame >= len(lista_animacao[acao]):
            frame = 0

    # Exibir animação
    screen.blit(lista_animacao[acao][frame], (750, -10))

    flee_text = font.render("Você fugiu!", True, BLACK)
    flee_rect = flee_text.get_rect(bottomleft=(10, SCREEN_HEIGHT - 50))
    screen.blit(flee_text, flee_rect)

    pygame.display.flip()

# Função para desenhar a tela de vitória
def draw_victory_screen(score):
    screen.blit(BG, (0, 0))

    victory_text = font.render("Você venceu!", True, WHITE)
    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(victory_text, victory_rect)

    # Convertendo o score de milissegundos para minutos, segundos e milissegundos
    minutes = score // 60000
    seconds = (score % 60000) // 1000
    milliseconds = score % 1000

    score_text = font.render(f"Pontuação: {minutes} min {seconds} seg", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(score_text, score_rect)

    pygame.display.flip()

# Função principal
def main():
    global vida_inimigo  # Declare vida inimigo como global para ser acessível aqui

    # Embaralha as perguntas
    random.shuffle(questions)

    current_question_index = 0
    intro_screen = True
    flee_screen = False
    victory_screen = False
    pontos = 0
    sequencia = 0
    start_time = pygame.time.get_ticks()
    score = 0
    mostrar_dano_critico = False
    mostrar_penalidade = False
    penalidade_start_time = 0
    max_vida_inimigo = vida_inimigo

    while True:
        if intro_screen:
            draw_intro_screen()
        elif flee_screen:
            draw_flee_screen()
        elif victory_screen:
            draw_victory_screen(score)
        else:
            draw_question_screen(questions[current_question_index], vida_inimigo, max_vida_inimigo, mostrar_dano_critico, mostrar_penalidade)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                if intro_screen:
                    button_width = 250
                    button_height = 50
                    button_x = SCREEN_WIDTH - 300
                    button_y = SCREEN_HEIGHT - 100
                    battle_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

                    if battle_button_rect.collidepoint(mouse_x, mouse_y):
                        intro_screen = False

                elif flee_screen:
                    pygame.quit()
                    return

                elif victory_screen:
                    pygame.quit()
                    return

                else:
                    button_width = 1000
                    button_height = 60
                    button_spacing = 25
                    total_button_height = button_height + button_spacing
                    button_x = SCREEN_WIDTH / 2 - button_width / 2
                    button_y = 200

                    for i, answer in enumerate(questions[current_question_index]["answers"]):
                        button_rect = pygame.Rect(button_x, button_y + i * total_button_height, button_width, button_height)
                        if button_rect.collidepoint(mouse_x, mouse_y):
                            # Verifica se a resposta está correta
                            if answer["option"] == questions[current_question_index]["correct_answer"]:
                                print("Resposta correta!")
                                pontos += 1
                                sequencia += 1
                                if sequencia % 3 == 0:
                                    vida_inimigo -= 3
                                    mostrar_dano_critico = True
                                else:
                                    vida_inimigo -= 1
                                    mostrar_dano_critico = False
                                if vida_inimigo <= 0:
                                    victory_screen = True
                                    score = pygame.time.get_ticks() - start_time
                                    break
                            else:
                                print("Resposta incorreta!")
                                sequencia = 0
                                mostrar_dano_critico = False
                                mostrar_penalidade = True
                                penalidade_start_time = pygame.time.get_ticks()
                                # Adiciona penalidade de 5 segundos
                                start_time -= 5000

                            print("Sua sequência é de", sequencia)
                            print("Vida do inimigo:", vida_inimigo)

                            # Avança para a próxima pergunta
                            current_question_index = (current_question_index + 1) % len(questions)
                            break

                    # Verifica se o botão de fugir foi clicado
                    flee_button_rect = pygame.Rect(button_x, button_y + (i + 1) * total_button_height, button_width, button_height)
                    if flee_button_rect.collidepoint(mouse_x, mouse_y):
                        flee_screen = True

        # Resetar a exibição da penalidade após algum tempo
        if mostrar_penalidade and pygame.time.get_ticks() - penalidade_start_time > 1000:  # 1 segundo para mostrar a penalidade
            mostrar_penalidade = False

if __name__ == "__main__":
    main()
    pygame.quit()
