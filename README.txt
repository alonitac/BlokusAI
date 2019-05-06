301790515
777934738
*****
Comments:

(Appeals and explanation at the bottom.)

## blokus_cover_heuristic

To calculate the value of the heuristics we do the following steps:
Note the following terminology:
    - targets: targets that need to be covered to reach a goal state
    - corner : corner of the tiles
    - edge   : edge of the tile or tile pattern

for every target:
    calculate Manhattan distance from each covered location to target
    store minimum of those distances ("How close is the closest tile to the target?" equals 0 if target is covered)
    (** translate minimum distance to "admissible estimator of cost")
heuristic_value = sum of minimum distances

(**) The minimum distance (min_dist) needs a small modification to be a admissible heuristic. We have three cases:
     1) min_dist == 1: This is the worst possible case, because it means that the target is touching an edge of the
        tiles and cannot be reached anymore (because of the Blokus rules), which would result in an infinite cost.
        So we change: min_dist = infinity
     2) min_dist == 0: This means that the target is already covered, we don't need to change min_dist.
     3) min_dist > 1:
        - if the target lies directly horizontally or vertically to the tiles (which means to walk from the target to
          the tiles we only walk in either x or y direction). Then we add +1 to min_dist, because tiles can not touch
          each other at the edges, only over the corners so we need to make at least one turn.
        - if we need to walk into x and y direction from the target to the tiles:
          This is the part where taking the pure manhattan distance does not result in an admissible heuristic.
          The target might be 2 steps away from the tiles (if it is located next to a corner of a tile), but we ideally
          need only a 1-cost-tile to cover the target. The pure manhattan distance would overestimate the cost, so we
          need to change: min_dist = min_dist - 1 to keep min_dist a admissible estimator of the cost


## blokus_corners_heuristic

The corners heuristic works in the same way like the cover heuristic only that now the targets are the corners of the
board.


## Sub-Optimal Search

Our sub-optimal search is based on an A* search with an heuristic as described in blokus_cover_heuristic.
Only now instead of aiming to get closer to all targets per move (which means calculate the heuristic and consider all
targets), we are only interested in getting closer to the one target that is the closest (calculate heuristic for closest
target).
If the target is covered, we find a new closest target and move towards this one. This is repeated until all targets
are covered.

With this method we get the results (expanded nodes, cost):

| command | Sub-Optimal | Exercise sheet | BlokusCoverProblem |
| ------- | ----------- | -------------- | ------------------ |
| 1       | (8, 9)      | (21, 9)        | (85, 8)            |
| 2       | (8, 9)      | (23, 6)        | (16, 6)            |

And this is exactly what we wanted to achieve with this algorithm. Compared to the optimal solution (BlokusCoverProblem),
we get a drastic reduction in the expanded nodes, but with the trait-off of a higher cost.


## Mini Contest

For the Mini Contest we use A* search and the heuristics as described in blokus_cover_heuristics.
Compared to Sub-Optimal Search we now want to find the optimal solution that covers ALL targets.

In order to prune the search tree at least a little bit, we don't look at states anymore that were already evaluated
in a symmetric form.
Therefore for every state we first create a dictionary of its 8 variations (rotate (0, 90, 180, 270 Degrees),
flip horizontally and rotate again). Before the state is evaluated we first check if one of the symmetries were already
evaluated, if so we do not have to do it again.
To keep the dictionary of visited states small, we only save one of the state representatives, which should result in
a shorter lookup time in the future.

-----------------------------------------------------------------------------------------

# Appeals:

Dear course staff,

we have an appeal to the auto-grading of the Blokus exercise.
First a discussion about how we think the grading would have been more fair. The last paragraph explains, what we
changed in the code to deal with the error that we got in the first submission.

We got 3+5+1=9 points deducted because of the same error in our code. Whereas we understand why the auto-grader
deducts the points because no result was delivered, we find it pretty exaggerated that we get punished for the
same mistake three times.

Here an explanation where our code failed and what we think would be a more suitable way to deduct points:

## Question q6:

This is the part about the corner heuristic, Question q6 and q6a give together 3+1 points, q6 is where we failed.
Our approach was to use cover_heuristic with the corners of the board as target points. Since cover_heuristic
gives an error, we don't get any points for this question.

But in the description of the task you write:
"2 point for any admissible heuristic. The other 2 point will be awarded based on how many nodes your heuristic expands.
 The top 40% submissions will receive full credit +1 bones point; the next 35% will get 2 points and the other
 submissions will be awarded with 1 points."

How we designed our heuristics, it surely is admissible (explanation here in the readme file), so we think that
we should get the 2 points for the admissible heuristics.
About the points from comparison to our classmates: Of course we are not in the top 40%+35%, because of the error,
but we should at least get 1 point for the submission because our implementation of corner_heuristic itself is correct.

## Question q8 and q8a:

The description says:
"2 point for any admissible heuristic, A consistency heuristic will get another one points. The other 3 points will
 awarded based on the performance of your heuristic compared to your classmates."

Our heuristic is admissible and consistent, so we should get 3 points. But we again understand why we cannot get
the other 3 points in the comparison to our classmates, because cover_heuristic gave an error.

So from how we see it, we would understand a deduction of 4=1+3 points (question 6 + question 8)
instead of 9 points how it is now.

If you want, we can also meet and discuss it in person. Tuesday after the lecture would be good for us.

And for our own interest: Can you also tell us, which exact settings you chose for the questions?
Because when we run the commands from the instructions, the error does not appear. We can imagine it happening if the
heuristic is calculated for an empty board. We added two lines that will prevent this error from happening.
Now when the array of distances between the tiles and the targets is empty (if there was no target or no tiles to compute
the distance between), then the heuristic returns infinity, which is bigger than every other distance (that are finite),
so the search algorithm will still prefer to take an state where the heuristic could calculate an "actual" distance.

Have a nice day,
Alon and Franziska