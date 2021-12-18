"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics

FRAME_RATE = 1000 / 120 # 120 frames per second
NUM_LIVES = 3			# Number of attempts


def main():
    """
    This program runs a breakout game.
    """
    global NUM_LIVES
    graphics = BreakoutGraphics(lives_count=NUM_LIVES)

    # Add animation loop here!
    while True:
        if graphics.is_game_started and graphics.lives_count > 0 and graphics.total_bricks > 0:
            dx = graphics.get_dx()
            dy = graphics.get_dy()
            graphics.ball.move(dx, dy)
            if not graphics.check_ball_hit_object_and_alive():
                graphics.lives_count -= 1
                graphics.reset_ball()
        pause(FRAME_RATE)


if __name__ == '__main__':
    main()
