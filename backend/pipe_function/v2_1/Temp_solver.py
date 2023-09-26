import math
def Temp_solver (Qo, Qw, Qg, oil_density, water_density, gas_density, dL, D_in,dZ,angle,T1,P1,P2):
    T_env= 15.55+273
    Qo=Qo/86400
    Qw=Qw/86400
    Qg=Qg/86400
    T1=T1+273
    Cap_o=2250
    Cap_w=4180
    Cap_g=1000
    h=75
    P1=P1*14.7
    P2=P2*14.7


    Qm=Qo*oil_density+Qw*water_density

    Cap_sm=(Cap_w*Qw*water_density+Cap_o*Qo*oil_density+Cap_g*Qg*gas_density)/Qm

    def H (P):
        H_g = P * ((1.619e-10 * P + 1.412e-6) * P - 0.02734) * 2326
        H_o = 3.36449e-3 * P * 2326
        H_w = (2.9641e-3 / (water_density/1000)) * P * 2326
        H_sm=(H_o*Qo*oil_density+H_w*Qw*water_density+H_g*Qg*gas_density)/Qm
        return H_sm

    A= (math.pi *(D_in+2*dZ)*dL*h)/(2*Qm)

    T=(Cap_sm*T1+H(P1)-H(P2)-9.81*math.sin(angle)*dL-A*T1+2*A*T_env)/(Cap_sm+A)-273

    return T
print(Temp_solver(677,469,0,870,1020,1.029,3130,0.01,0.09,0,58.4,18.6,17.9))