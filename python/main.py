import time
import os

from arduino.app_utils import App

from hello_arduino import hello_arduino
from with_variable import hello_someone
from with_submodule import hello_baa
from with_submodule.foo.hello import hello_foo
from with_container import getMetric, ping

hello_arduino()

hello_someone(os.getenv("NAME"))

hello_baa()
hello_foo()

def loop():
    set_led1_color(1,0,0)
    ping()
    metric = getMetric()
    print("ping metrics:", metric)

    time.sleep(5)
    set_led2_color(0,1,0)
    


App.run(user_loop=loop)
