# <h1 align="center">Tap-GetResponse</h1>


`tap-getresponse` is a Singer tap for GetResponse.

![logo](https://www.ekito.fr/wp-content/uploads/2021/07/getresponse_logo.png)

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.


<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPi:

```bash
pipx install tap-getresponse
```

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-getresponse.git@main
```

-->

## Configuration 📝

### Accepted Config Options


| Setting    | Required | Default | Description            |
| :--------- | :------: | :-----: | :--------------------- |
| auth_token |   True   |  None   | GetResponse token API. |

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.


```
# .env
TAP_GETRESPONSE_AUTH_TOKEN=... # your token!
```

### Source Authentication and Authorization

To get your API Token, follow the [official documentation](https://apidocs.getresponse.com/v3/authentication).

## Usage

You can easily run `tap-getresponse` by itself or in a pipeline using [Meltano](https://meltano.com/).


### Execute in a Meltano pipeline

#### Install the project

```bash
meltano install
```

#### Select Entities and Attributes to Extract

```bash
meltano select tap-getresponse <entity> <attribute>
meltano select tap-getresponse --exclude <entity> <attribute>

# For example:
meltano select tap-getresponse webinars "*"
```

Verify that only the intended entities and attributes are now selected using `meltano select --list`:
```bash
meltano select tap-getresponse --list
```

#### Run the pipeline

Run your newly added GetResponse extractor and chosen loader in a pipeline using `meltano run`:
```bash
meltano run tap-getresponse <loader>

# For example:
meltano run tap-getresponse target-jsonl
```

There is also the `meltano elt` (or `meltano el`) command which is a more rigid command for running only EL pipelines.

Or directly using the `meltano invoke`, which only executes a single plugin at a time. This can be useful for debugging the extractor (`meltano invoke tap-getresponse`).

```bash
# Test invocation:
meltano invoke tap-getresponse --version
# OR run a test `elt` pipeline:
meltano elt tap-getresponse <loader>
# Example
meltano elt tap-getresponse target-jsonl
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-getresponse` CLI interface directly using `poetry run`:

```bash
poetry run tap-getresponse --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

<!--
Developer TODO:
Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any "TODO" items listed in
the file.
-->

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-getresponse
meltano install
```


### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
