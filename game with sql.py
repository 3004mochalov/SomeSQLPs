import pygame
import random
import psycopg2
import tkinter as tk
from tkinter import messagebox, simpledialog

# Параметры игры
WIDTH, HEIGHT = 600, 400
SNAKE_SIZE = 10
SNAKE_SPEED = 15

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")


def connect_db():
    return psycopg2.connect(
        dbname="scores",
        user="postgres",
        password="4134",
        host="localhost",
        port="1337"
    )


# Функция для записи очков в базу данных
def save_score(username, score):
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (username, score))
        conn.commit()
    except Exception as e:
        print("Ошибка при записи в базу данных:", str(e))
    finally:
        cur.close()
        conn.close()


# Функция для получения всех результатов из базы данных
def get_all_scores():
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT username, score FROM scores ORDER BY score DESC")
        scores = cur.fetchall()
        return scores
    except Exception as e:
        print("Ошибка при получении данных:", str(e))
        return []
    finally:
        cur.close()
        conn.close()


# Функция для отображения результатов в интерфейсе Tkinter
def show_scores(scores):
    results = "Топ Результаты:\n"
    for username, score in scores:
        results += f"{username}: {score}\n"
    messagebox.showinfo("Результаты", results)


# Основная функция игры
def main():
    # Получаем имя игрока через диалоговое окно
    username = simpledialog.askstring("Имя игрока", "Введите ваше имя:")
    if not username:
        username = "Игрок"  # использовать "Игрок", если имя не введено
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = (SNAKE_SIZE, 0)
    food_position = (random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                     random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, SNAKE_SIZE):
                    direction = (0, -SNAKE_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -SNAKE_SIZE):
                    direction = (0, SNAKE_SIZE)
                elif event.key == pygame.K_LEFT and direction != (SNAKE_SIZE, 0):
                    direction = (-SNAKE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-SNAKE_SIZE, 0):
                    direction = (SNAKE_SIZE, 0)

        # Перемещение змейки
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, new_head)

        # Проверка на еду
        if snake[0] == food_position:
            score += 1
            food_position = (random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE,
                             random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE)
        else:
            snake.pop()

        # Проверка на столкновение со стенами или самой собой
        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
                snake[0][1] < 0 or snake[0][1] >= HEIGHT or
                snake[0] in snake[1:]):
            save_score(username, score)
            scores = get_all_scores()
            show_scores(scores)  # Показываем результаты после завершения
            print("Game Over! Ваш счет:", score)
            pygame.quit()
            return

        window.fill(WHITE)

        # Рисование змейки
        for segment in snake:
            pygame.draw.rect(window, GREEN, (*segment, SNAKE_SIZE, SNAKE_SIZE))

        # Рисование еды
        pygame.draw.rect(window, RED, (*food_position, SNAKE_SIZE, SNAKE_SIZE))

        # Рисование счета на экране
        font = pygame.font.SysFont(None, 35)
        text = font.render(f"Счет: {score}", True, (0, 0, 0))
        window.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(SNAKE_SPEED)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Скрываем главное окно Tkinter
    main()