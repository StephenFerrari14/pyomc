import click


def printStep(step):
    def decorator(func):
        def wrapper(*args, **kwargs):
            click.echo(step)
            return func(*args, *kwargs)
        return wrapper
    return decorator