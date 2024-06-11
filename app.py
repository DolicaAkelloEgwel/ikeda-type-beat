from app import App
from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES



class IkedaTypeBeat(App):
    def __init__(self):
      self.button_states = Buttons(self)

    def draw_lines(self, ctx):
        pass

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()

    def draw(self, ctx):
        clear_background(ctx)
        ctx.rgb(255,255,255).rectangle(-120,-120,240,240).fill()

__app_export__ = IkedaTypeBeat
