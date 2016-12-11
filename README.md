# CSP-Final-Project #
An implementation of Gale-Shapely plus a new, more heuristic based approach to matching.  Refer to the final paper, section 4, for more details.

## Dependencies ##

You need numpy in order to run the code.

On Ubuntu, run the commands `sudo pip install --upgrade pip`, then run `sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose`.  The second command takes a while..

## Usage ##

There are several ways to run the application.  
* One is just by running the script with no arguments, like `python main.py`.  
* Another is to generate random system and user matricies at runtime by adding the flag '-N' or '--newMatricies', followed by row and column length, and then the number of matrices to generate.  For example: `python main.py -N 4 4 200`.  
* You can also specify the number of matches in many to many matching to look for by adding the flag `[--maxMatches/-M]` and then the number of matches.  For example: `python main.py -N 4 4 200 -M 2`
* It is also possible to run the large scale test set referenced in the final paper using the command `python main.py [--runTestSet/-R]`. 


