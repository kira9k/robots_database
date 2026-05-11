function [Optimized_DesignVars,Info] = feedforward_optimize(DesignVars, t, y)



load_system('lab12_a');

if nargin < 1 || isempty(DesignVars)
    DesignVars = sdo.getParameterFromModel('lab12_a','k_feedforward');
    DesignVars(1).Minimum = 0;
end

Requirements = struct;
Requirements.SignalTracking = sdo.requirements.SignalTracking(...
    'ReferenceSignal', getData('SignalTracking_ReferenceSignal', t, y), ...
    'Weights', getData('SignalTracking_Weights', t, y));

Simulator = sdo.SimulationTest('lab12_a');

Sig_Info = Simulink.SimulationData.SignalLoggingInfo;
Sig_Info.BlockPath = 'lab12_a/DC';
Sig_Info.LoggingInfo.LoggingName = 'Sig';
Sig_Info.LoggingInfo.NameMode = 1;

Simulator.LoggingInfo.Signals = Sig_Info;

Simulator = setup(Simulator, 'FastRestart', 'on');

SimulatorCleanup = onCleanup(@() restore(Simulator));

optimfcn = @(P) lab12_a_optFcn(P,Simulator,Requirements);

Options = sdo.OptimizeOptions;
Options.OptimizedModel = Simulator;
Options.BackupFilename = fullfile(pwd,'lab12_a__BackupfileSDO.mat');
Options.MethodOptions.MaxIterations = 50;


%if any(isnan(Vals.F(:))) || any(isinf(Vals.F(:)))
%    warning('Objective содержит NaN/Inf на начальной точке!');
%end

[Optimized_DesignVars,Info] = sdo.optimize(optimfcn,DesignVars,Options);

%% Update Model
%
% Update the model with the optimized parameter values.
sdo.setValueInModel('lab12_a',Optimized_DesignVars);
end

function Vals = lab12_a_optFcn(P,Simulator,Requirements)
%LAB12_A_OPTFCN
%
% Function called at each iteration of the optimization problem.
%
% The function is called with a set of parameter values, P, and returns
% the objective value and constraint violations, Vals, to the optimization
% solver.
%
% See the sdoExampleCostFunction function and sdo.optimize for a more
% detailed description of the function signature.
%

%% Model Evaluation

% Simulate the model.
Simulator.Parameters = P;
Simulator = sim(Simulator);

% Retrieve logged signal data.
SimLog = find(Simulator.LoggedData,get_param('lab12_a','SignalLoggingName'));
Sig_Log = find(SimLog,'Sig');

% Evaluate the design requirements.
F_SignalTracking = evalRequirement(Requirements.SignalTracking,Sig_Log.Values);

%% Return Values.
%
% Collect the evaluated design requirement values in a structure to
% return to the optimization solver.
Vals.F = F_SignalTracking;
end

function Data = getData(DataID, t, y)
%GETDATA
%
% Helper function to store data used by responseOptimization_lab12_a.
%
% The input, DataID, specifies the name of the data to retrieve. The output,
% Data, contains the requested data.
%

switch DataID
    case 'SignalTracking_ReferenceSignal'
        Data = timeseries(y,t);
    case 'SignalTracking_Weights'
        Data = [1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1;  ...
            1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1; 1];
end
end
