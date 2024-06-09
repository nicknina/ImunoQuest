import pygame, sys
from button import Button
import mysql.connector
from pygame.locals import *
import random
from imagens import Sprites
from perguntas import questions

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
pygame.display.set_caption("ImunoQuest")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 0, 0)


# Definições de fonte
font = pygame.font.Font("C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\font.ttf", 25)
font_textos = pygame.font.Font("C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\font.ttf", 10)

BG = pygame.image.load("C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\Background.png")
background_image = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\background_quiz.png').convert()

def get_font(size): 
    return pygame.font.Font("C:\\Users\\nicol\\Downloads\\PIGameTest\\PIGameTest\\assets\\font.ttf", size)

def conectar_bd():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1234",
            database="pi1ano"
        )
        print("Conexão bem-sucedida ao banco de dados!")
        return conn
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None

def main_menu():
    
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250), 
                            text_input="ALUNOS", font=get_font(75), base_color="#b68f40", hovering_color="White")
        OPTIONS_BUTTON = Button(image=None, pos=(640, 400), 
                            text_input="PROFESSOR", font=get_font(75), base_color="#b68f40", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550), 
                            text_input="SAIR", font=get_font(75), base_color="#b68f40", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def options():
    def fazer_login(email, senha):
        # Credenciais armazenadas diretamente no código
        credenciais = {
            "1": "1",
        }

        if email in credenciais and credenciais[email] == senha:
            print("Login bem-sucedido!")
            return True
        else:
            print("Credenciais incorretas. Por favor, tente novamente.")
            return False

    email = ""
    senha = ""
    error_message = ""
    success_message = ""
    email_rect = pygame.Rect(350, 250, 800, 35)
    senha_rect = pygame.Rect(350, 450, 800, 35)
    active_rect = None
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('white')
    color = color_inactive

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        
        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        
        TEXT_EMAIL = get_font(25).render("Email: ", True, "White")
        SCREEN.blit(TEXT_EMAIL, (200, 260))
        TEXT_SENHA = get_font(25).render("Senha: ", True, "White")
        SCREEN.blit(TEXT_SENHA, (200, 460))

        error_text = get_font(20).render(error_message, True, pygame.Color("red"))
        error_rect = error_text.get_rect(center=(640, 550))
        SCREEN.blit(error_text, error_rect)

        success_text = get_font(20).render(success_message, True, pygame.Color("green"))
        success_rect = success_text.get_rect(center=(640, 570))
        SCREEN.blit(success_text, success_rect)

        pygame.draw.rect(SCREEN, color, email_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, color, senha_rect, 2, border_radius=5)

        email_surface = get_font(25).render(email, True, "White")
        SCREEN.blit(email_surface, (email_rect.x + 5, email_rect.y + 5))
        senha_surface = get_font(25).render('*' * len(senha), True, "White")
        SCREEN.blit(senha_surface, (senha_rect.x + 5, senha_rect.y + 5))

        LOGIN_BUTTON = Button(image=None, pos=(440, 660),
                              text_input="Login", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(880, 660),
                             text_input="Voltar", font=get_font(50), base_color="White", hovering_color="Green")

        LOGIN_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        LOGIN_BUTTON.update(SCREEN)
        BACK_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_rect = email_rect
                    color = color_active
                elif senha_rect.collidepoint(event.pos):
                    active_rect = senha_rect
                    color = color_active
                else:
                    active_rect = None
                    color = color_inactive

                if LOGIN_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    print("Valores a serem verificados no login:")
                    print("Email:", email)
                    print("Senha:", senha)
                    if fazer_login(email, senha):
                        success_message = "Login bem-sucedido! Você está conectado."
                        return tela_professor()
                    else:
                        error_message = "Credenciais incorretas. Por favor, tente novamente."

                elif BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

            elif event.type == pygame.KEYDOWN:
                if active_rect == email_rect:
                    if event.key == pygame.K_RETURN:
                        active_rect = senha_rect
                    elif event.key == pygame.K_BACKSPACE:
                        email = email[:-1]
                    else:
                        email += event.unicode
                elif active_rect == senha_rect:
                    if event.key == pygame.K_RETURN:
                        if fazer_login(email, senha):
                            success_message = "Login bem-sucedido! Você está conectado."
                            return tela_professor()
                    elif event.key == pygame.K_BACKSPACE:
                        senha = senha[:-1]
                    else:
                        senha += event.unicode

        pygame.display.update()

