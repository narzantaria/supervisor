# Supervisor

The universal tool for automatic build and launch of your code on file changes.
Consists of two files:

1. **supervisor.py**: The main script.
2. **supervisor.cfg**: The configuration file.

### Why?

![why](media/why.png)

As an example, I will give programming in C++. Many developers use special environments, such as Qt and others that have built-in controls for compile and launch. However, if you work in *Visual Studio code* or other IDE and you want your code to be automatically rebuilt and launched after each change, then this tool may be useful for you.

### How it works

The script is made with Python language. When starting, it reads the configuration file and monitors the changes in the current folder. In the file changes, the script starts the process of compilation of the code of your target program. The script is constantly in standby mode and monitors changes in files, folders and subfolders.

For the correct working of the script in your operating system, the following packages should be installed:

* python.
* watchdog - the file system watching package.

You can start the script by following command in a console:

> python3 supervisor.py

The configuration file has a common view: `<FIELD>: <VALUE>`.

The descriptions of the field values are as follows:

* release_dir: folder for compilation result. 
* release_binary: The name of the final binary file. 
* command: the compilation command. 
* ignore: list of folders and files that will be ignored (not watched).

Before the compilation starts, a number of actions are performed - cleaning the release folder, closing the previous windows, etc. Finally - the binary is launched.

If you are working on a console application, then it will be launched in the same terminal where the script is launched. If it is a window (GUI) application, then after the compilation the window of your compiled file will be launched. Before that, the script will close all the previous windows of the application, if they were open.

The script can be interrupted using the combination "Ctrl+C".

In this case, the target code is made in C ++, but it can be another programming language. Python does not participate in the build process of the application - it only executes the compiler command (in this case g++).
You can play with a configuration and adjust the project for yourself.

The necessary tools for compilation of your target language should also be installed.

You can find detailed information about Python here: [https://www.python.org/downloads](https://www.python.org/downloads/).
Information about the *Watchdog* package is available here: [https://pypi.org/project/watchdog](https://pypi.org/project/watchdog/).

I hope this tool will help you in development and increase the effectiveness of your work.