import pygame
import json

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

def textarea_create(_id, world_x, world_y, lines):
    obj = {
        'id': _id,
        'world_x': world_x, 
        'world_y': world_y, 
        'world_w': 100, 
        'world_h': 100, 
        'screen_x': world_x, 
        'screen_y': world_y, 
        'screen_w': 100, 
        'screen_h': 100, 
        'lines': lines,
    }
    return obj

line_cursor_row_i = 0
line_cursor_col_i = 0
textareas = []

text = 'sample text'
lines = text.split()
textarea = textarea_create(0, 0, 0, lines)
textareas.append(textarea)

text = 'sample text 2'
lines = [text]
textarea = textarea_create(1, 500, 500, lines)
textareas.append(textarea)

textarea_i = 0

def save_json():
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(textareas, f, indent=4, ensure_ascii=False)

def load_json():
    global textareas
    with open('data.json', 'r', encoding='utf-8') as f:
        textareas = json.load(f)

load_json()

def main_input():
    global running
    global font_md
    global line_cursor_row_i
    global line_cursor_col_i
    global textareas
    global textarea_i
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                if line_cursor_row_i > 0:
                    line_cursor_row_i -= 1
                    if line_cursor_col_i > len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                        line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
                else:
                    line_cursor_col_i = 0
            elif event.key == pygame.K_DOWN:
                if line_cursor_row_i < len(textareas[textarea_i]['lines'])-1:
                    line_cursor_row_i += 1
                    if line_cursor_col_i > len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                        line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
                else:
                    line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
            elif event.key == pygame.K_LEFT:
                if line_cursor_col_i > 0:
                    line_cursor_col_i -= 1
                else:
                    if line_cursor_row_i > 0:
                        line_cursor_row_i -= 1
                        line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
            elif event.key == pygame.K_RIGHT:
                if line_cursor_col_i < len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                    line_cursor_col_i += 1
                else:
                    if line_cursor_row_i < len(textareas[textarea_i]['lines'])-1:
                        line_cursor_row_i += 1
                        line_cursor_col_i = 0
            elif event.key == pygame.K_BACKSPACE:
                if line_cursor_col_i > 0:
                    line_cur = textareas[textarea_i]['lines'][line_cursor_row_i]
                    line_chunk_1 = line_cur[:line_cursor_col_i-1]
                    line_chunk_2 = line_cur[line_cursor_col_i:]
                    line_cur = f'{line_chunk_1}{line_chunk_2}'
                    textareas[textarea_i]['lines'][line_cursor_row_i] = line_cur
                    line_cursor_col_i -= 1
                else:
                    if line_cursor_row_i > 0:
                        line_cur = textareas[textarea_i]['lines'][line_cursor_row_i]
                        del textareas[textarea_i]['lines'][line_cursor_row_i]
                        line_cursor_row_i -= 1
                        line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
                        textareas[textarea_i]['lines'][line_cursor_row_i] += line_cur
            elif event.key == pygame.K_DELETE:
                if line_cursor_col_i < len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                    line_cur = textareas[textarea_i]['lines'][line_cursor_row_i]
                    line_chunk_1 = line_cur[:line_cursor_col_i]
                    line_chunk_2 = line_cur[line_cursor_col_i+1:]
                    line_cur = f'{line_chunk_1}{line_chunk_2}'
                    textareas[textarea_i]['lines'][line_cursor_row_i] = line_cur
            elif event.key == pygame.K_RETURN and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                print('thidk')
            elif event.key == pygame.K_RETURN:
                line_cur = textareas[textarea_i]['lines'][line_cursor_row_i]
                line_chunk_1 = line_cur[:line_cursor_col_i]
                line_chunk_2 = line_cur[line_cursor_col_i:]
                textareas[textarea_i]['lines'][line_cursor_row_i] = line_chunk_1
                textareas[textarea_i]['lines'].insert(line_cursor_row_i + 1, line_chunk_2)
                line_cursor_col_i = 0
                line_cursor_row_i += 1
            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_json()
            elif event.key == pygame.K_l and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                load_json()
            # elif event.unicode.isprintable():
            elif pygame.K_a <= event.key <= pygame.K_z or event.key == pygame.K_SPACE:
                line_chunk_1 = textareas[textarea_i]['lines'][line_cursor_row_i][:line_cursor_col_i]
                line_chunk_2 = textareas[textarea_i]['lines'][line_cursor_row_i][line_cursor_col_i:]
                textareas[textarea_i]['lines'][line_cursor_row_i] = line_chunk_1 + event.unicode + line_chunk_2
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
    if pygame.mouse.get_pressed()[0]:
        if mouse['action_executing'] == 0:
            mouse['action_executing'] = 1
            for textarea_index, textarea in enumerate(textareas):
                if (mouse['pos_x'] > textarea['screen_x'] and 
                    mouse['pos_y'] > textarea['screen_y'] and 
                    mouse['pos_x'] < textarea['screen_x'] + textarea['screen_w'] and 
                    mouse['pos_y'] < textarea['screen_y'] + textarea['screen_h']
                ):
                    mouse['drag_mouse_start_x'] = mouse['pos_x']
                    mouse['drag_mouse_start_y'] = mouse['pos_y']
                    mouse['drag_node_id'] = textarea['id']
                    mouse['drag_node_start_x'] = textarea['world_x']
                    mouse['drag_node_start_y'] = textarea['world_y']
                    mouse['drag_executing'] = 1
                    textarea_i = textarea_index
                    break
    else: 
        mouse['action_executing'] = 0
        mouse['drag_executing'] = 0
        mouse['drag_node_id'] = None
    if pygame.mouse.get_pressed()[1]: 
        nav.pan_start(pygame)
    else: 
        nav.pan_stop()
    if pygame.mouse.get_pressed()[2]: 
        if mouse['right_click_action_executing'] == 0:
            mouse['right_click_action_executing'] = 1
            ### get last id
            id_next = textareas[-1]['id'] + 1
            textarea = textarea_create(id_next, mouse['screen_x'], mouse['screen_y'], ['edit me'])
            textareas.append(textarea)
    else: 
        mouse['right_click_action_executing'] = 0

