% Here is the (mostly) given code from the assignment first:

% Probabilities of failure
0.05::faulty_motion_sensor(living_room).
0.05::faulty_motion_sensor(hallway).
0.02::faulty_light_sensor.
0.03::faulty_temp_sensor.
0.01::faulty_thermostat.
0.01::power_failure.

% Probabilities of normal conditions
0.9::movement(living_room).
0.8::movement(hallway).
0.95::light_switch_on.

% Failure probability based on other conditions
motion_detected(Room) :-
    not(faulty_motion_sensor(Room)),
    movement(Room).

light_on :-
    not(faulty_light_sensor),
    light_switch_on.

heating_on :-
    not(faulty_thermostat),
    not(power_failure).

% Other rules based on sensor readings
light_failure :- not(light_on).
no_heating :- not(heating_on).
incorrect_temp_reading :- faulty_temp_sensor.

% Here are the sample queries we showed as an example in the writeup.
% These can be uncommented to run them and obtain the same results as we got 
% in the writeup
%
% Sample Queries:

% Evidences at time 1
% evidence(motion_detected(living_room), false).
% evidence(light_on, false).

% Evidences at time 2
% evidence(motion_detected(living_room, true).
% evidence(light_on, true).

% Queries for whole system
% query(faulty_light_sensor).
% query(faulty_motion_sensor(hallway)).
% query(faulty_motion_sensor(living_room)).
% query(faulty_thermostat).
% query(power_failure).


% There are other sets of evidence and queries we wrote that were 
% "interesting". Uncomment them to run each individually. They will not work
% independently due to conflicting evidence.
%
% The first set is given int the writeup, then we included 5 more sets, for
% a total of 6 sets, to (hopefully) fulfill the "interesting queries" requirement

% Query Set 1: No motion and no light
% Simulates a situation where the system doesn't detect motion or light.
% Tests likelihood of sensor or power failure when no activity is observed.
% Expect higher probability for sensor faults or power issues.

evidence(motion_detected(living_room), false).
evidence(light_on, false).
query(faulty_motion_sensor(living_room)).
query(power_failure).
query(faulty_light_sensor).


% Query Set 2: Motion detected but lights are off
%
% Tests whether the light sensor or power supply is more likely to be at fault
% when motion is observed but lights don't turn on.

% evidence(motion_detected(living_room), true).
% evidence(light_on, false).
% query(faulty_light_sensor).
% query(power_failure).
% query(faulty_thermostat).


% Query Set 3: Conflicting sensor evidence
% Tries to create ambiguity—motion is detected, but heating and lights are off.
% Helps identify whether multiple components may be failing at once.

% evidence(motion_detected(hallway), true).
% evidence(light_on, false).
% evidence(no_heating, true).
% query(faulty_light_sensor).
% query(faulty_thermostat).
% query(power_failure).
