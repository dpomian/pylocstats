# pylocstats
## Motivation
The motivation behind this project is to be able to parse one or multiple python repositories and generate statistics around the number of lines of code at function level. There are several tools and static analyzers that are able to produce all sorts of code statistics, but I haven't found one that would compute the number of lines of code for each function.

## How to install
For convenience I've included a [conda](https://www.anaconda.com/) environment file that you can use to replicate the environment needed to run this tool.

1. Install Anaconda. Refer to [anaconda official documentation](https://docs.anaconda.com/anaconda/install/).
2. Edit the ```name``` and ```prefix``` configuration in ```condaenv/environment.yml``` so that it points to where your other conda environments are.
3. Install the conda environment using the ```conda/environment.yml``` file. You can do so by following the [official documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file).
