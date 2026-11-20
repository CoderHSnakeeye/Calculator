from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.utils import platform

# Window size for desktop testing
if platform not in ('android', 'ios'):
    Window.size = (360, 640)
    Window.minimum_width, Window.minimum_height = 360, 640

class CalcButton(Button):
    def __init__(self, text, kind='num', **kwargs):
        colors = {
            'num':  (0.98, 0.98, 0.98, 1),
            'op':   (0.0, 0.4, 0.8, 1),
            'func': (0.9, 0.9, 0.9, 1),
            'eq':   (0.16, 0.66, 0.27, 1),
        }
        txt_colors = {
            'num':  (0.1, 0.1, 0.1, 1),
            'op':   (1, 1, 1, 1),
            'func': (0.2, 0.2, 0.2, 1),
            'eq':   (1, 1, 1, 1),
        }
        super().__init__(
            text=text,
            font_size=sp(24),
            background_normal='',
            background_color=colors[kind],
            color=txt_colors[kind],
            bold=True,
            **kwargs
        )
        self.kind = kind

class CalculatorApp(App):
    def build(self):
        self.expr = ""
        self.last_was_operator = False

        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        # Display
        self.display = TextInput(
            text='0',
            font_size=sp(48),
            readonly=True,
            halign='right',
            valign='middle',
            multiline=False,
            background_color=(0.12, 0.12, 0.12, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=(dp(16), dp(16)),
            size_hint_y=None,
            height=dp(120),
        )
        root.add_widget(self.display)

        # Error label
        self.error_label = TextInput(
            text='',
            font_size=sp(14),
            readonly=True,
            halign='right',
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 0.3, 0.3, 1),
            size_hint_y=None,
            height=dp(24),
        )
        root.add_widget(self.error_label)

        # Button grid
        grid = GridLayout(cols=4, spacing=dp(8), size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        buttons = [
            ('C', 'func', 2), ('⌫', 'func'), ('%', 'func'), ('÷', 'op'),
            ('7', 'num'), ('8', 'num'), ('9', 'num'), ('×', 'op'),
            ('4', 'num'), ('5', 'num'), ('6', 'num'), ('−', 'op'),
            ('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'op'),
            ('0', 'num', 2), ('.', 'num'), ('=', 'eq', 2),
        ]

        for item in buttons:
            text = item[0]
            kind = item[1]
            span = item[2] if len(item) > 2 else 1
            btn = CalcButton(text=text, kind=kind, size_hint_y=None, height=dp(72))
            btn.bind(on_press=self.on_button)
            if span == 2:
                # Kivy doesn't support colspan directly; use nested layout
                wrapper = BoxLayout(size_hint_y=None, height=dp(72))
                btn.size_hint_x = 0.5
                wrapper.add_widget(btn)
                wrapper.add_widget(CalcButton(text='', kind=kind, size_hint_x=0.5, height=dp(72)))
                wrapper.children[1].opacity = 0
                wrapper.children[1].disabled = True
                grid.add_widget(wrapper)
            else:
                grid.add_widget(btn)

        root.add_widget(grid)
        return root

    def on_button(self, instance):
        text = instance.text
        kind = instance.kind

        if kind == 'num':
            if text == '.' and self._current_number_has_dot():
                return
            self.expr += text
            self._update_display()

        elif kind == 'op':
            if not self.expr:
                return
            if self.expr[-1] in '+-*/':
                self.expr = self.expr[:-1]
            self.expr += {'÷': '/', '×': '*', '−': '-', '+': '+'}.get(text, text)
            self._update_display()

        elif kind == 'func':
            if text == 'C':
                self.expr = ''
                self.error_label.text = ''
            elif text == '⌫':
                self.expr = self.expr[:-1]
            elif text == '%':
                self.expr += '*0.01'
            self._update_display()

        elif kind == 'eq':
            self._calculate()

    def _current_number_has_dot(self):
        # Check if current number (after last operator) already has a dot
        for op in '+-*/':
            idx = self.expr.rfind(op)
            if idx != -1:
                return '.' in self.expr[idx+1:]
        return '.' in self.expr

    def _calculate(self):
        if not self.expr:
            return
        try:
            allowed = set("0123456789+-*/().% ")
            if not all(c in allowed for c in self.expr):
                raise ValueError("Invalid characters")
            result = eval(self.expr, {"__builtins__": {}}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expr = str(result)
            self._update_display()
            self.error_label.text = ''
        except ZeroDivisionError:
            self.error_label.text = 'Error: Division by zero'
        except Exception:
            self.error_label.text = 'Error: Invalid expression'

    def _update_display(self):
        self.display.text = self.expr or '0'
        # Scroll to end
        self.display.cursor = (len(self.display.text), 0)

if __name__ == '__main__':
    CalculatorApp().run()