from app import App
from random import choice, randrange
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

ROW_HEIGHT = 20
GAP_HEIGHT = 2
BLOCK_HEIGHT = ROW_HEIGHT - GAP_HEIGHT
N_ROWS = 240 // ROW_HEIGHT

LOWER_BLOCK = 8
UPPER_BLOCK = 20

POSITION_LIST = [i for i in range(-120,121)]

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
    return result

class IkedaTypeBeat(App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.block_pos = []

        for _ in range(N_ROWS):
            n_block_points = choice(range(LOWER_BLOCK, UPPER_BLOCK, 2))
            self.block_pos.append(self.get_random_points(n_block_points))

    def get_random_points(self, n_block_points):
        points = _sample(POSITION_LIST, n_block_points)
        return [(points[i], points[i+1]) for i in range(0, len(points), 2)]

    def draw_lines(self, ctx):
        for i in range(N_ROWS):
            ctx.rgb(0,0,0).rectangle(-120, -120 + (i * ROW_HEIGHT), 240, GAP_HEIGHT).fill()

    def mirror_block(self, ctx, rgb, x, y, w, h):
        pass
    
    def move_blocks(self, ctx):
        for i in range(N_ROWS):
            for xs in self.block_pos[i]:
                ctx.rgb(0,0,0).rectangle(xs[0], (i * ROW_HEIGHT + GAP_HEIGHT) - 120, xs[0] + xs[1], BLOCK_HEIGHT).fill()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(255,255,255).rectangle(-120,-120,240,240).fill()
        self.draw_lines(ctx)
        self.move_blocks(ctx)

__app_export__ = IkedaTypeBeat
