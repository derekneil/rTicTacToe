![SCREENSHOTS](https://raw.github.com/derekneil/rtictactoe/master/symmetry.png "Before and After Symmetry")

##Symmetry
X infact only has 3 distinct opening moves. All other opening moves are simply mirrors, or rotations of these three distinct moves. The same can be said about many other board states as the game is played. Taking advantage of these equivalent board states, we can speed up the "exploration" time at the beginning of the game, and assign values to all equivalent states since they lead to the same actions.


![SCREENSHOTS](https://raw.github.com/derekneil/rtictactoe/master/oscilate_Randomness_at_10k_stop_at_70k.png "Randomness Influence")

##Randomness
Randomness had a significant impact on the outcomes of the games, even at %10, the player that was playing with randomness immediately began to lose more often compared to when both players were playing randomly. After 70k games we finally set both players back to playing without any random move selection and again we see the same red ­ draw rate for the last 1000 games shoot up to %100.