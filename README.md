# Candidate Smasher (Python)

Python port of the Ruby code Candidate Smasher on GitHub at <https://github.com/Display-Lab/candidate-smasher>


## Known Issues (as of 2022-08-07)

1. Issue with method Ruby merge\_external\_templates(): The variable “t\_ids” is set in the first line of the method but is not used. This is possibly a mistake.

1. The Ruby method generate\_candidates() uses the Ruby function flatten(). Python doesn't have an equivalent, so I wrote one. My flatten() function only flattens one level (i.e. it is equivalent to ruby flatten(1)). In the future, this function should be improved to use more than one level. I am not sure if this is an issue with actual data.
