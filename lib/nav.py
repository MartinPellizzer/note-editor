camera = {
    'pos_x': 0,
    'pos_y': 0,
    'pan_x': 0,
    'pan_y': 0,
    'zoom': 1,
}

mouse = {
    'world_x': 0,
    'world_y': 0,
    'screen_x': 0,
    'screen_y': 0,
    'row_i': 0,
    'col_i': 0,
    'action_executing': 0,
    'pan_executing': 0,
    'pan_mouse_start_x': 0,
    'pan_mouse_start_y': 0,
    'pan_camera_start_x': 0,
    'pan_camera_start_y': 0,
    'drag_executing': 0,
    'drag_mouse_start_x': 0,
    'drag_mouse_start_y': 0,
    'drag_node_id': None,
    'drag_node_start_x': 0,
    'drag_node_start_y': 0,
    'draw_line_executing': 0,
    'draw_line_start_x': 0,
    'draw_line_start_y': 0,
    'draw_line_end_x': 0,
    'draw_line_end_y': 0,
    'right_click_action_executing': 0,
}

def mouse_pos_get(pygame, window_w, window_h):
    mouse['world_x'], mouse['world_y'] = pygame.mouse.get_pos()

def pan_start(pygame):
    if mouse['pan_executing'] == 0:
        mouse['pan_mouse_start_x'] = mouse['world_x']
        mouse['pan_mouse_start_y'] = mouse['world_y']
        mouse['pan_camera_start_x'] = camera['pan_x']
        mouse['pan_camera_start_y'] = camera['pan_y']
    mouse['pan_executing'] = 1
    camera['pan_x'] = mouse['pan_camera_start_x'] + (mouse['world_x'] - mouse['pan_mouse_start_x']) // camera['zoom']
    camera['pan_y'] = mouse['pan_camera_start_y'] + (mouse['world_y'] - mouse['pan_mouse_start_y']) // camera['zoom']

def pan_stop():
    mouse['pan_executing'] = 0

def zoom_pos_center(window_w, window_h):
    cx = window_w // 2
    cy = window_h // 2
    offset_x = cx * (1 - camera['zoom'])
    offset_y = cy * (1 - camera['zoom'])
    return offset_x, offset_y