def play():
    while True:
        SCREEN.blit(BG, (0, 0))
        
        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        SCREEN.blit(MENU_TEXT, MENU_TEXT.get_rect(center=(640, 100)))

        LOGIN_BUTTON = Button(image=None, pos=(640, 250), text_input="LOGIN", font=get_font(75), base_color="White", hovering_color="Green")
        REGISTER_BUTTON = Button(image=None, pos=(640, 400), text_input="CADASTRO", font=get_font(75), base_color="White", hovering_color="Green")
        QUIT_BUTTON = Button(image=None, pos=(640, 550), text_input="SAIR", font=get_font(75), base_color="White", hovering_color="Green")

        LOGIN_BUTTON.changeColor(pygame.mouse.get_pos())
        LOGIN_BUTTON.update(SCREEN)
        REGISTER_BUTTON.changeColor(pygame.mouse.get_pos())
        REGISTER_BUTTON.update(SCREEN)
        QUIT_BUTTON.changeColor(pygame.mouse.get_pos())
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOGIN_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    tela_login()
                if REGISTER_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    tela_registro()
                if QUIT_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_menu()

        pygame.display.update()

def tela_professor():
    pygame.display.set_caption("ImunoQuest")

    alunos = []
    conn = conectar_bd()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id, nome, email, pontuacao_facil, pontuacao_medio, pontuacao_dificil FROM alunos")
            alunos = cursor.fetchall()
        except mysql.connector.Error as err:
            print("Erro ao buscar dados:", err)
        finally:
            cursor.close()
            conn.close()

    scroll_y = 0
    scroll_speed = 20

    while True:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(BG, (0, 0))

        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        SCREEN.blit(MENU_TEXT, MENU_TEXT.get_rect(center=(640, 100)))

        BACK_BUTTON = Button(image=None, pos=(640, 660),
                             text_input="Voltar", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)

        # Criação da área rolável
        scroll_area_height = 450
        scroll_area = pygame.Surface((SCREEN_WIDTH, scroll_area_height))
        scroll_area.blit(BG, (0, -250))  # Ajuste para usar a imagem de fundo

        y_offset = scroll_y
        for aluno in alunos:
            aluno_text = get_font(10).render(f"ID: {aluno[0]}, Nome: {aluno[1]}, Email: {aluno[2]}, Facil: {aluno[3]}, Medio: {aluno[4]}, Dificil: {aluno[5]}", True, "White")

            scroll_area.blit(aluno_text, (200, y_offset))
            y_offset += 40

        # Blit da área rolável na tela principal
        SCREEN.blit(scroll_area, (0, 150))

        # Desenho da barra de rolagem
        total_content_height = y_offset
        if total_content_height > scroll_area_height:
            scrollbar_height = int(scroll_area_height / total_content_height * scroll_area_height)
            scrollbar_y = int(-scroll_y / total_content_height * scroll_area_height)
            pygame.draw.rect(SCREEN, (200, 200, 200), (SCREEN_WIDTH - 20, 150 + scrollbar_y, 10, scrollbar_height))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    main_menu()
                elif event.button == 4:  # Scroll up
                    scroll_y = min(scroll_y + scroll_speed, 0)
                elif event.button == 5:  # Scroll down
                    scroll_y = max(scroll_y - scroll_speed, -(total_content_height - scroll_area_height))

        pygame.display.update()



