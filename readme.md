# Environment Setup

Before running this script, please configure the following environment：

- Python3.0+

- BCC

  ~~~
  sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
  ~~~

- The wasm runtime you want to run, such as
  - [wasmer](https://github.com/wasmerio/wasmer)
  - [wasmtime]([bytecodealliance/wasmtime: A fast and secure runtime for WebAssembly (github.com)](https://github.com/bytecodealliance/wasmtime))
  - [wasm3](https://github.com/wasm3/wasm3)
  - [wamr](https://github.com/bytecodealliance/wasm-micro-runtime)
  - [wasmedge](https://wasmedge.org/)
  - and so on...





# Get Started

After the environment is configured, you can run `main.py` with arguments.

~~~
python3 main.py --runtime=[wasm runtime] --source=[wasm code] --times=[times]
~~~

Then you can monitor the execution time of the specified program in the specified runtime.

The data will be stored in the `.txt` file in the `/record` directory



