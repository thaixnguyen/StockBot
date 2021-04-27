import invoke


@invoke.task(
    help={"arg": "(Takes docker-compose arguments. Use quotes for multiple arguments.)"}
)
def compose(c, arg):
    """
    Acts as docker-compose
    """
    c.run(f"docker-compose -f docker/docker-compose.yml {arg}", pty=True)


@invoke.task
def exec(c):
    """
    Gets you into the docker container shell
    """
    compose(c, "exec stockbot /bin/bash")


@invoke.task
def build(c):
    """
    Builds the containers
    """
    compose(c, "build")


@invoke.task(help={"verbose": "(Prints docker-compose log in real time)"})
def dev(c, verbose=False):
    """
    One-button solution for getting the containers up and run the bot
    """
    compose(c, "up -d")
    if verbose:
        compose(c, "logs -f")
    print("Containers are now up.")


@invoke.task
def restart(c, verbose=False):
    compose(c, "stop")
    dev(c, verbose=verbose)


@invoke.task
def requirements(c):
    """
    Exports your pipenv environment to requirements.txt
    """
    c.run("pipenv run pip freeze > requirements.txt")


@invoke.task
def runbot(c):
    """
    Runs the bot
    """
    compose(c, "exec stockbot python /apps/stockbot/stockbot.py")
