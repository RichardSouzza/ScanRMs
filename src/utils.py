import os
from textwrap import TextWrapper
from contextlib import contextmanager, redirect_stderr, redirect_stdout


wrapper = TextWrapper(width=160) 


@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)
