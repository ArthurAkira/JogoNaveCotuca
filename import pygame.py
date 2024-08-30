import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definição de cores 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
bulletcor = (100, 100, 255)

# Configurações da tela
width, height = 800, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Arthur Akira & Leo')

# Carregar imagens
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (50, 50))  # Ajuste o tamanho conforme necessário

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (50, 50))  # Ajuste o tamanho conforme necessário


# Variáveis do jogador
player_size = 20
player_x = width // 2 - player_size // 2
player_y = height - 2 * player_size
player_speed = 3
normal_player_speed = 3
boosted_player_speed = 6
player_shoot_delay = 150
last_player_shoot_time = 0
player_lives = 3
player_invulnerable_time = 3000
player_invulnerable_timer = 0
last_collision_time = 0

# Variáveis do inimigo
enemy_size = 50
enemy_x = random.randint(0, width - enemy_size)
enemy_y = random.randint(0, height // 2 - enemy_size)
enemy_speed = 1
enemy_shoot_delay_min = 1
enemy_shoot_delay_max = 30
time_since_last_enemy_shot = 0
last_reaction_time = pygame.time.get_ticks()
enemy_reaction_delay = 1200
enemy_next_shot_delay = random.randint(enemy_shoot_delay_min, enemy_shoot_delay_max)
enemy_random_movement_delay = 3000 
last_enemy_random_movement = pygame.time.get_ticks()

# Variáveis do projetil
bullet_radius = 5
bullet_size = 10
bullet_speed = 15
bullet_list = []
normal_bullet_offset = player_size // 4 - bullet_size // 2
boosted_bullet_offset = player_size // 6 - bullet_size // 2
is_boosted = False

class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 5
    def move(self):
        self.y += self.speed
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (self.x, self.y), self.radius)
enemy_bullet_list = []

show_menu = True

