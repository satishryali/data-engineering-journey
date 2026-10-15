# Notes
## Logging Module

```python
import logging

logging.basicConfig(level = INFO,format = "%(asctime)s - %(levelname)s - %(message)s - %(lineno)d")

Logger = logging.getLogger(__name__)
```

- If you want the full list you can actually refer to the logattributes in python in google or documentation.

- s for text and d for numbers %(asctime)s - %(levelname)s - %(message)s - %(lineno)d

- if you want to save the logs to different files you can use file_name, file_mode

```python
logging.basicConfig(filename = r"C:\GIT\TESTING\Tests\Logging\app.log",filemode='a',level=logging.INFO,format="%(asctime)s - %(levelname)s (%(name)s) : %(message)s")
```

- Tip : If you always want to keep the logs after the filename then use this python command :

```python
log_path = Path(__file__).resolve().parent / "app.log"
```

- Absolute Path : An absolute path gives the full location of a file, starting from the drive:

```python
C:\GIT\TESTING\Tests\Logging\Log.py
```

- Relative Path : A relative path gives a location starting from your current working directory:

```python
Tests\Logging\Log.py
```

- parent : actually taking care of moving one folder up.


# TIPS

# When you are not sure about the error using logging.exception in the except section.
- except exception as e:
    logging.exception("message")
- This will gives us the error.
