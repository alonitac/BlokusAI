301790515
777934738
*****
Comments:

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