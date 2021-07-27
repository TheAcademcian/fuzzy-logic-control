"""
FLC: Speed control of a vehicle
Let two fuzzy inputs (speed difference (SD) and acceleration (A)) and one fuzzy
output throttle control (TC) be there.

X: Universe of discourse [0,240]
Partitions: 
    NL: Open left MF (a = 30, b = 60) 
    NM: Traingular(a = 30, b = 60, c = 90)
    NS: Traingular(a = 60, b = 90, c = 120)
    ZE: Traingular(a = 90, b = 120, c = 150)
    PS: Traingular(a = 120, b = 150, c = 180)
    PM: Traingular(a = 150, b = 180, c = 210)
    PL: Open right (a = 180, b = 210) 
    
Rules
R1: if SD is NL and A is ZE then TC is PL
R2: if SD is ZE and A is NL then TC is PL
R3: if SD is NM and A is ZE then TC is PM
R4: if SD is NS and A is PS then TC is PS
R5: if SD is PS and A is NS then TC is NS
R6: if SD is PL and A is ZE then TC is NL
R7: if SD is ZE and A is NS then TC is PS
R8: if SD is ZE and A is NM then TC is PM
"""

import numpy as np
Speed = 120
Acceleration = 125

print("The speed input is: ", Speed)
print("The Acceleration input is: ", Acceleration)
print("\n")
#Functions for open left-Right fuzzyfication  
def openLeft(x,alpha, beta):
    if x<alpha:
        return 1
    if alpha<x and x<=beta:
        return (beta - x)/(beta - alpha)
    else:
        return 0
    
def openRight(x,alpha, beta):
    if x<alpha:
        return 0
    if alpha<x and x<=beta:
        return (x-alpha)/(beta - alpha)
    else:
        return 0

# Function for traingular fuzzyfication  
def triangular(x,a,b,c):
    return max(min((x-a)/(b-a), (c-x)/(c-b)),0)

#Fuzzy Partition 
def partition(x):
    NL = 0;  NM = 0; NS = 0; ZE = 0; PS = 0; PM = 0; PL = 0
    
    if x> 0 and x<60:
        NL = openLeft(x,30,60)
    if x> 30 and x<90:
        NM = triangular(x,30,60,90)
    if x> 60 and x<120:
        NS = triangular(x,60,90,120)
    if x> 90 and x<150:
        ZE = triangular(x,90,120,150)
    if x> 120 and x<180:
        PS = triangular(x,120,150,180)
    if x> 150 and x<210:
        PM = triangular(x,120,150,180)
    if x> 180 and x<240:
        PL = openRight(x,180,210)
 
    return NL,NM,NS,ZE,PS,PM,PL;

# Getting fuzzy values for all the inputs for all the fuzzy sets
NLSD,NMSD,NSSD,ZESD,PSSD,PMSD,PLSD = partition(Speed)
NLAC,NMAC,NSAC,ZEAC,PSAC,PMAC,PLAC = partition(Acceleration)

# Display the fuzzy values for all fuzzy sets
outPut = [[NLSD,NMSD,NSSD,ZESD,PSSD,PMSD,PLSD],
          [NLAC,NMAC,NSAC,ZEAC,PSAC,PMAC,PLAC]]
print("The fuzzy values of the crisp inputs")
print(["NL","NM","NS","ZE","PS","PM","PLSD"])
print(np.round(outPut,2))

# Rules implementation
def compare(TC1, TC2):
    TC = 0
    if TC1>TC2 and TC1 !=0 and TC2 !=0:
        TC = TC2
    else:
        TC = TC1
    
    if TC1 == 0 and TC2 !=0:
        TC = TC2
        
    if TC2 == 0 and TC1 !=0:
        TC = TC1
        
    return TC


def rule(NLSD,NMSD,NSSD,ZESD,PSSD,PMSD,PLSD,NLAC,NMAC,NSAC,ZEAC,PSAC,PMAC,PLAC):
    PLTC1 = min(NLSD,ZEAC) 
    PLTC2 = min(ZESD,NLAC)
    PLTC = compare(PLTC1, PLTC2)
    
    PMTC1 = min(NMSD,ZEAC)
    PMTC2 = min(ZESD,NMAC)
    PMTC = compare(PMTC1, PMTC2)
    
    PSTC1 = min(NSSD,PSAC)
    PSTC2 = min(ZESD,NSAC)
    PSTC = compare(PSTC1, PSTC2)
    NSTC = min(PSSD,NSAC)
    NLTC = min(PLSD,ZEAC)
    
    return PLTC, PMTC, PSTC, NSTC, NLTC;

PLTC, PMTC, PSTC, NSTC, NLTC = rule(NLSD,NMSD,NSSD,ZESD,PSSD,PMSD,PLSD,NLAC,NMAC,NSAC,ZEAC,PSAC,PMAC,PLAC)

print("\n")
# Display the fuzzy values for all rules
outPutRules = [[PLTC, PMTC, PSTC, NSTC, NLTC ]]
print("The fuzzy output: ")
print(["PLTC", "PMTC", "PSTC", "NSTC", "NLTC"])
print(np.round(outPutRules,2))


# De-fuzzyfication
def areaTR(mu, a,b,c):
    x1 = mu*(b-a) + a
    x2 = c - mu*(c-b)
    d1 = (c-a); d2 = x2-x1
    a = (1/2)*mu*(d1 + d2)
    return a # Returning area

def areaOL(mu, alpha, beta):
    xOL = beta -mu*(beta - alpha)
    return 1/2*mu*(beta+ xOL), beta/2

def areaOR(mu, alpha, beta):
    xOR = (beta - alpha)*mu + alpha
    aOR = (1/2)*mu*((240 - alpha) + (240 -xOR))
    return aOR, (240 - alpha)/2 + alpha

def defuzzyfication(PLTC, PMTC, PSTC, NSTC, NLTC):
    areaPL = 0; areaPM = 0; areaPS = 0; areaNS = 0; areaNL = 0;
    cPL = 0; cPM = 0; cPS = 0; cNS = 0; cNL = 0;

    if PLTC != 0:
        #areaPL, cPL = areaOR(PLTC, 180, 210)
        areaPL, cPL = areaOR(PLTC, 180, 210)
                
    if PMTC != 0:
        areaPM = areaTR(PMTC, 150, 180, 210)
        cPM = 180
    
    if PSTC != 0:
        areaPS = areaTR(PSTC, 120, 150, 180)
        cPS = 150
          
    if NSTC != 0:
        areaNS = areaTR(NSTC, 60, 90, 120)
        cNS = 90
        
    if NLTC !=0:
        areaNL, cNL = areaOL(NLTC, 30, 60)
        
    numerator = areaPL*cPL + areaPM*cPM + areaPS*cPS + areaNS*cNS + areaNL*cNL
    denominator = areaPL + areaPM + areaPS + areaNS + areaNL
    if denominator ==0:
        print("No rules exist to give the result")
        return 0
    else:
        crispOutput = numerator/denominator
        return crispOutput
crispOutputFinal = defuzzyfication(PLTC, PMTC, PSTC, NSTC, NLTC)

if crispOutputFinal !=0:
    print("\nThe crisp TC value is: ", crispOutputFinal)