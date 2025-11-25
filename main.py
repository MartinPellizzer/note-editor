import pygame
import time

import os
import json

from lib import nav
from lib.nav import camera
from lib.nav import mouse

offset_x = 0
offset_y = 0

core = {
    'editor_mode': 0,
    'last_k_time': 0,
    'kj_timeout': 0.25,
}

pygame.init()
window_w = 1280
window_w = 1920
window_h = 720
window_h = 1080
window = pygame.display.set_mode(
    (window_w, window_h),
    pygame.RESIZABLE,
)
clock = pygame.time.Clock()
pygame.key.set_repeat(300, 50)
font_filepath = f'''fonts/CourierPrime-Regular.ttf'''
camera['zoom'] = 2
font_md_base = 8
font_md_world = pygame.font.Font(font_filepath, font_md_base)
font_md = pygame.font.Font(font_filepath, font_md_base * camera['zoom'])
font_sm_base = 16
font_sm = pygame.font.Font(font_filepath, font_sm_base * camera['zoom'])

def text_world_coords_get():
    line_char_num_max = 0
    max_h = 0
    for line in lines:
        line_char_num = len(line)
        if line_char_num_max < line_char_num: line_char_num_max = line_char_num
    char_w, char_h = font_md_world.size('c')
    max_h = char_h * len(lines)
    max_w = char_w * line_char_num_max
    return max_w, max_h

def textarea_create(_id, world_x, world_y, lines):
    obj = {
        'id': _id,
        'world_x': world_x, 
        'world_y': world_y, 
        'world_w': 0, 
        'world_h': 0, 
        'screen_x': world_x, 
        'screen_y': world_y, 
        'screen_w': 0, 
        'screen_h': 0, 
        'lines': lines,
    }
    # obj['world_w'], obj['world_h'] = text_world_coords_get()
    return obj

line_cursor_row_i = 0
line_cursor_col_i = 0
textareas = []

'''
text = 'sample text'
lines = text.split()
textarea = textarea_create(0, 0, 0, lines)
textareas.append(textarea)

text = 'sample text 2'
lines = [text]
textarea = textarea_create(1, 500, 500, lines)
textareas.append(textarea)
'''

textarea_i = 0

cell_size = 64

data_filepath = 'data/9.json'

def save_json():
    with open(data_filepath, 'w', encoding='utf-8') as f:
        json.dump(textareas, f, indent=4, ensure_ascii=False)

def load_json():
    global textareas
    if not os.path.exists(data_filepath):
        with open(data_filepath, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)
    with open(data_filepath, 'r', encoding='utf-8') as f:
        textareas = json.load(f)

load_json()

keyboard = {
    'control_pressed': False,
}

def input_keyboard_mode_normal(event):
    global running
    global line_cursor_row_i
    global line_cursor_col_i
    global textareas
    global textarea_i
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
            pass
        elif event.key == pygame.K_i:
            core['editor_mode'] = 1
        elif event.key == pygame.K_k:
            if line_cursor_row_i > 0:
                line_cursor_row_i -= 1
                if line_cursor_col_i > len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                    line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
            else:
                line_cursor_col_i = 0
        elif event.key == pygame.K_j:
            if line_cursor_row_i < len(textareas[textarea_i]['lines'])-1:
                line_cursor_row_i += 1
                if line_cursor_col_i > len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                    line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
            else:
                line_cursor_col_i = len(textareas[textarea_i]['lines'][line_cursor_row_i])
        elif event.key == pygame.K_h:
            if line_cursor_col_i > 0:
                line_cursor_col_i -= 1
        elif event.key == pygame.K_l:
            if line_cursor_col_i < len(textareas[textarea_i]['lines'][line_cursor_row_i]):
                line_cursor_col_i += 1
        elif event.key == pygame.K_o:
            line_cur = textareas[textarea_i]['lines'][line_cursor_row_i]
            line_chunk_1 = line_cur[:]
            line_chunk_2 = ''
            textareas[textarea_i]['lines'][line_cursor_row_i] = line_chunk_1
            textareas[textarea_i]['lines'].insert(line_cursor_row_i + 1, line_chunk_2)
            line_cursor_col_i = 0
            line_cursor_row_i += 1
            core['editor_mode'] = 1

def input_keyboard_mode_insert(event):
    pass

