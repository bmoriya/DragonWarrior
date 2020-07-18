from unittest import TestCase

import pygame as pg
import pygame_menu
from pygame import init, Surface, FULLSCREEN, RESIZABLE, DOUBLEBUF, USEREVENT, time
from pygame.display import set_mode, set_caption
from pygame.event import get
from pygame.time import Clock
from pygame.time import get_ticks
from pygame.transform import scale

from src import maps
from src.camera import Camera
from src.common import UNARMED_HERO_PATH, get_image, \
    DRAGON_QUEST_FONT_PATH
from src.config import SCALE, TILE_SIZE, FULLSCREEN_ENABLED, NES_RES
from src.maps import parse_animated_spritesheet
from tests.test_game import TestMockMap


class TestDragonWarriorMap(TestCase):
    GAME_TITLE = "Dragon Warrior"
    FPS = 60

    ORIGIN = (0, 0)
    BLACK, WHITE, RED = (0, 0, 0), (255, 255, 255), (255, 0, 0)
    BACK_FILL_COLOR = BLACK
    MOVE_EVENT = USEREVENT + 1
    time.set_timer(MOVE_EVENT, 100)

    def setUp(self) -> None:
        # Initialize pygame
        self.all_sprites = []
        self.rects = []
        self.oldrects = []
        self.activerects = []
        self.dragon_warrior_theme = pygame_menu.themes.Theme(background_color=self.BLACK, cursor_color=self.WHITE,
                                                             cursor_selection_color=self.WHITE,
                                                             focus_background_color=self.BLACK,
                                                             title_background_color=self.BLACK,
                                                             title_font=DRAGON_QUEST_FONT_PATH,
                                                             title_font_size=8 * SCALE, title_offset=(32 * SCALE, 0),
                                                             widget_font=DRAGON_QUEST_FONT_PATH,
                                                             widget_alignment=pygame_menu.locals.ALIGN_LEFT,
                                                             widget_background_color=self.BLACK,
                                                             widget_font_color=self.WHITE,
                                                             widget_font_size=8 * SCALE,
                                                             widget_margin=(10 * SCALE, 5 * SCALE),
                                                             widget_offset=(0, 5 * SCALE),
                                                             widget_selection_effect=pygame_menu.widgets.
                                                             LeftArrowSelection(blink_ms=500))
        self.opacity = 0
        init()
        self.command_menu_launched, self.paused = False, False
        # Create the game window.
        if FULLSCREEN_ENABLED:
            flags = FULLSCREEN | DOUBLEBUF
        else:
            flags = RESIZABLE | DOUBLEBUF
        self.screen = set_mode((NES_RES[0] * SCALE, NES_RES[1] * SCALE), flags)
        self.screen.set_alpha(None)
        set_caption(self.GAME_TITLE)
        self.roaming_character_go_cooldown = 3000
        self.next_tile_checked = False

        unarmed_hero_sheet = get_image(UNARMED_HERO_PATH)
        unarmed_hero_tilesheet = scale(unarmed_hero_sheet, (
            unarmed_hero_sheet.get_width() * SCALE, unarmed_hero_sheet.get_height() * SCALE))
        self.unarmed_hero_images = parse_animated_spritesheet(unarmed_hero_tilesheet, is_roaming=True)

        # self.current_map = maps.TantegelThroneRoom(hero_images=self.unarmed_hero_images)
        self.current_map = maps.TantegelCourtyard(hero_images=self.unarmed_hero_images)
        # self.current_map = maps.Overworld(hero_images=self.unarmed_hero_images)

        # self.current_map = maps.TestMap(hero_images=self.unarmed_hero_images)

        self.bigmap_width, self.bigmap_height = self.current_map.width, self.current_map.height
        self.bigmap = Surface((self.bigmap_width, self.bigmap_height)).convert()
        self.bigmap.fill(self.BACK_FILL_COLOR)
        self.player_moving = False
        self.speed = 2

        self.current_map.load_map()
        for roaming_character in self.current_map.roaming_characters:
            roaming_character.last_roaming_clock_check = get_ticks()
            roaming_character.column, roaming_character.row = roaming_character.rect.x // TILE_SIZE, roaming_character.rect.y // TILE_SIZE
        # Make the big scrollable map

        self.background = Surface(self.screen.get_size()).convert()
        initial_hero_location = self.current_map.get_initial_character_location('HERO')
        self.hero_layout_row, self.hero_layout_column = initial_hero_location.take(0), initial_hero_location.take(1)
        self.camera = Camera(hero_position=(int(self.hero_layout_column), int(self.hero_layout_row)),
                             current_map=self.current_map, speed=None)
        self.allow_command_menu_launch = False
        self.enable_animate, self.enable_roaming, self.enable_movement = True, True, True
        self.clock = Clock()
        self.events = get()
        self.background = self.bigmap.subsurface(self.ORIGIN[0], self.ORIGIN[1], self.current_map.width,
                                                 self.current_map.height).convert()
        self.command_menu_launch_flag = False
        self.command_menu_subsurface = self.background.subsurface((self.hero_layout_column * TILE_SIZE) - TILE_SIZE * 2,
                                                                  (self.hero_layout_row * TILE_SIZE) - (TILE_SIZE * 6),
                                                                  TILE_SIZE * 8, TILE_SIZE * 5)
        self.command_menu = pygame_menu.Menu(height=self.command_menu_subsurface.get_height() * 3,
                                             width=self.command_menu_subsurface.get_width() * 2, title='COMMAND',
                                             center_content=False, column_force_fit_text=False,
                                             column_max_width=(TILE_SIZE * 1, TILE_SIZE * 3), columns=2, enabled=True,
                                             joystick_enabled=True, mouse_enabled=False, mouse_visible=False, rows=4,
                                             theme=self.dragon_warrior_theme)
        pg.event.set_allowed([pg.QUIT])

        self.dragon_warrior_map = TestMockMap(hero_images=self.unarmed_hero_images)

    def test_get_initial_character_location(self):
        self.assertEqual(self.dragon_warrior_map.get_initial_character_location('HERO').take(0), 0)
        self.assertEqual(self.dragon_warrior_map.get_initial_character_location('HERO').take(1), 0)

    def test_get_tile_by_value(self):
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(0), 'ROOF')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(1), 'WALL')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(2), 'WOOD')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(3), 'BRICK')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(4), 'CHEST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(5), 'DOOR')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(6), 'BRICK_STAIRDN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(7), 'BRICK_STAIRUP')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(8), 'BARRIER')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(9), 'WEAPON_SIGN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(10), 'INN_SIGN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(11), 'CASTLE')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(12), 'TOWN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(13), 'GRASS')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(14), 'TREES')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(15), 'HILLS')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(16), 'MOUNTAINS')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(17), 'CAVE')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(18), 'GRASS_STAIRDN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(19), 'SAND')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(20), 'MARSH')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(21), 'BRIDGE')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(22), 'WATER')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(23), 'BOTTOM_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(24), 'BOTTOM_LEFT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(25), 'LEFT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(26), 'TOP_LEFT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(27), 'TOP_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(28), 'TOP_RIGHT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(29), 'RIGHT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(30), 'BOTTOM_RIGHT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(31), 'BOTTOM_TOP_LEFT_COAST')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(32), 'BOTTOM_TOP_RIGHT_COAST')

        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(33), 'HERO')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(34), 'KING_LORIK')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(35), 'DOWN_FACE_GUARD')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(36), 'LEFT_FACE_GUARD')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(37), 'UP_FACE_GUARD')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(38), 'RIGHT_FACE_GUARD')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(39), 'ROAMING_GUARD')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(40), 'MAN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(41), 'WOMAN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(42), 'WISE_MAN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(43), 'SOLDIER')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(44), 'MERCHANT')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(45), 'PRINCESS_GWAELIN')
        self.assertEqual(self.dragon_warrior_map.get_tile_by_value(46), 'DRAGONLORD')
