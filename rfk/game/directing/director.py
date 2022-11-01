from turtle import position
from game.shared.point import Point
from game.shared.color import Color
import random
from game.casting.artifact import Artifact
from game.services.keyboard_service import KeyboardService
from game.services.video_service import VideoService
import time
from game.casting.actor import Actor
from pyray import get_mouse_x

FRAME_RATE = 12
MAX_X = 900
MAX_Y = 600
CELL_SIZE = 15
FONT_SIZE = 15
COLS = 60
ROWS = 40
CAPTION = "Robot Finds Kitten"

WHITE = Color(255, 255, 255)
DEFAULT_ARTIFACTS = 40


class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._score = 0
        
        
    def start_game(self, cast):
        """Starts the game using the given cast. Runs the main game loop.

        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.open_window()
        
        
        while self._video_service.is_window_open():
            self._get_inputs(cast)
            self._do_updates(cast)
            self._do_outputs(cast)
        self._video_service.close_window()

    def _get_inputs(self, cast):
        """Gets directional input from the keyboard and applies it to the robot.
        
        Args:
            cast (Cast): The cast of actors.
        """
        robot = cast.get_first_actor("robots")
        velocity = self._keyboard_service.get_direction()
        robot.set_velocity(velocity)        

    def _do_updates(self, cast):
        """Updates the robot's position and resolves any collisions with artifacts.
        
        Args:
            cast (Cast): The cast of actors.
        """
        
        banner = cast.get_first_actor("banners")
        robot = cast.get_first_actor("robots")
        artifacts = cast.get_actors("artifacts")

        banner.set_text("")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        robot.move_next(max_x, max_y)

        for artifact in artifacts:
            
            get_x = artifact.get_position().get_x()
            get_y = artifact.get_position().get_y()
            artifact.set_position(Point(get_x, get_y+5))

            
        for artifact in artifacts:
            if robot.get_position().equals(artifact.get_position()):
                
                if artifact.get_text() == '*':
                    self._score += 1
                else:
                    self._score -= 1
                
        text = random.choice(['*','O'])
        x = random.randint(1, COLS - 1)
        y = random.randint(1, ROWS - 1)
        position = Point(x, y)
        position = position.scale(CELL_SIZE)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        color = Color(r, g, b)
        
        artifact = Artifact()
        artifact.set_text(text)
        artifact.set_font_size(FONT_SIZE)
        artifact.set_color(color)
        artifact.set_position(position)
        
        cast.add_actor("artifacts", artifact)
        banner = Actor()
        banner.set_text(self._score)
        banner.set_font_size(FONT_SIZE)
        banner.set_color(WHITE)
        banner.set_position(Point(CELL_SIZE, 0))
        cast.add_actor("banners", banner)

        keyboard_service = KeyboardService(CELL_SIZE)
        video_service = VideoService(CAPTION, MAX_X, MAX_Y, CELL_SIZE, FRAME_RATE)
        director = Director(keyboard_service, video_service)
        
        
         
        
    def _do_outputs(self, cast):
        """Draws the actors on the screen.
        
        Args:
            cast (Cast): The cast of actors.
        """
        self._video_service.clear_buffer()
        actors = cast.get_all_actors()
        self._video_service.draw_actors(actors)
        self._video_service.flush_buffer()