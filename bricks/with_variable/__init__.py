import os

def hello_with_variable():
    name = os.getenv("NAME")
    print(f"Hi: {name} from with_variable brick")