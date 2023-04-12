import pygame 
from random import randint
import modules.class_sprites as m_cl



# шрифти і написи
pygame.font.init() 


font1 = pygame.font.Font(None, 80)
font2 = pygame.font.Font(None, 36)
 

# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
 
while run:
    # подія натискання на кнопку Закрити
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        #подія натискання на пробіл - спрайт стріляє
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE:
                m_cl.fire_sound.play()
                m_cl.ship.fire()
    
    # сама гра: дії спрайтів, перевірка правил гри, перемальовка
    if not finish:
        # оновлюємо фон
        m_cl.window.blit(m_cl.background, (0, 0))
 
        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(m_cl.score), 1, (255, 255, 255))
        m_cl.window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(m_cl.lost), 1, (255, 255, 255))
        m_cl.window.blit(text_lose, (10, 50))
 
        # рухи спрайтів
        m_cl.ship.update()
        m_cl.monsters.update()
        m_cl.bullets.update()

        # оновлюємо їх у новому місці при кожній ітерації циклу
        m_cl.ship.reset()
        m_cl.monsters.draw(m_cl.window)
        m_cl.bullets.draw(m_cl.window)

        # перевірка зіткнення кулі та монстрів (і монстр, і куля при зіткненні зникають)
        collides = pygame.sprite.groupcollide(m_cl.monsters,m_cl. bullets, True, True)
        for c in collides:
            # цей цикл повториться стільки разів, скільки монстрів збито
            m_cl.score = m_cl.score + 1
            monster = m_cl.Enemy(m_cl.img_enemy, randint(80, m_cl.win_width - 80), -40, 80, 50, randint(1, 5))
            m_cl.monsters.add(monster)

        # можливий програш: пропустили занадто багато або герой зіткнувся з ворогом
        if pygame.sprite.spritecollide(m_cl.ship, m_cl.monsters, False) or m_cl.lost >= m_cl.max_lost:
            finish = True # програли, ставимо тло і більше не керуємо спрайтами.
            m_cl.window.blit(m_cl.background, (0, 0))
            finish_game = font2.render("GAME OVER - YOU LOSE", True, (255,255,255))
            text = font2.render("Рахунок: " + str(m_cl.score), 1, (255, 255, 255))
            m_cl.window.blit(finish_game, (200, 200))
            m_cl.window.blit(text, (200, 300))
 
            text_lose = font2.render("Пропущено: " + str(m_cl.lost), 1, (255, 255, 255))
            m_cl.window.blit(text_lose, (200, 350))
            
            
        # перевірка виграшу: скільки очок набрали?
        if m_cl.score >= m_cl.goal:
            finish = True
            m_cl.window.blit(m_cl.background, (0, 0))
            finish_game = font2.render("GAME OVER  - YOU WON", True, (255,255,255))
            text = font2.render("Рахунок: " + str(m_cl.score), 1, (255, 255, 255))
            m_cl.window.blit(finish_game, (200, 200))
            m_cl.window.blit(text, (200, 300))
 
            text_lose = font2.render("Пропущено: " + str(m_cl.lost), 1, (255, 255, 255))
            m_cl.window.blit(text_lose, (200, 350))
            

        pygame.display.update()
    # цикл спрацьовує кожні 0.05 секунд
    pygame.time.delay(50)