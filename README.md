# Juno Python

This is a library that provides you with helper methods for interfacing with the microservices framework, [juno](https://github.com/bytesonus/juno).

## How to use:

There is a lot of flexibility provided by the library, in terms of connection options and encoding protocol options. However, in order to use the library, none of that is required.

In case you are planning to implement a custom connection option, you will find an example in `src/connection/unix_socket_connection.py`.

For all other basic needs, you can get away without worrying about any of that.

### A piece of code is worth a thousand words

```python
import asyncio
from typings import Dict, Any

from juno_python import JunoModule

def print_hello(args: Dict[str, Any]):
	print('Hello')

def main():
    module = JunoModule.default('./path/to/juno.sock')
	# The None below is used to mark dependencies
    await module.initialize('module-name', '1.0.0', None)
    print("Initialized!")
    await module.declare_function('print_hello', print_hello)
    # The None below marks the arguments passed to the function
    await module.call_function('module2.print_hello_world', None)    
	asyncio.get_running_loop().run_forever()

if __name__ == "__main__":
	main()
```