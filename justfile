@install:
    hatch run python --version

@example-server:
    cd example && hatch run litestar run --reload

@example-lt *ARGS:
    cd example && hatch run litestar {{ ARGS }}
