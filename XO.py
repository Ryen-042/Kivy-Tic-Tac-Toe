from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.core.window import Window

class XO_Game(Widget):
    players = {1:'X', 2:'O'}
    curr_player = 1
    game_status = ''
    popup_opened = False
    popup_touch_status = False

    popup = Popup(
            title = 'Game Over!',
            title_align = 'center',
            size_hint = (0.3, 0.3),
            separator_color = [87/255, 1/255, 105/255, 1],
            background_color = [214/255, 39/255, 164/255, 0.7],
            auto_dismiss = True)
    
    def __init__(self, **kwargs):
        super(XO_Game, self).__init__(**kwargs)
        # After dismissing the popup, clear all cells to start a new game.
        self.popup.bind(on_dismiss=self.clear_cells)

        # Update `popup_touch_status` each time a touch is performed on the popup.
        self.popup.bind(on_touch_down = self.update_popup_touch_status)
        
        # To drag the popup.
        self.popup.bind(on_touch_move = self.pop_mov)
        
        # To play with keyboard keys.
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    # Change player if 'tie' or game not over yet. Don't Change if 'win'.
    def change_player(self):
        if XO_Game.curr_player == 1:
            XO_Game.curr_player = 2
        else:
            XO_Game.curr_player = 1

    # Check if the game is over.
    def win_check(self):
        if (
            self.ids.b1.text == self.ids.b2.text == self.ids.b3.text != "" or
            self.ids.b4.text == self.ids.b5.text == self.ids.b6.text != "" or
            self.ids.b7.text == self.ids.b8.text == self.ids.b9.text != "" or
            
            self.ids.b1.text == self.ids.b4.text == self.ids.b7.text != "" or
            self.ids.b2.text == self.ids.b5.text == self.ids.b8.text != "" or
            self.ids.b3.text == self.ids.b6.text == self.ids.b9.text != "" or
            
            self.ids.b9.text == self.ids.b5.text == self.ids.b1.text != "" or
            self.ids.b7.text == self.ids.b5.text == self.ids.b3.text != ""):
                # Change player if 'tie' or game not over yet. Don't Change if 'win'.
                self.game_status = 'win'
        
        elif "" not in {
            self.ids.b1.text, self.ids.b2.text, self.ids.b3.text,
            self.ids.b4.text, self.ids.b5.text, self.ids.b6.text,
            self.ids.b7.text, self.ids.b8.text, self.ids.b9.text}:
                self.game_status = 'tie'
        
        else:
            self.game_status = ''

    # Executes after each action from the players
    def process_before_next_action(self):
        self.win_check()
        if self.game_status in ['win', 'tie'] and not self.popup_opened:
            if self.game_status == 'win':
                XO_Game.popup.content = Label(text=f'{self.players[XO_Game.curr_player]} Wins!')
            
            else:
                XO_Game.popup.content = Label(text='Tie')
                self.change_player()
            
            XO_Game.popup.pos_hint={'center_x': 0.5, 'center_y': 0.5}
            XO_Game.popup.open()
            self.popup_opened = True
        else:
            self.change_player()

    #  Clearing all the cells.
    def clear_cells(self, instance):
        self.ids.b1.text = self.ids.b2.text = self.ids.b3.text = ""
        self.ids.b4.text = self.ids.b5.text = self.ids.b6.text = ""
        self.ids.b7.text = self.ids.b8.text = self.ids.b9.text = ""

        self.ids.b1.disabled = self.ids.b2.disabled = self.ids.b3.disabled = False
        self.ids.b4.disabled = self.ids.b5.disabled = self.ids.b6.disabled = False
        self.ids.b7.disabled = self.ids.b8.disabled = self.ids.b9.disabled = False
        
        # If the popup appears, the keyboard is unbound, so, we need to re-bind it.
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
        self.game_status = ''
        self.popup_opened = False

    # Playing with mouse.
    def play(self, instance):
        instance.text = self.players[XO_Game.curr_player]
        instance.disabled = True
        self.process_before_next_action()

    # Next Two functions are for playing with keyboard.
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Because the numbers in the numpad give different inputs from the ones in the number row,
        # we need to check both of them.
        numpads = [ "numpad1", "numpad2", "numpad3",
                    "numpad4", "numpad5", "numpad6",
                    "numpad7", "numpad8", "numpad9"]

        if keycode[1] in '123456789' or keycode[1] in numpads:
            if not self.popup_opened:
                if   keycode[1] in ['1', "numpad1"] and self.ids.b1.text == "":
                    self.ids.b1.text = self.players[XO_Game.curr_player]
                    self.ids.b1.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['2', "numpad2"] and self.ids.b2.text == "":
                    self.ids.b2.text = self.players[XO_Game.curr_player]
                    self.ids.b2.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['3', "numpad3"] and self.ids.b3.text == "":
                    self.ids.b3.text = self.players[XO_Game.curr_player]
                    self.ids.b3.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['4', "numpad4"] and self.ids.b4.text == "":
                    self.ids.b4.text = self.players[XO_Game.curr_player]
                    self.ids.b4.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['5', "numpad5"] and self.ids.b5.text == "":
                    self.ids.b5.text = self.players[XO_Game.curr_player]
                    self.ids.b5.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['6', "numpad6"] and self.ids.b6.text == "":
                    self.ids.b6.text = self.players[XO_Game.curr_player]
                    self.ids.b6.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['7', "numpad7"] and self.ids.b7.text == "":
                    self.ids.b7.text = self.players[XO_Game.curr_player]
                    self.ids.b7.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['8', "numpad8"] and self.ids.b8.text == "":
                    self.ids.b8.text = self.players[XO_Game.curr_player]
                    self.ids.b8.disabled = True
                    self.process_before_next_action()
                elif keycode[1] in ['9', "numpad9"] and self.ids.b9.text == "":
                    self.ids.b9.text = self.players[XO_Game.curr_player]
                    self.ids.b9.disabled = True
                    self.process_before_next_action()
                
                if self.game_status in ['win', 'tie']:
                    # Disable keyboard events to prevent the cells from being selected by the keyboard when the popup is open.
                    self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        
        if keycode[1] == 'escape':
            App.get_running_app().stop()
            Window.close()
        return True
    
    # Update `popup_touch_status` each time a touch is performed on the popup to prevent any accidental
    # moving of the popup when clicking and dragging outside it.
    def update_popup_touch_status(self, instance, touch):
        if  self.popup_opened:
            if (self.popup.x +10 <= touch.ox <= self.popup.x + self.popup.size[0] -10 and
                self.popup.y +10 <= touch.oy <= self.popup.y + self.popup.size[1] -5 ):
                    self.popup_touch_status = True
            else:
                self.popup_touch_status = False

    # For dragging the popup.
    def pop_mov(self, instance, touch):
        if self.popup_touch_status:
            XO_Game.popup.pos_hint={'center_x': touch.x / self.width, 'center_y': touch.y / self.height}
            # XO_Game.popup.pos_hint={'x': (self.popup.x + touch.dx)/self.width, 'y': (self.popup.y + touch.dy)/self.height}

class XOApp(App):
    def build(self):
        return XO_Game()

if __name__ == "__main__":
    	XOApp().run()
