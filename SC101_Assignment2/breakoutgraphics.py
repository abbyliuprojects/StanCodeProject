"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
LIVES_SPACING = 10

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.


class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout', lives_count=3):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        paddle_x = (self.window.width - PADDLE_WIDTH) / 2
        paddle_y = self.window.height - PADDLE_OFFSET - PADDLE_HEIGHT
        self.paddle = GRect(PADDLE_WIDTH, PADDLE_HEIGHT, x=paddle_x, y=paddle_y)
        self.paddle.filled = True
        self.window.add(self.paddle)

        # Lives Left
        # for i in range(1, lives_count+1):
        #     lives_x = self.window.width - (LIVES_SPACING + LIVES_SIZE)*i
        #     lives = GOval(LIVES_SIZE, LIVES_SIZE, x=lives_x, y=self.window.height - LIVES_SIZE - LIVES_SPACING)
        #     lives.filled = True
        #     lives.fill_color = "red"
        #     self.window.add(lives)
        self.lives_count = lives_count
        self.lives_count_label = GLabel(f"{self.lives_count} Lives Left")
        self.lives_count_label.x = self.window.width - self.lives_count_label.width - LIVES_SPACING
        self.lives_count_label.y = self.window.height - self.lives_count_label.height - LIVES_SPACING
        self.window.add(self.lives_count_label)

        # Center a filled ball in the graphical window
        ball_size = BALL_RADIUS * 2
        self.ball = GOval(ball_size, ball_size)
        self.ball.filled = True
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dx = 0
        self.__dy = 0
        self.reset_ball()

        # Initialize our mouse listeners
        onmousemoved(self.paddle_move)
        onmouseclicked(self.start_game)
        self.is_game_started = False

        # Draw bricks
        self.total_bricks = 0
        brick_height_with_spacing = BRICK_HEIGHT + BRICK_SPACING
        for y in range(BRICK_OFFSET, BRICK_OFFSET + brick_height_with_spacing * BRICK_ROWS, brick_height_with_spacing):
            for x in range(0, (BRICK_WIDTH + BRICK_SPACING) * BRICK_COLS, BRICK_WIDTH + BRICK_SPACING):
                brick = GRect(BRICK_WIDTH, BRICK_HEIGHT, x=x, y=y)
                brick.filled = True
                brick_col_num = (y-BRICK_OFFSET)/brick_height_with_spacing
                if brick_col_num < 2:
                    color = "red"
                elif brick_col_num < 4:
                    color = "orange"
                elif brick_col_num < 6:
                    color = "yellow"
                elif brick_col_num < 8:
                    color = "green"
                else:
                    color = "blue"
                brick.fill_color = color
                self.window.add(brick)
                self.total_bricks += 1



    def get_dx(self):
        """
        Return the horizontal speed for the ball and reverse it if the ball hits the wall
        :return: int, the horizontal speed for the ball
        """
        if self.ball.x > self.window.width - self.ball.width or self.ball.x < 0:
            self.__dx = -self.__dx
        return self.__dx

    def get_dy(self):
        """
        Return the vertical speed for the ball
        :return: int, the vertical speed for the ball
        """
        return self.__dy

    def reset_ball(self):
        """
        Reset the position and speed for the ball
        """
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if random.random() > 0.5:
            self.__dx = -self.__dx
        self.ball.x = (self.window.width - self.ball.width) / 2
        self.ball.y = (self.window.height - self.ball.height) / 2
        self.is_game_started = False
        self.lives_count_label.text = f"{self.lives_count} Lives Left"

    def paddle_move(self, event):
        """
        Make the paddle move with mouse
        :param event: mouse event
        """
        if event.x > self.window.width - self.paddle.width:
            paddle_x = self.window.width - self.paddle.width
        else:
            paddle_x = event.x
        self.paddle.x = paddle_x

    def ball_jump(self):
        """
        Reverse the vertical speed for the ball
        """
        self.__dy = -self.__dy

    def start_game(self, event):
        """
        Set the game started by clicking mouse
        :param event: mouse event
        """
        if not self.is_game_started:
            self.is_game_started = True

    def check_ball_hit_object_and_alive(self):
        """
        Check if the ball hit any objects and return if the attempt is still alive
        :return: boolean, if the attempt still alive
        """
        for index_y in range(2):
            for index_x in range(2):
                x = self.ball.x + (self.ball.width * index_x)
                y = self.ball.y + (self.ball.height * index_y)

                if y >= self.window.height:
                    # if the ball hits the bottom of the window, it is failed
                    return False

                maybe_object = self.window.get_object_at(x, y)
                if maybe_object is not None and maybe_object is not self.lives_count_label:
                    if maybe_object is not self.paddle:
                        # ball hits the bricks
                        self.window.remove(maybe_object)
                        self.total_bricks -= 1
                        self.ball_jump()
                    elif maybe_object is self.paddle and self.__dy > 0:
                        # ball hits the paddle
                        self.ball_jump()
                    break
                elif y <= 0:
                    self.ball_jump()
                    break
        return True