def main_update():
    global offset_x
    global offset_y
    offset_x, offset_y = nav.zoom_pos_center(window_w, window_h)
    for textarea in textareas:
        textarea['screen_x'] = (textarea['world_x'] + camera['pan_x']) * camera['zoom'] + offset_x
        textarea['screen_y'] = (textarea['world_y'] + camera['pan_y']) * camera['zoom'] + offset_y
        textarea['screen_w'] = (textarea['world_w'] * camera['zoom'])
        textarea['screen_h'] = (textarea['world_h'] * camera['zoom'])
    mouse['screen_x'] = (mouse['pos_x'] + camera['pan_x']) * camera['zoom'] + offset_x
    mouse['screen_y'] = (mouse['pos_y'] + camera['pan_y']) * camera['zoom'] + offset_x
    if mouse['drag_executing'] == 1:
        if mouse['drag_node_id'] != None:
            for textarea in textareas:
                if textarea['id'] == mouse['drag_node_id']:
                    textarea['world_x'] = mouse['drag_node_start_x'] + (mouse['pos_x'] - mouse['drag_mouse_start_x']) // camera['zoom']
                    textarea['world_y'] = mouse['drag_node_start_y'] + (mouse['pos_y'] - mouse['drag_mouse_start_y']) // camera['zoom']

### convert world coordinates to screen coordinates
def world_to_screen(world_pos_x, world_pos_y):
    screen_pos_x = (world_pos_x + camera['pan_x']) * camera['zoom'] + offset_x
    screen_pos_y = (world_pos_y + camera['pan_y']) * camera['zoom'] + offset_y
    return screen_pos_x, screen_pos_y

def render_text():
    for textarea_index, textarea in enumerate(textareas):
        start_x, start_y = world_to_screen(textarea['world_x'], textarea['world_y'])
        max_w = 0
        line_i = 0
        ### get best line height 
        line_h = 0
        for line in textarea['lines']:
            _, _line_h = font_md.size(line)
            if line_h < _line_h: line_h = _line_h
        for line in textarea['lines']:
            line_w, _ = font_md.size(line)
            if max_w < line_w: max_w = line_w
            line_x = start_x
            line_y = start_y + line_h*line_i
            line_surface = font_md.render(line, True, '0xFFFFFF')
            window.blit(line_surface, (line_x, line_y))
            line_i += 1
        # pygame.draw.rect(window, "#ffffff", (start_x, start_y, max_w, line_h*line_i), 1 * camera['zoom'])
        if textarea_index == textarea_i:
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
