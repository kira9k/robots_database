function [Optimized_DesignVars,Info] = non_linear_optimize(DesignVars, overshoot, settlingTime)

load_system('../matlab_models/lab12_a');

if nargin < 3 || isempty(DesignVars)
    DesignVars = sdo.getParameterFromModel('lab12_a','kp');
end

Requirements = struct;
Requirements.StepRespEnvelope = sdo.requirements.StepResponseEnvelope(...
    'PercentOvershoot', overshoot, ...
    'RiseTime', settlingTime-0.001, ...
    'SettlingTime', settlingTime);

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
Options.OptimizedModel = Simulator;
Options.MethodOptions.MaxIterations = 50;
Options.BackupFilename = fullfile(pwd,'lab12_a__BackupfileSDO.mat');

[Optimized_DesignVars,Info] = sdo.optimize(optimfcn,DesignVars,Options);

sdo.setValueInModel('lab12_a',Optimized_DesignVars);
end

function Vals = lab12_a_optFcn(P,Simulator,Requirements)

Simulator.Parameters = P;
Simulator = sim(Simulator);


SimLog = find(Simulator.LoggedData,get_param('lab12_a','SignalLoggingName'));
Sig_Log = find(SimLog,'Sig');

Cleq_StepRespEnvelope = evalRequirement(Requirements.StepRespEnvelope,Sig_Log.Values);


Vals.Cleq = Cleq_StepRespEnvelope(:);
end
