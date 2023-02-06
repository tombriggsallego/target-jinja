# target-jinja

`target-jinja` is a Singer target for Jinja2. It produces a set of output files from Jinja2 templates for each input record received. It was built with the [Meltano Target SDK](https://sdk.meltano.com).

Incoming records are provided to the Jinja2 library to render the provided templates. Thus the variable names available for use in templates are determined by the fields in the incoming data.

Output file names are generated using the `output_template` setting. Fields from the incoming record are also available for use when determining the output paths. Two additional variables are also available:

1. template_stem - the filename of the template being processed without the extension
2. template_suffix - the suffix of the template filename

## Example
Let's say you have a set of *N* dbt macros that you would like to call once for each of your *M* customers. To make that happen in dbt you need *N * M* models, where each model calls a macro and passes the internal customer ID to it.

target-jinja allows you to define a set of model templates with a placeholder for the customerId, then generate all the necessary model files based on data in the database. For example, create two model templates like so:

### Products Table Template
```
{{ onecustomer_product_table({{{ customerId }}}) }}
```

### Invoices Table Template
```
{{ onecustomer_invoice_table({{{ customerId }}}) }}
```

Put those two templates in a directory and set the `template_path` setting to point to that directory. Then set the `output_template` setting to something that puts each model into a customer-specific directory and has a customer specific name, e.g.

`/path/to/dbt/project/models/{{{ customerName }}}/{{{ template_stem }}}_{{{ customerId }}}{{{ template_suffix }}}`

Note that this example requires setting the `variable_start_string` and `variable_end_string` parameters to `{{{` and `}}}`, respectively, in order to avoid interfering with the formatting of the actual dbt model.

 Now define a tap in Meltano that retrieves a single stream containing your list of customers, including each customer's ID (in the customerId field). Run the tap and feed the data to the target, e.g.

`meltano run tap-somedb target-jinja`

and viola, you'll have two dbt models per customer in each customer-specific directory in your dbt project! Now when you run dbt it'll produce two tables per customer, named according to the customerId, and (assuming your macros are defined accordingly) contain only data for that customer.

## Installation

Install from GitHub:

```bash
pipx install git+https://github.com/tombriggs/target-jinja.git@main
```

## Capabilities

* `about`
* `stream-maps`
* `schema-flattening`

## Settings

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| template_path        | True     | None    | The path to the target template directory |
| output_template      | True     | None    | The Jinja template string with which output files will be named |
| variable_start_string| False    | None    | The string marking the beginning of a print statement |
| variable_end_string  | False    | None    | The string marking the end of a print statement |
| stream_maps          | False    | None    | Config object for stream maps capability. For more information check out [Stream Maps](https://sdk.meltano.com/en/latest/stream_maps.html). |
| stream_map_config    | False    | None    | User-defined config values to be used within map expressions. |
| flattening_enabled   | False    | None    | 'True' to enable schema flattening and automatically expand nested properties. |
| flattening_max_depth | False    | None    | The max depth to flatten schemas. |

A full list of supported settings and capabilities is available by running: `target-jinja --about`

### Configure using environment variables

This Singer target will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `target-jinja` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Target Directly

```bash
target-jinja --version
target-jinja --help
# Test using the "Carbon Intensity" sample:
tap-carbon-intensity | target-jinja --config /path/to/target-jinja-config.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `target_jinja/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `target-jinja` CLI interface directly using `poetry run`:

```bash
poetry run target-jinja --help
```

### Testing with [Meltano](https://meltano.com/)

_**Note:** This target will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd target-jinja
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke target-jinja --version
# OR run a test `elt` pipeline with the Carbon Intensity sample tap:
meltano elt tap-carbon-intensity target-jinja
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the Meltano Singer SDK to
develop your own Singer taps and targets.

