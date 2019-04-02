12345678
777934738
*****
Comments:

## blokus_corner_heuristic

To calculate the value of the heuristics we do the following steps:
Note the following terminology:
    - targets: corner of the board
    - corner : corner of the tiles

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


## blokus_cover_heuristic

The cover heuristic works in the same way as the corner heuristic only that now the targets are variable and not fixed
at the board.



-p small_set.txt -f astar -s 10 10 -H blokus_cover_heuristic -z cover -x 3 3 "[(2,2), (5, 5), (6, 7)]"

-p small_set.txt -f astar -s 8 8 -H blokus_cover_heuristic -z cover -x 3 3 "[(0,8), (8, 0), (8, 8)]"


-p valid_pieces.txt -s 10 10 -z sub-optimal -x 7 7 "[(5,5), (8,8), (4,9)]"

(4, 13) l (21, 9)

-p valid_pieces.txt -s 10 10 -z sub-optimal -x 5 5 "[(3,4), (6,6), (7,5)]"

(8, 11) l (23, 6)