def registrar_aluno(nome1, email1, senha1):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alunos WHERE email = %s", (email1,))
        if cursor.fetchone():
            print("Erro: O e-mail já está em uso.")
            return False

        cursor.execute("INSERT INTO alunos (nome, email, senha) VALUES (%s, %s, %s)", (nome1, email1, senha1))
        conn.commit()
        cursor.close()
        conn.close()

        print("Dados do aluno registrados com sucesso.")
        return True
    except Exception as e:
        print("Erro ao registrar aluno:", e)
        return False

def fazer_login(email1, senha1):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM alunos WHERE email = %s AND senha = %s", (email1, senha1))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False
    except Exception as e:
        print("Erro ao fazer login:", e)
        return False
def obter_emails_cadastrados():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        cursor.execute("SELECT email FROM alunos")
        emails = cursor.fetchall()

        cursor.close()
        conn.close()

        return [email[0] for email in emails]  # Retorna uma lista contendo apenas os emails
    except Exception as e:
        print("Erro ao obter os emails cadastrados:", e)
        return []
def gravar_pontuacao(dificuldade, email_aluno, score1):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        if dificuldade == 1:
            cursor.execute("UPDATE alunos SET facil = %s WHERE email = %s", (score1, email_aluno))
        elif dificuldade == 2:
            cursor.execute("UPDATE alunos SET medio = %s WHERE email = %s", (score1, email_aluno))
        elif dificuldade == 3:
            cursor.execute("UPDATE alunos SET dificil = %s WHERE email = %s", (score1, email_aluno))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print("Erro ao atualizar a pontuação no banco de dados:", e)
        
def tela_registro():
    email = ""
    nome = ""
    senha = ""
    active_rect = None
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('green')
    color = color_inactive

    email_rect = pygame.Rect(350, 250, 800, 35)
    nome_rect = pygame.Rect(350, 350, 800, 35)
    senha_rect = pygame.Rect(350, 450, 800, 35)

    while True:
        SCREEN.blit(BG, (0, 0))
        
        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        SCREEN.blit(MENU_TEXT, MENU_TEXT.get_rect(center=(640, 100)))

        # Renderizar textos
        SCREEN.blit(get_font(25).render("Email: ", True, "White"), (200, 260))
        SCREEN.blit(get_font(25).render("Nome: ", True, "White"), (200, 360))
        SCREEN.blit(get_font(25).render("Senha: ", True, "White"), (200, 460))

        # Desenhar e renderizar as caixas de texto
        pygame.draw.rect(SCREEN, color, email_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, color, nome_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, color, senha_rect, 2, border_radius=5)

        SCREEN.blit(get_font(25).render(email, True, "White"), (email_rect.x + 5, email_rect.y + 5))
        SCREEN.blit(get_font(25).render(nome, True, "White"), (nome_rect.x + 5, nome_rect.y + 5))
        SCREEN.blit(get_font(25).render('*' * len(senha), True, "White"), (senha_rect.x + 5, senha_rect.y + 5))

        SAVE_BUTTON = Button(image=None, pos=(440, 660), text_input="Salvar", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(880, 660), text_input="Voltar", font=get_font(50), base_color="White", hovering_color="Green")
        
        SAVE_BUTTON.changeColor(pygame.mouse.get_pos())
        SAVE_BUTTON.update(SCREEN)
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_rect = email_rect
                elif nome_rect.collidepoint(event.pos):
                    active_rect = nome_rect
                elif senha_rect.collidepoint(event.pos):
                    active_rect = senha_rect
                else:
                    active_rect = None

                color = color_active if active_rect else color_inactive

                if SAVE_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    if registrar_aluno(nome, email, senha):
                        return tela_login()
                elif BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return play()
            elif event.type == pygame.KEYDOWN:
                if active_rect:
                    if event.key == pygame.K_RETURN:
                        if registrar_aluno(nome, email, senha):
                            return tela_login()
                    elif event.key == pygame.K_BACKSPACE:
                        if active_rect == nome_rect:
                            nome = nome[:-1]
                        elif active_rect == email_rect:
                            email = email[:-1]
                        elif active_rect == senha_rect:
                            senha = senha[:-1]
                    else:
                        if active_rect == nome_rect:
                            nome += event.unicode
                        elif active_rect == email_rect:
                            email += event.unicode
                        elif active_rect == senha_rect:
                            senha += event.unicode

        pygame.display.update()

