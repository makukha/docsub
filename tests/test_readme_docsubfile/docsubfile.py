from docsub import Environment, click, pass_env

@click.group()
def x() -> None:
    pass

@x.command()
@click.argument('users', nargs=-1)
def say_hello(users: tuple[str, ...]) -> None:
    for user in users:
        click.echo(f'Hi there, {user}!')

@x.command()
@click.argument('users', nargs=-1)
@pass_env
def log_hello(env: Environment, users: tuple[str, ...]) -> None:
    base = env.get_temp_dir('log_hello')
    (base / 'hello.log').write_text(f'said hello to {users}')
