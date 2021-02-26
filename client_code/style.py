from anvil.js.window import document


class Injector:
    def __init__(self):
        self.injected = []
        
    def inject(self, css):
        if not css in self.injected:
            sheet = document.createElement("style")
            sheet.innerHTML = css
            document.body.appendChild(sheet)
            self.injected.append(css)