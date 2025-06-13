from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.lang import Builder
import random

class HomeScreen(Screen):
    pass

class GameScreen(Screen):
    score = NumericProperty(0)

    def on_enter(self):
        self.reset_game()

    def reset_game(self):
        self.score = 0
        self.ids.score_label.text = f"Score: {self.score}"
        self.create_grid()

    def create_grid(self):
        grid_placeholder = self.ids.grid_placeholder
        grid_placeholder.clear_widgets()
        grid = GridLayout(cols=6, rows=6, spacing=dp(2), size_hint=(None, None))
        grid.size = (dp(6 * 50), dp(6 * 50))

        colors = [(1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1), (1, 1, 0, 1), (1, 0, 1, 1)]
        self.buttons = []

        for _ in range(36):
            color = random.choice(colors)
            btn = Button(background_normal='', background_color=color)
            btn.bind(on_release=self.on_block_pressed)
            self.buttons.append(btn)
            grid.add_widget(btn)

        grid_placeholder.add_widget(grid)

    def on_block_pressed(self, instance):
        color = instance.background_color
        same_color_buttons = [btn for btn in self.buttons if btn.background_color == color and btn.opacity == 1]

        if len(same_color_buttons) >= 2:
            for btn in same_color_buttons:
                btn.opacity = 0
                btn.disabled = True
            self.update_score(len(same_color_buttons))

    def update_score(self, matches):
        self.score += matches ** 2
        self.ids.score_label.text = f"Score: {self.score}"

class BlocklyApp(App):
    def build(self):
        Builder.load_file("game.kv")
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    BlocklyApp().run()
