import pygame
import sys
import time 
import random

pygame.init()

#  FULLSCREEN
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Sistema de Red")

clock = pygame.time.Clock()

#  Colores estilo hacker
BLACK = (0, 0, 0)
GREEN = (0, 255, 120)
DARK_GREEN = (0, 100, 50)
RED = (255, 60, 60)
GRAY = (40, 40, 40)

font = pygame.font.SysFont("consolas", 22)
big_font = pygame.font.SysFont("consolas", 42)

score = 0
errors = 0
level_index = 0

TIME_LIMIT = 180

#  caracteres tipo código
chars = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#  columnas de lluvia tipo Matrix
columns = [random.randint(0, HEIGHT) for _ in range(WIDTH // 20)]

def draw_matrix():
    for i, y in enumerate(columns):
        char = random.choice(chars)
        text = font.render(char, True, GREEN)

        x = i * 20
        screen.blit(text, (x, y))

        columns[i] += 15
        if columns[i] > HEIGHT:
            columns[i] = 0

#  líneas tipo terminal
def draw_terminal():
    lines = [
        ">>> Conectando a servidor...",
        ">>> Autenticando...",
        ">>> Decodificando señal...",
        ">>> Acceso parcial concedido...",
        ">>> Reconstruyendo paquetes..."
    ]

    for i, line in enumerate(lines):
        text = font.render(line, True, DARK_GREEN)
        screen.blit(text, (50, HEIGHT - 150 + i * 20))

#  barra de señal
def draw_signal_bar(time_left):
    pygame.draw.rect(screen, GRAY, (100, 60, WIDTH - 200, 20))
    width = int((time_left / TIME_LIMIT) * (WIDTH - 200))
    pygame.draw.rect(screen, GREEN, (100, 60, width, 20))

# HUD
def draw_hud():
    score_text = font.render(f"Conectividad: {score}", True, GREEN)
    screen.blit(score_text, (100, 30))

    error_text = font.render(f"Errores: {errors}/2", True, RED)
    screen.blit(error_text, (WIDTH - 250, 30))

#  botón estilo terminal
class Button:
    def __init__(self, text, x, y):
        self.text = text
        self.rect = pygame.Rect(x, y, 500, 50)

    def draw(self):
        mouse = pygame.mouse.get_pos()
        color = GREEN if self.rect.collidepoint(mouse) else DARK_GREEN

        pygame.draw.rect(screen, color, self.rect, 1)

        txt = font.render(self.text, True, color)
        screen.blit(txt, (self.rect.x + 15, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

#  niveles
levels = [
    {
        "question": "Decodifica binario: 1000011",
        "options": ["67", "65", "70"],
        "answer": "67"
    },
    {
        "question": "Decodifica binario: 10110110",
        "options": ["180", "182", "190"],
        "answer": "182"
    },
    {
        "question": "ASCII:01010010 01000101 01000100",
        "options": ["RED", "NET", "SYS"],
        "answer": "RED"
    },
    {
        "question": "Decodifica binario: 11111100100",
        "options": ["2020", "4050", "3008"],
        "answer": "2020"
    },
    {
        "question": "1001001 1001110 1010100 1000101 1010001 1001110 1000101 1010100",
        "options": ["Conexión", "Instalacion", "Internet"],
        "answer": "Internet"
    }   
    
]

#  efecto glitch
def glitch_text(text, color):
    for _ in range(5):
        screen.fill(BLACK)
        draw_matrix()

        glitch = random.randint(-10, 10)

        msg = big_font.render(text, True, color)
        screen.blit(msg, (WIDTH//2 - 200 + glitch, HEIGHT//2))

        pygame.display.update()
        pygame.time.delay(100)

#  pantalla final
def end_screen(text, win=True):
    screen.fill(BLACK)
    draw_matrix()

    color = GREEN if win else RED
    msg = big_font.render(text, True, color)
    screen.blit(msg, (WIDTH//2 - 250, HEIGHT//2))

    pygame.display.update()
    pygame.time.delay(4000)

    pygame.quit()
    sys.exit()

# ▶ inicio
def start_screen():
    while True:
        screen.fill(BLACK)
        draw_matrix()

        title = big_font.render(">>> SISTEMA DE RED <<<", True, GREEN)
        start = font.render("ENTER para iniciar | ESC para salir", True, GREEN)

        screen.blit(title, (WIDTH//2 - 250, HEIGHT//3))
        screen.blit(start, (WIDTH//2 - 200, HEIGHT//2))

        draw_terminal()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

#  juego
def game():
    global score, errors, level_index

    start_screen()

    while level_index < len(levels):
        level = levels[level_index]

        buttons = [
            Button(level["options"][0], WIDTH//2 - 250, 300),
            Button(level["options"][1], WIDTH//2 - 250, 360),
            Button(level["options"][2], WIDTH//2 - 250, 420)
        ]

        start_time = time.time()
        answered = False

        while not answered:
            screen.fill(BLACK)
            draw_matrix()
            draw_terminal()

            time_left = TIME_LIMIT - (time.time() - start_time)

            if time_left <= 0:
                score -= 5
                errors += 1
                glitch_text("SEÑAL PERDIDA", RED)
                break

            question = font.render(level["question"], True, GREEN)
            screen.blit(question, (WIDTH//2 - 250, 200))

            draw_signal_bar(time_left)
            draw_hud()

            for btn in buttons:
                btn.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    for btn in buttons:
                        if btn.is_clicked(pos):
                            if btn.text == level["answer"]:
                                score += 10
                                glitch_text("ACCESO CORRECTO", GREEN)
                            else:
                                score -= 5
                                errors += 1
                                glitch_text("ERROR", RED)

                            answered = True

            pygame.display.update()
            clock.tick(60)

        level_index += 1

        if errors >= 2:
            end_screen(">>> SE PERDIO LA SEÑAL <<<", False)

    end_screen(">>> TRANSMISION RESTAURADA <<<", True)

game()