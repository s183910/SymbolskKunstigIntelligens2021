/*******************************************************\
|                Mavis: Searchclient                    |
|                        README                         |
\*******************************************************/

This readme describes how to use the included Python search client with the server that is contained in server.jar.

The server requires at least a JRE for Java 11, and has been tested with OpenJDK.

The Python searchclient has been tested with Python 3.9, but probably works with previous versions of Python 3.
The searchclient requires the 'psutil' package to monitor its memory usage; the package can be installed with pip:
    $ pip install psutil

All the following commands assume the working directory is the one this readme is located in.

You can read about the server options using the -h argument:
    $ java -jar server.jar -h

Starting the server using the searchclient:
    $ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py" -l levels/SAD1.lvl

The searchclient uses the BFS search strategy by default. Use arguments -dfs, -astar, or -greedy to set
alternative search strategies (after you implement them). For instance, to use DFS search on the same level as above:
    $ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py -dfs" -l levels/SAD1.lvl

When using either -astar or -greedy, you must also specify which heuristic to use. Use arguments -goalcount or
-advancedheuristic to select between the two heuristic in domains/hospital/heuristics.py.
For instance, to use A* search with a goal count heuristic, on the same level as above:
    $ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py -astar -goalcount" -l levels/SAD1.lvl


Action libraries:
    'domains/hospital/actions.py' defines two action libraries:
    - 'DEFAULT_HOSPITAL_ACTION_LIBRARY' which is selected by default
    - 'STICKY_HOSPITAL_ACTION_LIBRARY' which can be selected by adding "-sticky" to the command line parameters.

Agent types:
    The folder 'agent_types' contains multiple different type of agents which can be selected using the command line:
    - 'classic' - A classic planning agent using GRAPH-SEARCH. Selected by default.
    - 'serial' - A planning agent using SERIAL-GRAPH-SEARCH. Select by adding "-serial" to the command line.
    - 'decentralised' - A planning agent using DECENTRALISED-AGENTS. Select by adding "-decentralised" to the command line.
    - 'helper' - A planning agent using the helper agent algorithm. Select by adding "-helper" to the command line.
    - 'non_deterministic' - A planning agent using AND-OR-GRAPH-SEACH with a broken executor.
                            Select by adding "-nondeterministic" to the command line.

We can then combine different types of frontiers, action libraries and agent types, e.g we can start a serial graph search
using sticky actions and a greedy search strategy with a goal count heuristic using the following combination of flags:
    $ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py -bfs -serial -sticky" -l levels/SAFirefly.lvl
Note that the order of the flags does not matter.

Memory settings:
    * Unless your hardware is unable to support this, you should let the searchclient allocate at least 4GB of memory *
    The searchclient monitors its own process' memory usage and terminates the search if it exceeds a given number of MiB.
    To set the max memory usage to 4GB:
        $ java -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py --max-memory 4g" -l levels/SAD1.lvl
    Avoid setting max memory usage too high, since it will lead to your OS doing memory swapping which is terribly slow.

Rendering on Unix systems:
    We experienced poor performance when rendering on some Unix systems, because hardware rendering is not turned on by default.
    To enable OpenGL hardware acceleration you should use the following JVM option: -Dsun.java2d.opengl=true
        $ java -Dsun.java2d.opengl=true -jar server.jar -g -s 300 -t 180 -c "python searchclient/searchclient.py" -l levels/SAD1.lvl
    See http://docs.oracle.com/javase/8/docs/technotes/guides/2d/flags.html for more information.
