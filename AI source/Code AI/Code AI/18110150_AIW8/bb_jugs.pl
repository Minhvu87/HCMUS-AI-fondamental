:- include(bb_planner).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%  bb_planner Example:  A Measuring Jugs Problem
%%  
%%  Changes: 1) Defined goal muliple possible goal_state options, which now
%%           works because of update to bb_planner
%%           2) Simplified and added explanation to the pour/4 predicate.

%%% There are three jugs (a,b,c), whose capacity is respectively:
%%% 3 litres, 5 litres and 8 litres.
%%% Initially jugs a and b are empty and jug c is full of water.

%%%% Goal: Find a sequence of pouring actions by which you can measure out
%%% 4 litres of water into one of the jugs without spilling any.

%%%  State representation will be as follows:
%%%  A state is a list:  [ how_reached, Jugstate1, Jugstate2, Jugstate3 ] 
%%%  Where each JugstateN is a lst of the form: [jugname, capcity, content]        
initial_state( [initial, [a,3,0], [b,5,0], [c,8,8]]).

%% Define goal state to accept any state where one of the
%% jugs contains 4 litres of water:
goal_state( [_, [a,_,4], [b,_,_], [c,_,_]]).
goal_state( [_, [a,_,_], [b,_,4], [c,_,_]]).
goal_state( [_, [a,_,_], [b,_,_], [c,_,4]]).

% Is it possible to get to this state?
%goal_state( [_, [a,_,_], [b,_,3], [c,_,3]]).
% Or this one?
%goal_state( [_, [a,_,_], [b,_,_], [c,_,6]]).

% What if I want to share out the water equally between two people?


%%% The state transitions are "pour" operations, where the contents of
%%% one jug is poured into another jug up to the limit of the capacity
%%% of the recipient jug.
%%% There are six possible pour actions from one jug to another:
transition( [_, A1,B1,C], [pour_a_to_b, A2,B2,C] ) :- pour(A1,B1,A2,B2).
transition( [_, A1,B,C1], [pour_a_to_c, A2,B,C2] ) :- pour(A1,C1,A2,C2).
transition( [_, A1,B1,C], [pour_b_to_a, A2,B2,C] ) :- pour(B1,A1,B2,A2).
transition( [_, A,B1,C1], [pour_b_to_c, A,B2,C2] ) :- pour(B1,C1,B2,C2).
transition( [_, A1,B,C1], [pour_c_to_a, A2,B,C2] ) :- pour(C1,A1,C2,A2).
transition( [_, A,B1,C1], [pour_c_to_b, A,B2,C2] ) :- pour(C1,B1,C2,B2).

%%% The pour operation is defined as follows:
% Case where there is room to pour full contents of Jug1 to Jug2
% so Jug 1 ends up empty and its contents are added to Jug2.
pour( [Jug1, Capacity1, Initial1], [Jug2, Capacity2, Initial2], % initial jug states
      [Jug1 ,Capacity1, 0],   [Jug2, Capacity2, Final2]         % final jug states
    ):- 
       Initial1 =< (Capacity2 - Initial2), 
       Final2 is Initial1 + Initial2.

% Case where only some of Jug1 contents fit into Jug2
% Jug2 ends up full and some water will be left in Jug1.
pour( [Jug1, Capacity1, Initial1], [Jug2, Capacity2, Initial2], % initial jug states
      [Jug1 ,Capacity1, Final1],   [Jug2, Capacity2, Capacity2] % final jug states
    ):- 
       Initial1 > (Capacity2 - Initial2), 
       Final1 is Initial1 - (Capacity2 - Initial2).

%% Define the other helper predicates that specify how bb_planner will operate:
legal_state( _ ).               % All states that can be reached are legal
equivalent_states( X, X ).      % Only identical states are equivalent.
loopcheck(on).                  % Don't allow search to go into a loop. 

%% Call this goal to find a solution.
%:- find_solution.

% This special comment adds the find_solution query to the examples menu
% under the console window.
/** <examples>
?- find_solution.
*/
