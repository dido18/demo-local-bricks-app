import time

from arduino.app_utils import App

from hello_arduino import hello_arduino
from with_variable import hello_with_variable
from with_submodule import hello_baa
from with_submodule.foo.hello import hello_foo
from with_container import getMetric, ping
from with_requirements import hello_fancy

hello_arduino()

hello_with_variable()

hello_baa()

hello_foo()

hello_fancy()

def loop():
    ping()
    print("ping metrics:",  getMetric())

    time.sleep(5)

App.run(user_loop=loop)
