# plat

A simple interface to the `at` command scheduler.


## Motivation

The command-line interface for `at` is difficult to use. `at` reads
commands from stdin, expects an obscure datetime syntax, includes no
timezone support, and makes it difficult to view scheduled commands.

Plat is a Python interface to the unix `at` command scheduler. It may
someday evolve a command-line interface itself.

The name "plat" is taken from "simPLe AT".


## Installation

Plat assumes a recent version of the `at` command is installed and
available in the current path.


## Platforms

The output of the at command varies slightly by platform; plat
handles recent versions of Linux and macOS (neé Mac OS X). Windows is
currently unsupported (contributions welcome).


## Unsupported Features

`at` (via the `batch` command) includes the ability to associate
priority ("niceness") with scheduled jobs (via `at -q` or the `batch`
command, itself a shorthand for `at -q b`). Plat currently uses only
queue 'a' and does not currently support "nicer" job queues
(contributions welcome).

`at` also supports a flexible time specification format that allows
users to pass simple datetime math statements (e.g. 'noon + 3 days').
Plat explicitly omits this feature to promote standardization over
flexibility (contributions not welcome).
