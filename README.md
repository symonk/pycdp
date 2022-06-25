# PYCDP

-----
`pycdp` is a simple library that offers pythonic models around the devtools protocol.  It does not carry out
any sort of IO with a browser (at present), but instead is useful for libraries that choose to do so.

Chrome devtools protocol operates using bidirectional event driven architecture across websockets.  `pycdp` aims
to offer a pythonic API for marshalling commands / events across such connections.

You can read more about the devtools protocol [here](https://github.com/ChromeDevTools/devtools-protocol)

In a nutshell `pycdp` parses the protocol json files and dynamically generates python code for the various
types, commands and events inside each of the `domains`.  In future `pycdp` will look to support an
asynchronous IO layer utilising the generated modules to drive devtools based browsers.

At present `pycdp` does NOT generate domains that are marked as `deprecated` in the cdp specification.

----

#### Low Level Details

Chrome devtools protocol is built on the concept of `Domains`.  These domains typically expose an API
in the form of:

    * Commands
    * Types
    * Events

`pycdp` generates a per domain python module in idiomatic python syntax, fully typed hinted
for autocompletion assistance.

Types exposed by the protocol fall in to a few categories:

    * Primitive (tho not technically in python) types
        * string
        * integer
        * boolean
        * array
        * number
        * object
        * any
    * Enum types
    * Plain old python objects

"Primitive types" (again to use the term loosely) end up in simple subclasses of their primitive types
and all `object` types generate a fully type hinted idiomatic python class
