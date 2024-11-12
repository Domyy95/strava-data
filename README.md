# Strava Insight

This project goal is to get insights from Strava activities, visualizing them and provide some useful strava tools.

## Project setup

The project uses [pre-commit](https://pre-commit.com/) cli to add git hooks for:
- release management: [commitizen](https://commitizen-tools.github.io/commitizen/)
- linter and code formatter: [ruff](https://docs.astral.sh/ruff/)

In order to setup the development environment it is possible to run the following command on terminal inside the project folder:

```shell
$ make setup-dev-env
```

This command will install development requirements from requirements-dev.txt file, including pytest,
and setup ***pre-commit*** hooks.

## Run the project
1. retrieve the client_id, client_secret and refresh_token from the strava api. You can follow the instructions [here](https://developers.strava.com/docs/getting-started/#account) to get them.

2. create an .env file in the root of the project with the following content:
```shell
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
REFRESH_TOKEN=your_refresh_token
```

3. run the following command to install the dependencies:
```shell
$ make install
```

4. run the following command to run the project:
```shell
$ make run
```

or if you use vs code you can just add this configuration to your launch.json file:
```json
{
    "configurations": [
        {
            "name": "Run",
            "type": "debugpy",
            "request": "launch",
            "module": "streamlit",
            "args": [
                "run",
                "src/main.py"
            ],
        }

    ]
}
```


## Git hooks
Git hook scripts are useful for identifying simple issues before submission to code review.
We run our hooks on every commit to automatically point out issues in code such as missing semicolons, trailing whitespace, and debug statements.

Before commit every change you should install [`pre-commit`](https://pre-commit.com) package in your enviroment:
```
pip install pre-commit
pre-commit install
```

then you can simply run against all the files:
```
pre-commit run --all-files
```
```
trim trailing whitespace.................................................Passed
fix end of files.........................................................Passed
check toml...............................................................Passed
check yaml...............................................................Passed
check for merge conflicts................................................Passed
ruff.....................................................................Passed
ruff-format..............................................................Failed
- hook id: ruff-format
- files were modified by this hook

1 file reformatted
```

#### Modify configuration for these utility tools:
- pre-commit general settings -> .pre-commit-config.yaml
- ruff settings -> .pyproject.toml
- commitizen settings -> .pyproject.toml

### Dependencies management

There are 2 levels of dependencies:
- development dependencies: they are all the dependencies needed to develop on the current repository, such as pytest and ruff
- library/package dependencies: they are all dependencies used by the library

To add more dependencies it is necessary to modify the requirements*.in files and run the following command:
```shell
$ make requirements*.txt
```
This command will lock all the direct and transitive dependencies in the requirements*.txt file.

### Important more commands are stored in the Makefile
