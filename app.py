from app import App
from random import choice, randrange, randint
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

MAX = 120
SCREEN_SIZE = MAX * 2

ROW_HEIGHT = 9
GAP_HEIGHT = 1
BLOCK_HEIGHT = ROW_HEIGHT - GAP_HEIGHT
N_ROWS = MAX * 2 // ROW_HEIGHT + 1

# these need to be even numbers
LOWER_BLOCK = 4
UPPER_BLOCK = 40

LOWER_SPEED = 1
UPPER_SPEED = 8

POSITION_LIST = [i for i in range(-120, 120)]

COLUMN_BLOCK_HEIGHT = 20


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


def _get_random_points(n_block_points):
    points = _sample(POSITION_LIST, n_block_points)
    return [[points[i], points[i + 1]] for i in range(0, len(points), 2)]


class BlockStream:
    def __init__(self):

        self._block_stream_speeds = [
            randint(LOWER_SPEED, UPPER_SPEED) for _ in range(N_ROWS)
        ]
        self._block_stream_pos = []
        for _ in range(N_ROWS):
            n_block_points = choice(range(LOWER_BLOCK, UPPER_BLOCK, 2))
            self._block_stream_pos.append(_get_random_points(n_block_points))

    @staticmethod
    def _draw_mirror_block(ctx, x1, x2, y, h):
        w = x2 - x1
        if x1 > x2:
            ctx.rgb(255, 255, 255).rectangle(x1, y, MAX - x1, h).fill()
            ctx.rgb(255, 255, 255).rectangle(-MAX, y, x2 + MAX, h).fill()
        else:
            ctx.rgb(255, 255, 255).rectangle(x1, y, w, h).fill()

    def _block_stream(self, ctx):
        for i in range(N_ROWS):
            for xs in self._block_stream_pos[i]:
                y = (i * ROW_HEIGHT + GAP_HEIGHT) - MAX

                self._draw_mirror_block(ctx, xs[0], xs[1], y, BLOCK_HEIGHT)

                xs[0] += self._block_stream_speeds[i]
                xs[1] += self._block_stream_speeds[i]

                if xs[0] >= MAX:
                    xs[0] -= SCREEN_SIZE
                if xs[1] >= MAX:
                    xs[1] -= SCREEN_SIZE

    def draw(self, ctx):
        clear_background(ctx)
        self._block_stream(ctx)


class TwoColumns:
    def __init__(self):
        # prepare list of points for columns mode
        self._column_block_pos = []
        for _ in range(2):
            column_points = []
            n_blocks = SCREEN_SIZE // COLUMN_BLOCK_HEIGHT
            for _ in range(n_blocks):
                column_points.append(
                    _sample([i for i in range(COLUMN_BLOCK_HEIGHT)], 2)
                )
            self._column_block_pos.append(column_points)

    def draw(self, ctx):
        ctx.rgb(255, 255, 255).rectangle(-MAX, -MAX, MAX, SCREEN_SIZE).fill()
        for i in range(2):
            for j in range(len(self._column_block_pos[i])):
                ys = self._column_block_pos[i][j]
                height = ys[1] - ys[0]
                offset = j * 24 - MAX + randint(0, COLUMN_BLOCK_HEIGHT - height)
                ctx.rgb(255 * i, 255 * i, 255 * i).rectangle(
                    i * MAX - MAX, offset, MAX, ys[1] - ys[0]
                ).fill()
                self._column_block_pos[i][j] = _sample([i for i in range(4, 10)], 2)


class IkedaTypeBeat(App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.modes = [BlockStream(), TwoColumns()]
        self._current = self.modes[0]
        self._index = 0

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            self._index = (self._index - 1) % len(self.modes)
            self._current = self.modes[self._index]
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self._index = (self._index + 1) % len(self.modes)
            self._current = self.modes[self._index]
            self.button_states.clear()

    def draw(self, ctx):
        self._current.draw(ctx)


__app_export__ = IkedaTypeBeat
