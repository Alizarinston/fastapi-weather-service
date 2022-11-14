# FastApi Weather Service

This is a service that allows to see the weather by zip code.

**_TODO_: Cover with tests;**

**_TODO_: Search suggestions from the favorites list (there are already backend and frontend methods - only need to create a block with a drop-down list);**

**_TODO_: Split the `ZipWeather` component of the front into components and optimize;**

## Local development

### Setup

We highly recommend to use provided script to setup everything by single command.
Just run the following command from project's root directory and follow instructions:

* `backend/bin/setup`

That's all!

### Style guides and name conventions

#### Linters and code-formatters

We use git-hooks to run linters and formatters before any commit.
It installs git-hooks automatically if you used `backend/bin/setup` command.
So, if your commit is failed then check console to see details and fix linter issues.

We use:

* black - code formatter
* mypy - static type checker
* flake8 - logical and stylistic lint
* flake8-bandit - security linter
* safety - security check for requirements

and few other flake8 plugins, check `backend/requirements/development.txt` for more details.

In order to run checkers manually use the following bash script:

```bash
backend/bin/pre-commit
```

### Base commands

```bash
docker-compose up  # To run FastAPI application server

# Useful commands
backend/bin/pytest # Run tests
backend/bin/aerich migrate  # Create migrations files based on `models` files
backend/bin/aerich upgrade  # Run database migrations
backend/bin/shell  # Run python shell
```
