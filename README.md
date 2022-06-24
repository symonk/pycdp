# pycdp
:snake: Pythonic marshalling of the devtools protocol

-----

`pycdp` is a simple library that offers pythonic models around the devtools protocol.  It does not carry out
any sort of IO with a browser, but instead is useful for libraries that choose to do so.

Chrome devtools protocol operates using bidirectional event driven architecture across websockets.  `pycdp` aims
to offer a pythonic API for marshalling commands / events across such connections.

You can read more about the devtools protocol [here](https://github.com/ChromeDevTools/devtools-protocol)
