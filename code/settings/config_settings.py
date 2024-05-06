# game setup
WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
ENERGY_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = '../assets/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'red'
ENERGY_COLOR = 'yellow'
UI_BORDER_COLOR_ACTIVE = 'gold'

weapon_data = {
    'sword': {'cooldown': 100, 'damage': 15, 'graphic':'../assets/weapon/sword/full.png'},
    'tombak': {'cooldown': 100, 'damage': 30, 'graphic':'../assets/weapon/tombak/full.png'}
}

Enemy_Data = {
    'bamboo': {'healt': 300, 'damage': 30, 'deffend': 3, 'speed': 2, 'atk_radius': 80, 'ntc_radius': 300, 'attack_type': 'leaf_attack', 'attack_sound': '../audio/zeeep.wav'},
    'raccoon': {'healt': 900, 'damage': 50, 'deffend': 3, 'speed': 3, 'atk_radius': 125, 'ntc_radius': 400, 'attack_type': 'claw', 'attack_sound': '../audio/raccoon.wav'},
    'spirit': {'healt': 100, 'damage': 25, 'deffend': 3, 'speed': 3, 'atk_radius': 80, 'ntc_radius': 320, 'attack_type': 'thunder', 'attack_sound': '../audio/spirit.wav'},
    'squid': {'healt': 150, 'damage': 20, 'deffend': 3, 'speed': 2, 'atk_radius': 80, 'ntc_radius': 320, 'attack_type': 'slash', 'attack_sound': '../audio/zeeep.wav'},
    'rakunmalas': {'healt': 1500, 'damage': 150, 'deffend': 3, 'speed': 7, 'atk_radius': 125, 'ntc_radius': 400, 'attack_type': 'claw', 'attack_sound': '../audio/raccoon.wav'}
}