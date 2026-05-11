function [Optimized_DesignVars,Info] = optimize_current(DesignVars)

open_system('../matlab_models/lab12_a')

if nargin < 1 || isempty(DesignVars)
    DesignVars = sdo.getParameterFromModel('lab12_a','kp');
    DesignVars(1).Minimum = 0;
end

Requirements = struct;
Requirements.StepRespEnvelope = sdo.requirements.StepResponseEnvelope(...
    'FinalValue', 10, ...
    'PercentOvershoot', 5, ...
    'PercentSettling', 0.9999999999999964, ...
    'RiseTime', 0.116, ...
    'SettlingTime', 0.117);


Simulator = sdo.SimulationTest('lab12_a');

Sig_Info = Simulink.SimulationData.SignalLoggingInfo;
Sig_Info.BlockPath = 'lab12_a/backlash';
Sig_Info.LoggingInfo.LoggingName = 'Sig';
Sig_Info.LoggingInfo.NameMode = 1;

Simulator.LoggingInfo.Signals = Sig_Info;

Simulator = setup(Simulator, 'FastRestart', 'off');

SimulatorCleanup = onCleanup(@() restore(Simulator));

optimfcn = @(P) lab12_a_optFcn(P,Simulator,Requirements);

Options = sdo.OptimizeOptions;
Options.Method = 'fmincon';
Options.OptimizedModel = Simulator;

[Optimized_DesignVars,Info] = sdo.optimize(optimfcn,DesignVars,Options);
end

function Vals = lab12_a_optFcn(P,Simulator,Requirements)

Simulator.Parameters = P;
Simulator = sim(Simulator);


SimLog = find(Simulator.LoggedData,get_param('lab12_a','SignalLoggingName'));
Sig_Log = find(SimLog,'Sig');

Cleq_StepRespEnvelope = evalRequirement(Requirements.StepRespEnvelope,Sig_Log.Values);

Vals.Cleq = Cleq_StepRespEnvelope(:);
end