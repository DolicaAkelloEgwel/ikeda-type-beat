from app import App
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES

ROW_HEIGHT = 10
GAP_HEIGHT = 2
N_ROWS = 240 // ROW_HEIGHT

class IkedaTypeBeat(App):
    def __init__(self):
      self.button_states = Buttons(self)

    def draw_lines(self, ctx):
        for i in range(N_ROWS):
            ctx.rgb(0,0,0).rectangle(-120, -120 + (i * ROW_HEIGHT), 240, GAP_HEIGHT).fill()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(255,255,255).rectangle(-120,-120,240,240).fill()
        self.draw_lines(ctx)

__app_export__ = IkedaTypeBeat
