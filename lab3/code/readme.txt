To run this code, append the 'code' folder to your sys.path.
You should run something like this in your blender console:

  import sys
  sys.path.append("/path/to/code")
  import main
  import ex5

main has ex1, ex2, ex7 and 8 in it, with the following arguments:

  main.main(number_of_exercise, number_of_times_to_subdivide, list_of_edge_creases)

As for ex5, you should run:

  ex5.main(number_of_times_to_subdivide)

These functions, as well as subfunctions, are all documented and explain the process of subdivision.

Ex6's video is of a subdivision of n = 4.