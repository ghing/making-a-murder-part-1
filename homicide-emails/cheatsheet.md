# Useful make and command line stuff

## Why make?

Make was originally designed to build source code files in languages like C, but it's good for journalism because it's general purpose is to do tasks when some files must be updated automatically from others when the others change.

We have to do this a lot in journalism because we're transforming and cleaning source data into a format that's more useful to us.  Make can preserve the in-between steps, so you're never altering your source data.  It also makes you break your problem into little pieces which can be useful if you're working with a large data set where re-running a process would take a really looong time.

## Anatomy of a Makefile 

Make's behavior is controlled by a program, called a makefile.  This is usually named `Makefile`.

Sections of a makefile are called "rules". They say how to make a "target" from a set of "prerequisites" using a "recipe".

A rule looks something like this:

```
some_target_file.txt : prereq1.txt preqreq2.txt prereq3.pdf
	some_shell_command prereq1.txt prereq2.txt && \
	another_shell_command prereq3.pdf
```

When you run `make`, a target will be rebuilt of any of the preqrequisites have a newer timestamp than the target.  If there are rules for any of the prerequisites, make will build those too (if needed).

That's why make is cool for data pipelines.  You can just define your rules and then `make` will just updates the parts that change.  This helps make your data work reproducible.

One non-obvious thing: the recipe is indented using a tab, not spaces.

Another thing: if you want your command to continue on multiple lines, you need to end the line with a `\`.  This is the same in most shell scripts, I think.

## Make runs the first rule it finds

If you just run `make` in a directory with a `Makefile`, make will run the first rule it finds in the file.  It's conventional to define a rule with a target named `all` as the first rule.

## You can use variables in makefiles

You can define variables in a Makefile.  This is particularly useful for defining lists of filenames.

```
DATA_DIR = data
INPUT_FILES = file1 file2 file3
```

There are some useful functions that you can call on variables to make things like building file paths easier (and a lot more).  See https://www.gnu.org/software/make/manual/html_node/Functions.html#Functions.

```
DATA_DIR = data
INPUT_FILES = file1 file2 file3
INPUT_PATHS = $(addprefix $(DATA_DIR)/,$(INPUT_FILES))
```

To reference a variable elsewhere in the Makefile, you use `$(VAR_NAME)`.

You've probably noticed that the `$` character has special meaning in Makefiles, so if you want to use it to reference a variable in the shell code in your recipes, you need to escape it by using two `$` characters.  For example `$$some_env_var`.

There are some special variables when working inside a rule in a Makefile:

* `$@` is the file name of the target
* `$<` is the name of the first prerequisite 
* `$^` is the filenames of all the prerequisites, separated by spaces
* `$?` is the filenames of all the prerequisites that are newer than the target

Using these not only saves typing, it also makes your recipes more flexible when you decide to change filenames.

If we had this rule:

```
output_file.txt : input_file1.txt input_file2.txt
	# This is the recipe made up of some shell commands ...
```

then inside the recipe, `$@` would be replaced by `output_file.txt`, `$<` would be replaced by `input_file1.txt` and `$^` would be replaced by `input_file1.txt input_file2.txt`.

## Command line stuff

### Redirecting output

The UNIX philosophy is to write a lot of small programs that do one and only one thing.  You can do powerful things by tying the programs together using a `|` which passes the output of one program to the input of another.  That's also a good way to write little helper programs because you can just have them read and write from standard input/output and you don't have to worry about other processing input and output filename arguments. 

If you want to read input from a file, you can use `<`.

If you want to write output from a file, you can use `>`.

### splitting text files

The `split` command can split a text file either by size or by a regular expression.

### running a command on a bunch of files

Sometimes you want to run the same command on a bunch of files.  You can do this by using a special feature of the `find` command.  You could do this with a loop in a shell script too, but one-liners are cool.

For example, this command will output all the markdown files in the current directory or subdirectories:

```
find ./ -name *.md -print0 | xargs -0 -n 1 cat
```

`./` is where to search for the files that you'll process.

`-print0` separates the found files with null characters instead of newlines.  This makes it easier in many cases to pass the results to other programs.

`xargs` is a command that takes a list of strings on standard input and uses the strings as arguments to a command.  This is how we run some program for each item. 

`-0` tells xargs that the input strings (in this case file paths) are separated by null characters.

`-n 1` causes xargs to take the input strings one at a time.  Otherwise we would run `cat` with all the filenames as arguments, which would work ok in this case, but isn't what we'd want for more complicated programs.

`cat` is the program that will get run on each of the input strings to xargs.  Essentially `cat /path/to/file` will get run for each file path output by `find`.  We could use any program that takes command line arguments here.

### ndjson

ndjson stands for newline delimited JSON and it's like a file format where each line is a JSON object.  It's useful because it works well with piping commands together or streaming data over a network.  

Mike Bostock's [Command Line Cartography](https://medium.com/@mbostock/command-line-cartography-part-1-897aa8f8ca2c) series shows some pretty amazing uses of the command line and the power of ndjson.

### pretty printing JSON

```
cat ugly_json.json | python -m json.tool
```

## Getting help with a command line tool

The `man` command shows the user manual for a particular command, e.g. `man make`.  Examples are usually at the bottom and these are usually easier to understand than all the command options. 

## Other resources

* [GNU make manual](https://www.gnu.org/software/make/manual/html_node/) - useful reading because sometimes the language of make is weird
* [Making Data, the DataMade Way](https://github.com/datamade/data-making-guidelines)