email_logado = ""

def tela_login():
    global email_logado
    email = ""
    senha = ""
    error_message = ""
    success_message = ""
    active_rect = None
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('green')
    color = color_inactive

    email_rect = pygame.Rect(350, 250, 800, 35)
    senha_rect = pygame.Rect(350, 450, 800, 35)

    while True:
        SCREEN.blit(BG, (0, 0))
        
        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        SCREEN.blit(MENU_TEXT, MENU_TEXT.get_rect(center=(640, 100)))

        SCREEN.blit(get_font(25).render("Email: ", True, "White"), (200, 260))
        SCREEN.blit(get_font(25).render("Senha: ", True, "White"), (200, 460))

        SCREEN.blit(get_font(20).render(error_message, True, pygame.Color("red")), (350, 500))
        SCREEN.blit(get_font(20).render(success_message, True, pygame.Color("green")), (350, 530))

        pygame.draw.rect(SCREEN, color, email_rect, 2, border_radius=5)
        pygame.draw.rect(SCREEN, color, senha_rect, 2, border_radius=5)

        SCREEN.blit(get_font(25).render(email, True, "White"), (email_rect.x + 5, email_rect.y + 5))
        SCREEN.blit(get_font(25).render('*' * len(senha), True, "White"), (senha_rect.x + 5, senha_rect.y + 5))

        LOGIN_BUTTON = Button(image=None, pos=(440, 660), text_input="Login", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(880, 660), text_input="Voltar", font=get_font(50), base_color="White", hovering_color="Green")

        LOGIN_BUTTON.changeColor(pygame.mouse.get_pos())
        LOGIN_BUTTON.update(SCREEN)
        BACK_BUTTON.changeColor(pygame.mouse.get_pos())
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if email_rect.collidepoint(event.pos):
                    active_rect = email_rect
                elif senha_rect.collidepoint(event.pos):
                    active_rect = senha_rect
                else:
                    active_rect = None

                color = color_active if active_rect else color_inactive

                if LOGIN_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    if fazer_login(email, senha):
                        email_logado = email  # Armazena o email do jogador logado
                        success_message = "Login bem-sucedido! Você está conectado."
                        return escolher_dificuldade()
                    else:
                        error_message = "Credenciais incorretas. Por favor, tente novamente."

                elif BACK_BUTTON.checkForInput(pygame.mouse.get_pos()):
                    return play()
            elif event.type == pygame.KEYDOWN:
                if active_rect == email_rect:
                    if event.key == pygame.K_RETURN:
                        if fazer_login(email, senha):
                            email_logado = email  # Armazena o email do jogador logado
                            success_message = "Login bem-sucedido! Você está conectado."
                            return escolher_dificuldade()
                        else:
                            error_message = "Credenciais incorretas. Por favor, tente novamente."
                    elif event.key == pygame.K_BACKSPACE:
                        email = email[:-1]
                    else:
                        email += event.unicode
                elif active_rect == senha_rect:
                    if event.key == pygame.K_RETURN:
                        if fazer_login(email, senha):
                            email_logado = email  # Armazena o email do jogador logado
                            success_message = "Login bem-sucedido! Você está conectado."
                            return escolher_dificuldade()
                        else:
                            error_message = "Credenciais incorretas. Por favor, tente novamente."
                    elif event.key == pygame.K_BACKSPACE:
                        senha = senha[:-1]
                    else:
                        senha += event.unicode

        pygame.display.update()




