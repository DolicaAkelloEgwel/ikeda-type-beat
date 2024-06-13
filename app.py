from app import App
from random import choice, randrange, randint
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

MAX = 120
SCREEN_SIZE = MAX * 2

ROW_HEIGHT = 10
GAP_HEIGHT = 1
BLOCK_HEIGHT = ROW_HEIGHT - GAP_HEIGHT
N_ROWS = MAX * 2 // ROW_HEIGHT

# these need to be even numbers
LOWER_BLOCK = 4
UPPER_BLOCK = 18

LOWER_SPEED = 1
MAX_SPEED = 18

POSITION_LIST = [i for i in range(-120, 120)]


def _sample(population, n_vals):
    if n_vals > len(population):
        raise ValueError("Sample larger than population or is negative")
    result = []
    indices = set()
    while len(result) < n_vals:
        index = randrange(len(population))
        if index not in indices:
            indices.add(index)
            result.append(population[index])
    return sorted(result)


class IkedaTypeBeat(App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.block_pos = []
        self.speeds = [randint(LOWER_SPEED, MAX_SPEED) for _ in range(N_ROWS)]

        for _ in range(N_ROWS):
            n_block_points = choice(range(LOWER_BLOCK, UPPER_BLOCK, 2))
            self.block_pos.append(self.get_random_points(n_block_points))

    def get_random_points(self, n_block_points):
        points = _sample(POSITION_LIST, n_block_points)
        return [[points[i], points[i + 1]] for i in range(0, len(points), 2)]

    def draw_lines(self, ctx):
        for i in range(N_ROWS):
            ctx.rgb(0, 0, 0).rectangle(
                -MAX, -MAX + (i * ROW_HEIGHT), SCREEN_SIZE, GAP_HEIGHT
            ).fill()

    def draw_mirror_block(self, ctx, x1, x2, y, h):
        w = x2 - x1
        if x1 > x2:
            ctx.rgb(0, 0, 0).rectangle(x1, y, MAX - x1, h).fill()
            ctx.rgb(0, 0, 0).rectangle(-MAX, y, x2 + MAX, h).fill()
        else:
            ctx.rgb(0, 0, 0).rectangle(x1, y, w, h).fill()

    def move_blocks(self, ctx):
        for i in range(N_ROWS):
            for xs in self.block_pos[i]:
                y = (i * ROW_HEIGHT + GAP_HEIGHT) - MAX

                self.draw_mirror_block(ctx, xs[0], xs[1], y, BLOCK_HEIGHT)

                xs[0] += self.speeds[i]
                xs[1] += self.speeds[i]

                if xs[0] >= MAX:
                    xs[0] -= SCREEN_SIZE
                if xs[1] >= MAX:
                    xs[1] -= SCREEN_SIZE

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(255, 255, 255).rectangle(-MAX, -MAX, SCREEN_SIZE, SCREEN_SIZE).fill()
        self.draw_lines(ctx)
        self.move_blocks(ctx)


__app_export__ = IkedaTypeBeat