def main_input():
    global running
    global font_sm
    global font_md
    global line_cursor_row_i
    global line_cursor_col_i
    global textareas
    global textarea_i
    global data_filepath
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if core['editor_mode'] == 0:
            input_keyboard_mode_normal(event)
        elif core['editor_mode'] == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    core['last_k_time'] = time.time()
                elif event.key == pygame.K_j:
                    if time.time() - core['last_k_time'] <= core['kj_timeout']:
                        core['editor_mode'] = 0
                        line_cur = textareas[textarea_i]['lines'][line_cursor_row_i]
                        line_chunk_1 = line_cur[:line_cursor_col_i-1]
                        line_chunk_2 = line_cur[line_cursor_col_i:]
                        line_cur = f'{line_chunk_1}{line_chunk_2}'
                        textareas[textarea_i]['lines'][line_cursor_row_i] = line_cur
                        line_cursor_col_i -= 1
                        continue
                if event.key == pygame.K_ESCAPE:
                    running = False
                    pass
                elif event.key == pygame.K_PERIOD and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    nav.pan_reset()
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
                elif event.key == pygame.K_0 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/0.json'
                    load_json()
                elif event.key == pygame.K_1 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/1.json'
                    load_json()
                elif event.key == pygame.K_2 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/2.json'
                    load_json()
                elif event.key == pygame.K_3 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/3.json'
                    load_json()
                elif event.key == pygame.K_4 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/4.json'
                    load_json()
                elif event.key == pygame.K_5 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/5.json'
                    load_json()
                elif event.key == pygame.K_6 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/6.json'
                    load_json()
                elif event.key == pygame.K_7 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/7.json'
                    load_json()
                elif event.key == pygame.K_8 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/8.json'
                    load_json()
                elif event.key == pygame.K_9 and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    data_filepath = 'data/9.json'
                    load_json()
                elif event.key == pygame.K_x and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    del textareas[textarea_i]
                    textarea_i = -1
                # elif event.unicode.isprintable():
                elif (
                        pygame.K_a <= event.key <= pygame.K_z or 
                        pygame.K_0 <= event.key <= pygame.K_9 or 
                        (event.key == pygame.K_9 and (pygame.key.get_mods() & pygame.KMOD_SHIFT)) or 
                        (event.key == pygame.K_0 and (pygame.key.get_mods() & pygame.KMOD_SHIFT)) or 
                        event.key == pygame.K_SPACE or event.key == pygame.K_MINUS or 
                        event.key == pygame.K_COMMA or event.key == pygame.K_PERIOD  
                ):
                    line_chunk_1 = textareas[textarea_i]['lines'][line_cursor_row_i][:line_cursor_col_i]
                    line_chunk_2 = textareas[textarea_i]['lines'][line_cursor_row_i][line_cursor_col_i:]
                    textareas[textarea_i]['lines'][line_cursor_row_i] = line_chunk_1 + event.unicode + line_chunk_2
                    line_cursor_col_i += 1
                    # textareas[textarea_i]['world_w'], textareas[textarea_i]['world_h'] = text_world_coords_get()
                elif event.key == pygame.K_LCTRL:
                    keyboard['control_pressed'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL:
                keyboard['control_pressed'] = False
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                if camera['zoom'] < 16:
                    camera['zoom'] += 1
                    font_md = pygame.font.Font(font_filepath, font_md_base * camera['zoom'])
                    font_sm = pygame.font.Font(font_filepath, font_sm_base * camera['zoom'])
            elif event.y < 0:
                if camera['zoom'] > 1:
                    camera['zoom'] -= 1
                    font_md = pygame.font.Font(font_filepath, font_md_base * camera['zoom'])
                    font_sm = pygame.font.Font(font_filepath, font_sm_base * camera['zoom'])

    nav.mouse_pos_get(pygame, window_w, window_h)
    if pygame.mouse.get_pressed()[0]:
        if mouse['action_executing'] == 0:
            mouse['action_executing'] = 1
            for textarea_index, textarea in enumerate(textareas):
                if (mouse['world_x'] > textarea['screen_x'] and 
                    mouse['world_y'] > textarea['screen_y'] and 
                    mouse['world_x'] < textarea['screen_x'] + textarea['screen_w'] and 
                    mouse['world_y'] < textarea['screen_y'] + textarea['screen_h']
                ):
                    mouse['drag_mouse_start_x'] = mouse['world_x']
                    mouse['drag_mouse_start_y'] = mouse['world_y']
                    mouse['drag_node_id'] = textarea['id']
                    mouse['drag_node_start_x'] = textarea['world_x']
                    mouse['drag_node_start_y'] = textarea['world_y']
                    mouse['drag_executing'] = 1
                    if textarea_i != textarea_index:
                        line_cursor_col_i = 0
                        line_cursor_row_i = 0
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
            if textareas != []:
                id_next = textareas[-1]['id'] + 1
            else:
                id_next = 0
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
        # textarea['screen_w'] = (textarea['world_w'] * camera['zoom'])
        # textarea['screen_h'] = (textarea['world_h'] * camera['zoom'])
        line_max_len = 0
        for line in textarea['lines']:
            if line_max_len < len(line): line_max_len = len(line)
        char_w, char_h = font_md.size('c')
        line_w = char_w * line_max_len
        line_h = char_h * len(textarea['lines'])
        textarea['screen_w'] = line_w
        textarea['screen_h'] = line_h
    mouse['screen_x'] = (mouse['world_x'] - offset_x) / camera['zoom'] - camera['pan_x']
    mouse['screen_y'] = (mouse['world_y'] - offset_y) / camera['zoom'] - camera['pan_y']
    ### drag
    if mouse['drag_executing'] == 1:
        if mouse['drag_node_id'] != None:
            for textarea in textareas:
                if textarea['id'] == mouse['drag_node_id']:
                    textarea['world_x'] = mouse['drag_node_start_x'] + (mouse['world_x'] - mouse['drag_mouse_start_x']) // camera['zoom']
                    textarea['world_y'] = mouse['drag_node_start_y'] + (mouse['world_y'] - mouse['drag_mouse_start_y']) // camera['zoom']
                    if keyboard['control_pressed']:
                        textarea['world_x'] = round(textarea['world_x'] / cell_size) * cell_size
                        textarea['world_y'] = round(textarea['world_y'] / cell_size) * cell_size

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
        # debug
        if 0:
            text_surface = font_md.render(f'''{textarea['world_x']} - {textarea['world_y']}''', True, '0xFF00FF00')
            window.blit(text_surface, (textarea['screen_x'], textarea['screen_y'] - line_h*2))
            text_surface = font_md.render(f'''{textarea['screen_x']} - {textarea['screen_y']}''', True, '0xFF00FF00')
            window.blit(text_surface, (textarea['screen_x'], textarea['screen_y'] - line_h))
            pygame.draw.rect(window, "#ffffff", (textarea['screen_x'], textarea['screen_y'], textarea['screen_w'], textarea['screen_h']), 1)
        if 0:
            pygame.draw.rect(window, "#ffffff", (textarea['screen_x'], textarea['screen_y'], textarea['screen_w'], textarea['screen_h']), 1)
        if 0:
            text_surface = font_sm.render(f'w:{textarea["screen_w"]}', True, '0xff00ff00')
            window.blit(text_surface, (textarea['screen_x'], textarea['screen_y'] - line_h*2))
            text_surface = font_sm.render(f'h:{textarea["screen_h"]}', True, '0xff00ff00')
            window.blit(text_surface, (textarea['screen_x'], textarea['screen_y'] - line_h))

def render_grid():
    color = '#202020'
    for col_i in range(-100, 100):
        x1 = ((cell_size * col_i) + camera['pan_x']) * camera['zoom'] + offset_x
        y1 = 0
        x2 = ((cell_size * col_i) + camera['pan_x']) * camera['zoom'] + offset_x
        y2 = window_h * 4
        pygame.draw.line(window, color, (x1, y1), (x2, y2), 1)
    for row_i in range(-100, 100):
        x1 = 0
        y1 = ((cell_size * row_i) + camera['pan_y']) * camera['zoom'] + offset_y
        x2 = window_w * 4
        y2 = ((cell_size * row_i) + camera['pan_y']) * camera['zoom'] + offset_y
        pygame.draw.line(window, color, (x1, y1), (x2, y2), 1)
    if 0:
        for col_i in range(-100, 100):
            for row_i in range(-100, 100):
                world_x = cell_size * col_i
                world_y = cell_size * row_i
                x = (world_x + camera['pan_x']) * camera['zoom'] + offset_x
                y = (world_y + camera['pan_y']) * camera['zoom'] + offset_y
                w = cell_size * camera['zoom']
                h = cell_size * camera['zoom']
                if 0:
                    text_surface = font_sm.render(f'x:{world_x}', True, color)
                    window.blit(text_surface, (x, y))
                    text_surface = font_sm.render(f'y:{world_y}', True, color)
                    window.blit(text_surface, (x, y+16*camera['zoom']))

def main_render():
    window.fill('#111111')
    render_grid()
    render_text()
    # debug
    if 0:
        text_surface = font_md.render(f'''{mouse['world_x']} - {mouse['world_y']}''', True, '0xFF00FF00')
        window.blit(text_surface, (600, 0))
        text_surface = font_md.render(f'''{mouse['screen_x']} - {mouse['screen_y']}''', True, '0xFF00FF00')
        window.blit(text_surface, (600, 48))
    if 1:
        if core['editor_mode'] == 0:
            text_surface = font_md.render(f'''NORMAL MODE''', True, '0xFF00FF00')
            window.blit(text_surface, (600, 0))
        elif core['editor_mode'] == 1:
            text_surface = font_md.render(f'''INSERT MODE''', True, '0xFF00FF00')
            window.blit(text_surface, (600, 0))
    pygame.display.flip()
    clock.tick(60)

running = True
while running:
    main_input()
    main_update()
    main_render()

pygame.quit()
