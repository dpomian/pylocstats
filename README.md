# pylocstats
## Motivation
The motivation behind this project is to be able to parse one or multiple python repositories and generate statistics around the number of lines of code at function level. There are several tools and static analyzers that are able to produce all sorts of code statistics, but I haven't found one that would compute the number of lines of code for each function.

## How to install
For convenience I've included a [conda](https://www.anaconda.com/) environment file that you can use to replicate the environment needed to run this tool.

1. Install Anaconda. Refer to [anaconda official documentation](https://docs.anaconda.com/anaconda/install/).
2. Edit the ```name``` and ```prefix``` configuration in ```condaenv/environment.yml``` so that it points to where your other conda environments are.
3. Install the conda environment using the ```conda/environment.yml``` file. You can do so by following the [official documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).
4. Activate the conda environment. Follow the [official documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment)

## How to use it
To use this tool you'll need to follow the installation steps above, so you **install** and **activate** the conda environment.
After you have installed and activated the conda environment:
```
cd pylocstats/src
pylocstats/src > python cli.py -h
usage: pylocstats [-h] {clone,clone-single,stats,stats-single,plot} ...

Repos Stats

positional arguments:
  {clone,clone-single,stats,stats-single,plot}
                        commands
    clone               Clone multiple git repos
    clone-single        Clone a single git repo
    stats               Build Lines of Code stats
    stats-single        Single project
    plot                Violin plots
```

You can run help for each of the commands. For example if you would like to see what parameters does the clone command have, you can run:

```
pylocstats/src > python cli.py clone -h
usage: pylocstats clone [-h] --repos-file REPOS_FILE --dest-path DEST_PATH

optional arguments:
  -h, --help            show this help message and exit
  --repos-file REPOS_FILE
                        repo list file
  --dest-path DEST_PATH
                        destination path
```
