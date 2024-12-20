# tap-jsonlinesfile

`tap-jsonlinesfile` is a Singer tap for JsonLinesFile.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

<!--

Developer TODO: Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

## Installation

Install from PyPi:

```bash
pipx install tap-jsonlinesfile
```

Install from GitHub:

```bash
pipx install git+https://github.com/ORG_NAME/tap-jsonlinesfile.git@main
```

-->

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-jsonlinesfile --about --format=markdown
```
-->

| Setting | Required | Default | Description |
|:--------|:--------:|:-------:|:------------|
| path | True     | None    | Path to directory to find jsonl files. |
| search_pattern | True     | None    | Search pattern to use when discovering files, using glob. Relative to 'path' |
| compression | False    | None    | Indicate if the files are compressed. Only support for `gz` currently. |
| variables_to_extract | False    | None    | A list of variables to extract, each with a JSON path and a column name. |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-jsonlinesfile --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-jsonlinesfile` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-jsonlinesfile --version
tap-jsonlinesfile --help
tap-jsonlinesfile --config CONFIG --discover > ./catalog.json
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

You can also test the `tap-jsonlinesfile` CLI interface directly using `poetry run`:

```bash
poetry run tap-jsonlinesfile --help
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
cd tap-jsonlinesfile
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-jsonlinesfile --version
# OR run a test `elt` pipeline:
meltano run tap-jsonlinesfile target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
