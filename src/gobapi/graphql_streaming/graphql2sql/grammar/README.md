# GraphQL grammar

The ```build.sh``` script in the root of ```src``` directory generates the parser.


# Generate new parser files
- Edit the grammar (`GraphQL.g4` in this directory)
- Run `./build.sh` from this directory from the development container. Antlr4 is pre-installed in the development container.

# How to ANTLR4 from your host environmen
Make sure [ANTLR4](https://www.antlr.org) is installed.

The name of the ANTLR-executable is system-dependent. Sometimes it is called ```antlr```, other times it is called ```antlr4```.

The build script default is ```antlr4```. To change this, run

```bash
export ANTLR_CMD=<<any other value>>
```

Run

```bash
./build.sh
```

to build and generate the project files.
