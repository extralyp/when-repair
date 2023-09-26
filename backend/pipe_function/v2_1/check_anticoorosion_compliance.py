import math
from . import FluidProps as FluidProps


def check_anticoorosion_compliance (muo, Fr, D, n, b, ro_o, sigl): #вязкость нефти, число Фруда, внутренний диаметр, массовая доля воды, расходное газосодержание, плотность нефти, поверхностное натяжение

    ro_w=1000
    D=D/1000
    mu_o_kin = (muo / ro_o) * 1.8
    # print(Fr)

    if Fr <= 0 :
        Fr = 0.000000001

    if muo<= 25 and n<0.3:
        v_cr=math.sqrt(Fr*9.81*D)
        #print('1')
    elif muo<=25 and n>=0.3:
        ro_em=(1-n)*ro_o+n*ro_w
        #print('2')
        if n<0.5:
            ro_mix=ro_em
            mu_mix_kin = 10 ** -6
            #print('2_1')
        else:
            ro_mix=ro_w
            mu_mix_kin = (muo / ro_em) * 1.8
            #print('2_2')


        v_cr=6.69*((D**0.268) * (sigl**0.171) *((math.fabs(ro_w-ro_mix*9.81)**0.366)))/((mu_mix_kin**0.073) * (ro_mix**0.536) *(math.fabs((-10.96)*(b**2)+(9.94*b)+1)**0.659))
    elif muo>25:
        try:
            v_cr=2.44*(((sigl**2 *(ro_w - ro_o)*9.81*(D**0.125))/((ro_o**3) * (mu_o_kin**1.125)))**0.205)*(2.72**(2.22*(b**7.63)))
        except:
            v_cr= 0
        #print('3')
    return v_cr

def Frudo_critical (n,b):
    # print(n, b)
    if b/(1-b)<2.72 and b/(1-b)>0:
        # print(1)
        Fr=0.159/(1-n)**2
    elif b/(1-b)>=2.72 and b/(1-b)<7.38:
        # print(2)
        Fr=0.02*(b/(1-b)**2)/(1-n)**2
    else:
        # print(7.38, "<=",b/(1-b))
        # print(3)
        Fr=(1/(1-n)**2)*((23*b/(1-b))/(1+b/(1-b))-19)
        # Fr=(1/(1-n)**2)*
        # ((23*b/(1-b))
        # /(1+b/(1-b))-19)

    # print(Fr)
    return Fr