def display_menu():
    font = pygame.font.Font(None, 36)
    text = font.render("Pressione espaço para começar", True, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

def restart_menu():
    global enemy_speed 
    global player_lives
    player_lives = 3
    enemy_speed = 1
    font = pygame.font.Font(None, 36)
    text = font.render("Você foi atingido! Pressione R para reiniciar.", True, WHITE)
    text_rect = text.get_rect(center=(width // 2, height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                waiting = False
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reinicia variáveis do jogador e inimigo
                    global player_x, player_y, enemy_x, enemy_y
                    player_x = width // 2 - player_size // 2
                    player_y = height - 2 * player_size
                    enemy_x = random.randint(0, width - enemy_size)
                    enemy_y = random.randint(0, height - enemy_size)
                    enemy_bullet_list.clear()
                    waiting = False


clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)
    current_time = pygame.time.get_ticks()
    time_since_last_enemy_shot += clock.get_rawtime()
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and show_menu:
                show_menu = False

    if show_menu:
        display_menu()
    else:
        if player_lives == 0:
            restart_menu()
        if time_since_last_enemy_shot >= enemy_next_shot_delay:
            enemy_bullet_list.append(EnemyBullet(enemy_x + enemy_size // 2, enemy_y + enemy_size))
            time_since_last_enemy_shot = 0
            enemy_next_shot_delay = random.randint(enemy_shoot_delay_min, enemy_shoot_delay_max)
        for bullet in enemy_bullet_list:
            bullet.move()
            bullet.draw(screen)
            if (bullet.y + bullet.radius > player_y and bullet.y - bullet.radius < player_y + player_size) \
                    and (bullet.x + bullet.radius > player_x and bullet.x - bullet.radius < player_x + player_size):
                if current_time - last_collision_time > player_invulnerable_time:
                    player_lives -= 1
                    last_collision_time = current_time
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            is_boosted = True
        else:
            is_boosted = False
        
        # Movimento do jogador
        if is_boosted:
            player_speed = boosted_player_speed
            bullet_offset = boosted_bullet_offset
        else:
            player_speed = normal_player_speed
            bullet_offset = normal_bullet_offset
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < width - player_size:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < height - player_size:
            player_y += player_speed
            
        if True:
            if current_time - last_player_shoot_time >= player_shoot_delay:
                bullet_list.append([player_x + 10 - player_size // 4 - bullet_size // 2, player_y])
                bullet_list.append([player_x + 10 * player_size // 4 - bullet_size // 2, player_y])
                last_player_shoot_time = current_time
                
        if keys[pygame.K_SPACE]:
            if current_time - last_player_shoot_time >= player_shoot_delay:
                if is_boosted:
                    bullet_list.append([player_x + player_size // 2 - bullet_size // 2, player_y])
                else:
                    bullet_list.append([player_x - bullet_offset, player_y])
                    bullet_list.append([player_x + player_size - bullet_offset, player_y])
                last_player_shoot_time = current_time

        if current_time - last_reaction_time > enemy_reaction_delay:
            target_enemy_y = player_y
            if enemy_y < target_enemy_y:
                enemy_vertical_movement = min(enemy_speed, target_enemy_y - enemy_y)
            elif enemy_y > target_enemy_y:
                enemy_vertical_movement = max(-enemy_speed, target_enemy_y - enemy_y)
            else:
                enemy_vertical_movement = 0
            target_enemy_x = player_x
            if enemy_x < target_enemy_x:
                enemy_x += min(enemy_speed, target_enemy_x - enemy_x)
            elif enemy_x > target_enemy_x:
                enemy_x -= min(enemy_speed, enemy_x - target_enemy_x)
            enemy_y += enemy_vertical_movement 
            
        # Verificação de colisão entre jogador e inimigo
        if (player_x < enemy_x + enemy_size and player_x + player_size > enemy_x and
            player_y < enemy_y + enemy_size and player_y + player_size > enemy_y):
            if current_time - last_collision_time > player_invulnerable_time:
                player_lives -= 1
                last_collision_time = current_time
            player_x = width // 2 - player_size // 2
            player_y = height - 2 * player_size
            enemy_x = random.randint(0, width - enemy_size)
            enemy_y = random.randint(0, height // 2 - enemy_size)
            enemy_bullet_list.clear()
            enemy_speed -= 3
            enemy_next_shot_delay -= 5
            if enemy_next_shot_delay < 1:
                enemy_next_shot_delay = 1

        # Verificar colisão entre projéteis e inimigo
        for bullet in bullet_list:
            if (bullet[1] < enemy_y + enemy_size) and (bullet[1] > enemy_y):
                if (bullet[0] > enemy_x and bullet[0] < enemy_x + enemy_size) or \
                (bullet[0] + bullet_size > enemy_x and bullet[0] + bullet_size < enemy_x + enemy_size):
                    bullet_list.remove(bullet)
                    enemy_x = random.randint(0, width - enemy_size)
                    enemy_y = 50
                    enemy_speed += 0.3
                    enemy_next_shot_delay -= 5
                    if enemy_next_shot_delay < 1:
                        enemy_next_shot_delay = 1
                    if enemy_speed > 20:
                        enemy_speed = 20
                    break
                
        # Contador para a invulnerabilidade do jogador
        if current_time - last_collision_time < player_invulnerable_time:
            player_invulnerable_timer = player_invulnerable_time - (current_time - last_collision_time)
        else:
            player_invulnerable_timer = 0 

        for bullet in bullet_list:
            pygame.draw.circle(screen, bulletcor, (bullet[0], bullet[1]), bullet_radius)
            bullet[1] -= bullet_speed
            if bullet[1] <= 0:
                bullet_list.remove(bullet)

        if player_invulnerable_timer > 1:
            font = pygame.font.Font(None, 24)
            invulnerable_text = font.render(f'Invulnerável: {player_invulnerable_timer // 1000} s', True, WHITE)
            text_rect = invulnerable_text.get_rect(center=(player_x + player_size // 2, player_y - 20))
            screen.blit(invulnerable_text, text_rect)

        player_hitbox_x = player_x + player_size // 2
        player_hitbox_y = player_y + player_size // 2
        player_hitbox_radius = player_size // 4
        
        enemy_center_x = enemy_x + enemy_size // 2
        enemy_center_y = enemy_y + enemy_size // 2
        enemy_radius = enemy_size // 2
        
        if (player_hitbox_x - enemy_center_x) ** 2 + (player_hitbox_y - enemy_center_y) ** 2 <= (player_hitbox_radius + enemy_radius) ** 2:
            if current_time - last_collision_time > player_invulnerable_time:
                player_lives -= 1
                last_collision_time = current_time
                player_x = width // 2 - player_size // 2
                player_y = height - 2 * player_size
                enemy_x = random.randint(0, width - enemy_size)
                enemy_y = random.randint(0, height // 2 - enemy_size)
                enemy_bullet_list.clear()
                enemy_speed -= 3
                enemy_next_shot_delay -= 5
                if enemy_next_shot_delay < 1:
                    enemy_next_shot_delay = 1
            
        screen.blit(player_image, (player_x, player_y))
        screen.blit(enemy_image, (enemy_x, enemy_y))
        pygame.draw.circle(screen,BLACK, (player_hitbox_x, player_hitbox_y), player_hitbox_radius, 2) 
        
        lives_text = font.render(f'Vidas: {player_lives}', True, WHITE)
        screen.blit(lives_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
