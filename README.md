# CSP-Final-Project
An implementation of Gale-Shapely plus a new, more heuristic based approach to matching

## Dependencies

You need numpy in order to run the code.

On Ubuntu, run the commands 'sudo pip install --upgrade pip', then run 'sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose'.  The second command takes a while..

## Usage 

There are two ways to run the application.  One is just by running the script with no arguments, like '$ python main.py'.  The other is to generate random system and user matricies at runtime by adding the flag '-N' or '--newMatricies', followed by row and column length, for example: '$ python main.py -N 4 4'.

## Current Issues (Notes)

When the male to female proposal paradigm is set for both the new algorithm and GS, GS consistently ranks at a higher utility than the new algorithm.  How can we fix this? However, after modifications and testing for many to many matching is done, will the results still be as bad?

Options:
- Calculate heuristic differently
	-- Calculate same way but on users instead of systems
	-- Find the median utility instead of the sum (try for both system and user, but what would be tie breaker?)
	-- Look into Boston algorithm mentioned by Prof
- Sort proposal order differently based on heuristic (highest to lowest right now, maybe lowest to highest?)
