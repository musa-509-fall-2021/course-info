from contextlib import contextmanager
from time import time, perf_counter


@contextmanager
def record_time():
    timer = {'start': time(), 'end': None, 'duration': None}
    yield timer
    timer['end'] = time()
    timer['duration'] = timer['end'] - timer['start']


@contextmanager
def print_time(template, **kwargs):
    with record_time() as timer:
        yield
    print(template.format(**timer), **kwargs)
