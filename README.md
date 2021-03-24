# HTTP log

`http-log` is a command line tool that allows processing [Common Log Format logs](https://en.wikipedia.org/wiki/Common_Log_Format), display statistics about the processed data and alert when traffic exceeds an average ratio.

## Installation

In order to run this tool you'll need Python 3.7+ and [pip](https://pypi.org/project/pip/) installed. You'll need to install the dependencies defined in `requirements.txt`:

```
$ pip install -r requirements.txt
```

## Usage

By default the tool expects a log in `/tmp/access.log` to exists. You can run the tool with:

```
$ python bin/run
```

You can override the log file path and the alert threshold, this is a summary of usage options:

```
$ python bin/run -h
usage: run [-h] [--threshold THRESHOLD] [--log-file-path LOG_FILE_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --threshold THRESHOLD
  --log-file-path LOG_FILE_PATH

```

Running tests:

```
$ pytest http_log/tests/
```

### Using Docker

You can use Docker to run the tool:

```
$ docker build -t http-log:latest .
$ docker run -it --rm -v PATH_TO_LOG_FILE:/tmp/access.log http-log:latest
```

## Design

A diagram of the used design can be found in `design.png`. In next sections I mention some of the main decisions taken for the exercise.

### Sliding Time Windows

The main decision taken for the exercise has been using sliding time windows to aggregate the total requests in last 2 minutes and overall statistics in last 10 seconds. Using a time window allows very easily to delete old data from the accumulated value as more data is added or the accumulator value is accessed. We find these time windows:

- `SlidingTimeWindow[int]` that will accumulate total request in last 2 minutes
- `SlidinginTimeWindow[Stats]` that will aggregate statistics in a `Stats` object as more log entries are added

The sliding time windows are implemented using an internal queue object so adding to the back or getting from the front takes constant `O(1)` time.

`Stats` object is a convenient class that keeps total hits and hits per section or HTTP status code. It implements `__add__` and `__sub__` methods so it can be used by `SlidinginTimeWindow`.

### Python coroutines

Instead using threading and deal with shared objects like the sliding time windows I've decided to use concurrency through [`asyncio` coroutines](https://docs.python.org/3/library/asyncio-task.html). This has allowed me to implement the different stages of the processing pipeline quite easily.

### Pipeline stages

We can see 4 different stages in the processing pipeline, each of them implemented in different coroutine:

- `read`, will read and parse lines from the log file and enqueue `LogEntry` objects into a `asyncio.Queue`
- `process` will read `LogEntry` objects from a `asyncio.Queue` and add entries to the 2 sliding time windows
- `alerts` uses `asyncio` sleeps to run every second the alerts logic associated to one of the sliding time windows
- `stats` displays every 10 seconds the traffic statistics collected from the log

I decided to use an `asyncio.Queue` between `read` and `process` so reading the log file is decoupled of processing the sliding time windows.

## Improvements

Everything can be improved, here are some ideas:

- At the moment every log entry is added to time windows so it each window needs to keep the whole log for 120s or 10s respectively. That can be improved if we pre-aggregate log entries per second so we reduce the number of entries in the sliding window. I think this is really an improvement that I'd like to add. It'd be an easy change in `http_log.pipeline._process()`

- Add support for other log formats

- Though it's probably not needed, if the queue size gets higher between `read` and `process` we could spawn multiple `process()` coroutines

- It'd be ideal be able to define multiple alerts based on different properties of the logs. That'd push us to rethink a little how time windows are defined and/or used.
