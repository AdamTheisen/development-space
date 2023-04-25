import functools
import logging
import io
import tempfile

logfile = tempfile.mkstemp(suffix='.log', dir='.')[1]
logging.basicConfig(level=logging.INFO, format='%(message)s', filename=logfile)
logger = logging.getLogger()

### Setup the console handler with a StringIO object
log_capture_string = io.StringIO()
ch = logging.StreamHandler(log_capture_string)
ch.setLevel(logging.INFO)
### Add the console handler to the logger
logger.addHandler(ch)

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.info(f"{func.__name__}() called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper

@log
def sum(a, b=10):
    return a+b

if __name__ == "__main__":
    a = sum(10, b=20)
    a = sum(a, b=20)

    print('test')
    ### Pull the contents back into a string and close the stream
    log_contents = log_capture_string.getvalue()
    log_capture_string.close()

    ### Output as lower case to prove it worked. 
    print(log_contents.lower())
