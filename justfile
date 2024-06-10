@install:
    hatch run python --version

@example-server:
    cd example && hatch run litestar run

@example-lt *ARGS:
    cd example && hatch run litestar {{ ARGS }}
