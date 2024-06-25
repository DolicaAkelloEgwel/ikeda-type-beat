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


def create_block_points(count):
    block_points = []
    for _ in range(count):
        n_block_points = choice(range(LOWER_BLOCK, UPPER_BLOCK, 2))
        block_points.append(_get_random_points(n_block_points))
    return block_points


class BlockStream:
    def __init__(self):

        self._block_stream_speeds = [
            randint(LOWER_SPEED, UPPER_SPEED) for _ in range(N_ROWS)
        ]
        self._block_stream_pos = create_block_points(N_ROWS)

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
        self.n_cols = 2
        self.cols = [(255, 255, 255), (0, 0, 0)]

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(255, 255, 255).rectangle(-MAX, -MAX, SCREEN_SIZE, SCREEN_SIZE).fill()
        ctx.restore()
        block_points = create_block_points(self.n_cols)
        for i in range(self.n_cols):
            for j in range(len(block_points[i])):
                ys = block_points[i][j]
                height = ys[1] - ys[0]
                ctx.rgb(0, 0, 0).rectangle(i * MAX - MAX, ys[0], MAX, height).fill()
        ctx.save()


class DynamicColumns:
    def __init__(self, max_cols=4):
        self.max_cols = max_cols
        self.block_points = create_block_points(self.max_cols)
        self.speeds = [(i % 2) * 4 - 2 for i in range(self.max_cols)]
        self.counter = 0
        self.block_width = SCREEN_SIZE / self.max_cols

    def draw_mirror_block(self, ctx, x, y1, y2):
        if y1 > y2:
            ctx.rgb(0, 0, 0).rectangle(
                x,
                -MAX,
                self.block_width,
                MAX + y2,
            ).fill()
            ctx.rgb(0, 0, 0).rectangle(
                x,
                y1,
                self.block_width,
                MAX - y1,
            ).fill()
        else:
            ctx.rgb(0, 0, 0).rectangle(
                x,
                y1,
                self.block_width,
                y2 - y1,
            ).fill()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(255, 255, 255).rectangle(-MAX, -MAX, SCREEN_SIZE, SCREEN_SIZE).fill()
        for i in range(self.max_cols):
            x = i * self.block_width - MAX
            for ys in self.block_points[i]:
                self.draw_mirror_block(ctx, x, ys[0], ys[1])

                ys[0] += self.speeds[i]
                ys[1] += self.speeds[i]

                if ys[0] > MAX:
                    ys[0] -= SCREEN_SIZE
                if ys[1] > MAX:
                    ys[1] -= SCREEN_SIZE
                if ys[0] < -MAX:
                    ys[0] += SCREEN_SIZE
                if ys[1] < -MAX:
                    ys[1] += SCREEN_SIZE


class IkedaTypeBeat(App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.modes = [BlockStream(), TwoColumns(), DynamicColumns()]
        self.index = 0

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            self.index = (self.index - 1) % len(self.modes)
            self.button_states.clear()
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.index = (self.index + 1) % len(self.modes)
            self.button_states.clear()

    def draw(self, ctx):
        self.modes[self.index].draw(ctx)


__app_export__ = IkedaTypeBeat
