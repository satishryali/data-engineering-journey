# Requesting API data

An API lets one program ask another for data. This lesson used the Open-Meteo weather API to see a real network wait before comparing threads and async.

## Fetch one response

```python
import json
from urllib.request import urlopen

url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=17.385&longitude=78.4867&current=temperature_2m"
)
with urlopen(url, timeout=10) as response:
    data = json.load(response)

print(data["current"]["temperature_2m"])
```

**Expected output:** one temperature number. It changes over time. `urlopen()` sends the HTTP request; `json.load()` reads the JSON reply into Python data. `data["current"]["temperature_2m"]` selects one value from the returned dictionary.

The saved notebook successfully fetched Hyderabad weather, including `current.temperature_2m` (24.4 °C on 28 October and 27.2 °C on 29 October in two saved responses). These are observed API replies, not fixed expected values.

## Format parameters with urlencode

Typing query strings by hand (like `"?latitude=17.385&..."`) works for simple fixed numbers, but breaks when values contain spaces or reserved characters like `&` and `=`.

`urllib.parse.urlencode()` takes a Python dictionary and converts it into a valid URL query string.

**Why we need it:**
- **Spaces and symbols:** URLs cannot contain raw spaces or characters that have a special meaning in URLs. `urlencode()` converts spaces to `+` and symbols like `&` to `%26` so the server does not treat them as syntax.
- **Clean code:** Keeping query parameters in a dictionary makes it easy to add, change or remove parameters dynamically.

```python
import json
from urllib.parse import urlencode
from urllib.request import urlopen

base_url = "https://api.open-meteo.com/v1/forecast"

# 1. Keep parameters in a clean dictionary
params = {
    "latitude": 17.385,
    "longitude": 78.4867,
    "current": "temperature_2m"
}

# 2. Build the query string automatically
full_url = f"{base_url}?{urlencode(params)}"

with urlopen(full_url, timeout=10) as response:
    data = json.load(response)

print(data["current"]["temperature_2m"])
```

**Expected output:** one temperature number (changes over time, e.g. `27.2`).

**How the important lines work:**
- `urlencode(params)`: converts the dictionary into `"latitude=17.385&longitude=78.4867&current=temperature_2m"`.
- `f"{base_url}?..."`: attaches the generated query string to the base URL with a `?`.
- If a value contains spaces (e.g. `{"city": "New York", "query": "rock & roll"}`), `urlencode()` produces `city=New+York&query=rock+%26+roll`, preventing broken requests.

## A request error in the thread pool

The learner's first three-city request used `"current": "temperature_2"`. Open-Meteo returned HTTP **400 Bad Request** because the correct variable is `temperature_2m`. The worker's error appeared at `job.result()` because a `Future` holds either the worker's result or its error. After correction, the saved notebook printed temperatures for Hyderabad, Mumbai and Bengaluru. Check the API's parameter names and inspect its error response before blaming the pool.

## Choosing a Python tool

- `urllib.request` is included with Python and can send HTTP requests.
- `requests` is an additional package with a shorter synchronous interface, including `params=`, `.json()` and `.raise_for_status()`.
- `httpx` supports both synchronous and async HTTP requests. For real async waiting, use an async-compatible client rather than putting blocking `urllib` or `requests` calls inside `async def`.
- FastAPI has a different main job: it helps you **build** an API for other programs to call. An HTTP client can call that API. An API can exchange JSON records, files, form data or other supported formats; the systems must agree on the format.

The real three-city call worked with the existing thread pool. Switching clients is optional; it does not fix an invalid API parameter.

Sources: [Open-Meteo API](https://open-meteo.com/en/docs), [urllib.request](https://docs.python.org/3.14/library/urllib.request.html), [Requests](https://requests.readthedocs.io/en/latest/), [HTTPX](https://www.python-httpx.org/), [FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/). Practice: [async notebook](../../../practice/Sync/Async/async.ipynb).