def escolher_dificuldade():
    
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(BG, (0, 0))
        
        MENU_TEXT = get_font(100).render("ImunoQuest", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        FACIL_BUTTON = Button(image=None, pos=(640, 280),
                                 text_input="FACIL", font=get_font(50), base_color="White", hovering_color="Green")
        MEDIO_BUTTON = Button(image=None, pos=(640, 400),
                              text_input="MEDIO", font=get_font(50), base_color="White", hovering_color="Green")
        DIFICIL_BUTTON = Button(image=None, pos=(640, 520),
                             text_input="DIFICIL", font=get_font(50), base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=None, pos=(640, 640),
                             text_input="VOLTAR", font=get_font(50), base_color="White", hovering_color="Green")
        

        FACIL_BUTTON.changeColor(PLAY_MOUSE_POS)
        MEDIO_BUTTON.changeColor(PLAY_MOUSE_POS)
        DIFICIL_BUTTON.changeColor(PLAY_MOUSE_POS)
        BACK_BUTTON.changeColor(PLAY_MOUSE_POS)

        FACIL_BUTTON.update(SCREEN)
        MEDIO_BUTTON.update(SCREEN)
        DIFICIL_BUTTON.update(SCREEN)
        BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FACIL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    dificuldade = 1
                    configurar_inimigo(dificuldade)  # Configura o inimigo com base na dificuldade
                    jogo(dificuldade)  # Inicia o jogo com a dificuldade selecionada
                elif MEDIO_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    dificuldade = 2
                    configurar_inimigo(dificuldade)
                    jogo(dificuldade)
                elif DIFICIL_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    dificuldade = 3
                    configurar_inimigo(dificuldade)
                    jogo(dificuldade)
                elif BACK_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    tela_login()

        pygame.display.update()

def gravar_pontuacao(email_aluno, dificuldade, pontuacao):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()

        # Dependendo da dificuldade, atualizar a pontuação no campo correspondente
        if dificuldade == 1:
            cursor.execute("UPDATE alunos SET pontuacao_facil = %s WHERE email = %s", (pontuacao, email_aluno))
        elif dificuldade == 2:
            cursor.execute("UPDATE alunos SET pontuacao_medio = %s WHERE email = %s", (pontuacao, email_aluno))
        elif dificuldade == 3:
            cursor.execute("UPDATE alunos SET pontuacao_dificil = %s WHERE email = %s", (pontuacao, email_aluno))

        conn.commit()
        cursor.close()
        conn.close()
        print("Pontuação salva com sucesso!")
    except Exception as e:
        print("Erro ao salvar a pontuação no banco de dados:", e)

def configurar_inimigo(dificuldade):
    global vida_inimigo
    imagem_inimigo = None

    if dificuldade == 1:
        imagem_inimigo = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest5\\PIGameTest5\\PIGameTest\\assets\\inimigo_facil.PNG').convert_alpha()
        vida_inimigo = 10
        tamanho = 0.4
    elif dificuldade == 2:
        imagem_inimigo = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest5\\PIGameTest5\\PIGameTest\\assets\\inimigo_medio.png').convert_alpha()
        vida_inimigo = 15
        tamanho = 0.3
    elif dificuldade == 3:
        imagem_inimigo = pygame.image.load('C:\\Users\\nicol\\Downloads\\PIGameTest5\\PIGameTest5\\PIGameTest\\assets\\inimigo_dificil.PNG').convert_alpha()
        vida_inimigo = 20
        tamanho = 0.4

    if imagem_inimigo is None:
        raise ValueError("A imagem do inimigo não foi carregada corretamente.")

    imagens = Sprites(imagem_inimigo)

    lista_animacao = []
    etapas_animacao = [6]  # Número de frames na animação
    contador_etapa = 0

    for animacao in etapas_animacao:
        lista_temporaria_img = []
        for _ in range(animacao):
            lista_temporaria_img.append(imagens.pegar_imagem(contador_etapa, 1000, 1000, tamanho, RED))
            contador_etapa += 1
        lista_animacao.append(lista_temporaria_img)

    ultima_atualizacao = pygame.time.get_ticks()
    cooldown_animacao = 150

    return lista_animacao, ultima_atualizacao, cooldown_animacao, vida_inimigo


def draw_intro_screen(lista_animacao, acao, dificuldade, ultima_atualizacao, cooldown_animacao, frame):
    SCREEN.blit(background_image, (0, 0))

    # Apresenta o inimigo junto com sua animação
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultima_atualizacao >= cooldown_animacao:
        frame += 1
        ultima_atualizacao = tempo_atual
        if frame >= len(lista_animacao[acao]):
            frame = 0

    # Exibir animação
    if dificuldade == 2:
        SCREEN.blit(lista_animacao[acao][frame], (800, 100))
    else:
        SCREEN.blit(lista_animacao[acao][frame], (750, -10))

    intro_text = font.render("Um vírus selvagem se aproxima", True, BLACK)
    intro_rect = intro_text.get_rect(bottomleft=(10, 670))
    SCREEN.blit(intro_text, intro_rect)

    # Desenha o botão de batalha
    button_width = 250
    button_height = 50
    button_x = SCREEN_WIDTH - 300
    button_y = SCREEN_HEIGHT - 100
    battle_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(SCREEN, GRAY, battle_button_rect)
    battle_text = font.render("Batalhar", True, BLACK)
    battle_text_rect = battle_text.get_rect(center=battle_button_rect.center)
    SCREEN.blit(battle_text, battle_text_rect)

    pygame.display.flip()

    return frame, ultima_atualizacao

def draw_question_screen(question_data, vida_inimigo, max_vida_inimigo, mostrar_dano_critico, mostrar_penalidade):
    SCREEN.blit(background_image, (0, 0))

    if max_vida_inimigo != 0:
        life_ratio = vida_inimigo / max_vida_inimigo
    else:
        life_ratio = 0

    # Desenha a pergunta
    question_text = font_textos.render(question_data["question"], True, RED)
    question_rect = question_text.get_rect(center=(600, SCREEN_HEIGHT - 650))
    SCREEN.blit(question_text, question_rect)

    # Desenha os botões de resposta
    button_width = 1000
    button_height = 60
    button_spacing = 25
    total_button_height = button_height + button_spacing
    button_x = SCREEN_WIDTH / 2 - button_width / 2
    button_y = 200

    for i, answer in enumerate(question_data["answers"]):
        button_rect = pygame.Rect(button_x, button_y + i * total_button_height, button_width, button_height)
        pygame.draw.rect(SCREEN, RED, button_rect)

        text_surface = font_textos.render(f"{answer['option'].upper()}: {answer['text']}", True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        SCREEN.blit(text_surface, text_rect)

    # Desenha o botão de fugir
    flee_button_rect = pygame.Rect(button_x, button_y + (len(question_data["answers"])) * total_button_height, button_width, button_height)
    pygame.draw.rect(SCREEN, RED, flee_button_rect)
    flee_text = font.render("Fugir", True, BLACK)
    flee_text_rect = flee_text.get_rect(center=flee_button_rect.center)
    SCREEN.blit(flee_text, flee_text_rect)

    # Desenha a barra de vida do inimigo
    life_bar_width = 400
    life_bar_height = 30
    life_bar_x = SCREEN_WIDTH // 2 - life_bar_width // 2
    life_bar_y = SCREEN_HEIGHT - 100
    current_life_width = life_bar_width * life_ratio

    pygame.draw.rect(SCREEN, BLACK, (life_bar_x, life_bar_y, life_bar_width, life_bar_height))
    pygame.draw.rect(SCREEN, RED, (life_bar_x, life_bar_y, current_life_width, life_bar_height))

    # Desenha a mensagem de dano crítico
    if mostrar_dano_critico:
        crit_text = font.render("Dano Crítico!", True, RED)
        crit_rect = crit_text.get_rect(center=(SCREEN_WIDTH // 2, life_bar_y + 60))
        SCREEN.blit(crit_text, crit_rect)

    # Desenha a mensagem de penalidade
    if mostrar_penalidade:
        penalty_text = font.render("+5 seg", True, RED)
        penalty_rect = penalty_text.get_rect(center=(life_bar_x + life_bar_width + 80, life_bar_y + life_bar_height // 2))
        SCREEN.blit(penalty_text, penalty_rect)

    pygame.display.flip()
# Função para desenhar a tela de fuga
def draw_flee_screen():
        global frame, ultima_atualizacao, cooldown_animacao, lista_animacao, acao

        SCREEN.blit(background_image, (0, 0))

        # Apresenta o inimigo junto com sua animação
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - ultima_atualizacao >= cooldown_animacao:
            frame += 1
            ultima_atualizacao = tempo_atual
            if frame >= len(lista_animacao[acao]):
                frame = 0

        # Exibir animação
        SCREEN.blit(lista_animacao[acao][frame], (750, -10))

        flee_text = font.render("Você fugiu!", True, BLACK)
        flee_rect = flee_text.get_rect(bottomleft=(10, SCREEN_HEIGHT - 50))
        SCREEN.blit(flee_text, flee_rect)

        pygame.display.flip()
def draw_victory_screen(score):
    SCREEN.blit(BG, (0, 0))
     
    victory_text = font.render("Você venceu!", True, WHITE)
    victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    SCREEN.blit(victory_text, victory_rect)

    # Convertendo o score de milissegundos para minutos, segundos e milissegundos
    minutes = score // 60000
    seconds = (score % 60000) // 1000
    milliseconds = score % 1000

    score_text = font.render(f"Pontuação: {minutes} min {seconds} seg", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    SCREEN.blit(score_text, score_rect)
    score1 = (f"{minutes}:{seconds}")
    

    pygame.display.flip()


def jogo(dificuldade):
    global vida_inimigo, intro_screen, flee_screen, victory_screen, imagens
    global email_logado
    
    random.shuffle(questions)
    
    intro_screen = True
    flee_screen = False
    victory_screen = False
    current_question_index = 0
    pontos = 0
    sequencia = 0
    start_time = pygame.time.get_ticks()
    score = 0
    mostrar_dano_critico = False
    mostrar_penalidade = False
    penalidade_start_time = 0
    
    lista_animacao, ultima_atualizacao, cooldown_animacao, vida_inimigo = configurar_inimigo(dificuldade)
    max_vida_inimigo = vida_inimigo
    acao = 0
    
    frame = 0
    
    while True:
        if intro_screen:
            frame, ultima_atualizacao = draw_intro_screen(lista_animacao, acao, dificuldade, ultima_atualizacao, cooldown_animacao, frame)
        elif flee_screen:
            escolher_dificuldade()
        elif victory_screen:
            draw_victory_screen(score)
            gravar_pontuacao(email_logado, dificuldade, score)
        else:
            draw_question_screen(questions[current_question_index], vida_inimigo, max_vida_inimigo, mostrar_dano_critico, mostrar_penalidade)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                    return escolher_dificuldade()
                elif victory_screen:
                    return draw_victory_screen(score)
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
                            else:
                                print("Resposta incorreta!")
                                sequencia = 0
                                mostrar_dano_critico = False
                                mostrar_penalidade = True
                                penalidade_start_time = pygame.time.get_ticks()
                                start_time -= 5000

                            current_question_index = (current_question_index + 1) % len(questions)

                            break

                    flee_button_rect = pygame.Rect(button_x, button_y + (len(questions[current_question_index]["answers"])) * total_button_height, button_width, button_height)
                    if flee_button_rect.collidepoint(mouse_x, mouse_y):
                        flee_screen = True

        if mostrar_penalidade and pygame.time.get_ticks() - penalidade_start_time > 1000:
            mostrar_penalidade = False

        pygame.display.update()

main_menu() 