import roboticstoolbox as rtb
import numpy as np

L1, L2 = 0.3, 0.3
m1, m2 = 5.0, 4.0
m_or, m_om = 1.0, 0.25
mp = m_or + m_om
g = 9.81

# Звенья
link1 = rtb.RevoluteDH(a=L1, alpha=0, d=0, m=m1, r=[L1/2,0,0])
link2 = rtb.RevoluteDH(a=L2, alpha=0, d=0, m=m2, r=[L2/2,0,0])

robot = rtb.DHRobot([link1, link2], name='TwoLink_fixed')
robot.gravity = np.array([0,-g,0])

# Payload на конце второго звена
robot.payload(mp,[L2,0,0])

# Диапазоны углов
q1_range = np.deg2rad(np.linspace(-45,90,40))
q2_range = np.deg2rad(np.linspace(-90,90,40))

# Максимальные статические моменты
max_tau_static = np.zeros(2)
for q1 in q1_range:
    for q2 in q2_range:
        tau = robot.gravload([q1,q2])
        max_tau_static = np.maximum(max_tau_static, np.abs(tau))

print("=== Максимальные СТАТИЧЕСКИЕ моменты ===")
print(f"τ1_max = {max_tau_static[0]:.3f} Н·м")
print(f"τ2_max = {max_tau_static[1]:.3f} Н·м")

# Максимальные динамические моменты
qd = [0.3/L1,0.3/L2]
qdd = [0.5/L1,0.5/L2]

max_tau_dyn = np.zeros(2)
for q1 in q1_range:
    for q2 in q2_range:
        tau = robot.rne([q1,q2], qd, qdd)
        max_tau_dyn = np.maximum(max_tau_dyn, np.abs(tau))

print("=== Максимальные ДИНАМИЧЕСКИЕ моменты ===")
print(f"τ1_max = {max_tau_dyn[0]:.3f} Н·м")
print(f"τ2_max = {max_tau_dyn[1]:.3f} Н·м")
