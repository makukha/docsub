from cyclopts import App

app = App()

@app.command
def say_hello(username: str, /):  # positional-only parameters
    print(f'Hi there, {username}!')
