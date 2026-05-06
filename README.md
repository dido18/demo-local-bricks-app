# 😀 Demo — Local Bricks App

An Arduino App Lab application that demonstrates different ways to define and use **local bricks** — reusable Python modules that extend your app with extra functionality.

---

## What Are Local Bricks?

Local bricks live in the `bricks/` folder of your app. Each brick is a subdirectory containing:

- `brick_config.yaml` — brick metadata, id, and optional variable declarations
- `__init__.py` — Python code exposed to `main.py`
- *(optional)* `brick_compose.yaml` — Docker Compose services the brick depends on
- *(optional)* `README.md` — brick-level documentation

Bricks are registered in `app.yaml` and are automatically imported into `main.py` by their directory name.

---

## Bricks in This App

### 1. `hello_arduino` — Basic Python-only brick

The simplest brick pattern: a single `__init__.py` with a Python function.

```
bricks/hello_arduino/
├── brick_config.yaml
└── __init__.py          # exposes hello_arduino()
```

Usage in `main.py`:
```python
from hello_arduino import hello_arduino
hello_arduino()   # prints "Hi, I am arduino ;)"
```

---

### 2. `with_variable` — Brick that accepts a configuration variable

Declares a variable (`NAME`) in `brick_config.yaml`. The variable is injected as an environment variable and read via `os.getenv()`.

```
bricks/with_variable/
├── brick_config.yaml    # declares variable NAME (default: arduino)
└── __init__.py          # exposes hello_someone(name)
```

Variable declaration in `brick_config.yaml`:
```yaml
variables:
  - name: NAME
    description: a variable to be used to say hello to someone
    default_value: arduino
```

The app overrides the default in `app.yaml`:
```yaml
- with_variable:
    variables:
      NAME: a-var-value
```

Usage in `main.py`:
```python
import os
from with_variable import hello_someone
hello_someone(os.getenv("NAME"))   # prints "Hi: a-var-value"
```

---

### 3. `with_requirements` — Brick with external Python dependencies

Demonstrates how to specify external Python packages using a `requirements.txt` file. The brick can then import and use those dependencies.

```
bricks/with_requirements/
├── brick_config.yaml
├── requirements.txt     # external Python dependencies
└── __init__.py          # exposes hello_fancy()
```

`requirements.txt`:
```
pyfiglet==1.0.4
```

`__init__.py`:
```python
import pyfiglet

def hello_fancy():
    banner = pyfiglet.figlet_format("Hello World", font="slant")
    print(banner)
```

Usage in `main.py`:
```python
from with_requirements import hello_fancy
hello_fancy()   # prints a fancy ASCII banner
```

---

### 4. `with_submodule` — Brick with internal Python sub-modules

Shows how to structure a brick with nested Python packages inside it.

```
bricks/with_submodule/
├── brick_config.yaml
├── __init__.py          # re-exports hello_baa from .baa
├── baa.py               # defines hello_baa()
└── foo/
    ├── __init__.py
    └── hello.py         # defines hello_foo()
```

Usage in `main.py`:
```python
from with_submodule import hello_baa          # top-level re-export
from with_submodule.foo.hello import hello_foo  # deep import
hello_baa()
hello_foo()
```

---

### 5. `with_container` — Brick that spins up a Docker container

Uses `brick_compose.yaml` to start a companion service (`viktoruj/ping_pong`) alongside the app. The brick's Python code communicates with the container over its internal hostname.

```
bricks/with_container/
├── brick_config.yaml
├── brick_compose.yaml   # starts the pingpong service
└── __init__.py          # exposes ping() and getMetric()
```

`brick_compose.yaml`:
```yaml
services:
  pingpong:
    image: viktoruj/ping_pong
```

Usage in `main.py`:
```python
from with_container import getMetric, ping

def loop():
    ping()
    metric = getMetric()
    print("ping metrics:", metric)
```

---

## App Entry Point (`python/main.py`)

```python
from arduino.app_utils import App
import os, time

from hello_arduino import hello_arduino
from with_variable import hello_someone
from with_requirements import hello_fancy
from with_submodule import hello_baa
from with_submodule.foo.hello import hello_foo
from with_container import getMetric, ping

hello_arduino()
hello_someone(os.getenv("NAME"))
hello_fancy()
hello_baa()
hello_foo()

def loop():
    ping()
    print("ping metrics:", getMetric())
    time.sleep(5)

App.run(user_loop=loop)  # must be the last line
```

Expected output

```
======== App is starting ============================
Hi, I am arduino ;)
Hi: a-var-value
hello baa
hello foo
__  __     ____         _       __           __    __
/ / / /__  / / /___     | |     / /___  _____/ /___/ /
/ /_/ / _ \/ / / __ \    | | /| / / __ \/ ___/ / __  / 
/ __  /  __/ / / /_/ /    | |/ |/ / /_/ / /  / / /_/ /  
/_/ /_/\___/_/_/\____/     |__/|__/\____/_/  /_/\__,_/   

2026-05-06 10:09:10.489 INFO - [MainThread] App:  App started
ping metrics: {'goroutines': 6, 'requests_per_minute': 6.505213034913026e-09, 'requests_per_second': 1.0842021724855043e-10, 'requests_total': 1}
```

---

## App Registration (`app.yaml`)

All bricks must be listed in `app.yaml`:

```yaml
name: App with local bricks
bricks:
  - hello_arduino: {}
  - with_container: {}
  - with_variable:
      variables:
        NAME: a-var-value
  - with_requirements: {}
  - with_submodule: {}
```
