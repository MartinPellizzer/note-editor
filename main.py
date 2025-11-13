import pygame

from lib import nav
from lib.nav import camera
from lib.nav import mouse

offset_x = 0
offset_y = 0

pygame.init()
window_w = 1920
window_h = 1080
window = pygame.display.set_mode((window_w, window_h))
pygame.key.set_repeat(300, 50)
font_md_base = 32
font_md = pygame.font.Font(f'''fonts/CourierPrime-Regular.ttf''', font_md_base)

text = 'sample text'
lines = text.split()
line_cursor_row_i = 0
line_cursor_col_i = 0

def main_input():
    global running
    global font_md
    global text
    global line_cursor_row_i
    global line_cursor_col_i
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                if line_cursor_row_i > 0:
                    line_cursor_row_i -= 1
                    if line_cursor_col_i > len(lines[line_cursor_row_i]):
                        line_cursor_col_i = len(lines[line_cursor_row_i])
            elif event.key == pygame.K_DOWN:
                if line_cursor_row_i < len(lines)-1:
                    line_cursor_row_i += 1
                    if line_cursor_col_i > len(lines[line_cursor_row_i]):
                        line_cursor_col_i = len(lines[line_cursor_row_i])
            elif event.key == pygame.K_LEFT:
                if line_cursor_col_i > 0:
                    line_cursor_col_i -= 1
            elif event.key == pygame.K_RIGHT:
                if line_cursor_col_i < len(lines[line_cursor_row_i]):
                    line_cursor_col_i += 1
            elif event.key == pygame.K_BACKSPACE:
                if line_cursor_col_i > 0:
                    line_cur = lines[line_cursor_row_i]
                    line_chunk_1 = line_cur[:line_cursor_col_i-1]
                    line_chunk_2 = line_cur[line_cursor_col_i:]
                    line_cur = f'{line_chunk_1}{line_chunk_2}'
                    lines[line_cursor_row_i] = line_cur
                    line_cursor_col_i -= 1
            elif event.key == pygame.K_RETURN:
                line_cur = lines[line_cursor_row_i]
                line_chunk_1 = line_cur[:line_cursor_col_i]
                line_chunk_2 = line_cur[line_cursor_col_i:]
                lines[line_cursor_row_i] = line_chunk_1
                lines.insert(line_cursor_row_i + 1, line_chunk_2)
                line_cursor_col_i = 0
                line_cursor_row_i += 1
            elif event.unicode.isprintable():
                lines[line_cursor_row_i] += event.unicode
                line_cursor_col_i += 1

        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if camera['zoom'] < 16:
                    camera['zoom'] += 1
                    font_md = pygame.font.Font(None, font_md_base * camera['zoom'])
            elif event.y < 0:
                if camera['zoom'] > 1:
                    camera['zoom'] -= 1
                    font_md = pygame.font.Font(None, font_md_base * camera['zoom'])
    nav.mouse_pos_get(pygame)
    if pygame.mouse.get_pressed()[1]: 
        nav.pan_start(pygame)
    else: 
        nav.pan_stop()

def main_update():
    global offset_x
    global offset_y
    offset_x, offset_y = nav.zoom_pos_center(window_w, window_h)

### convert world coordinates to screen coordinates
def world_to_screen(world_pos_x, world_pos_y):
    screen_pos_x = (world_pos_x + camera['pan_x']) * camera['zoom'] + offset_x
    screen_pos_y = (world_pos_y + camera['pan_y']) * camera['zoom'] + offset_y
    return screen_pos_x, screen_pos_y

def render_text():
    start_x, start_y = world_to_screen(window_w//2, window_h//2)
    max_w = 0
    line_i = 0
    ### get best line height 
    line_h = 0
    for line in lines:
        _, _line_h = font_md.size(line)
        if line_h < _line_h: line_h = _line_h
    for line in lines:
        line_w, _ = font_md.size(line)
        if max_w < line_w: max_w = line_w
        line_x = start_x
        line_y = start_y + line_h*line_i
        line_surface = font_md.render(line, True, '0xFFFFFF')
        window.blit(line_surface, (line_x, line_y))
        line_i += 1
    # pygame.draw.rect(window, "#ffffff", (start_x, start_y, max_w, line_h*line_i), 1 * camera['zoom'])
    ### cursor
    char_w, char_h = font_md.size('c')
    x = start_x + char_w * line_cursor_col_i
    y = start_y + char_h * line_cursor_row_i
    w = 1 * camera['zoom']
    h = line_h
    pygame.draw.rect(window, "#ffffff", (x, y, w, h))

def main_render():
    window.fill('#111111')
    render_text()
    pygame.display.flip()

running = True
while running:
    main_input()
    main_update()
    main_render()

pygame.quit()
