from cyclopts import App

app = App()


@app.command
def say_hello(*username: str):
    for u in username:
        print(f'Hi there, {u}!')


if __name__ == '__main__':
    app()
