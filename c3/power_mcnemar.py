import random
from math import comb
def p_exact(b,c):  # one-sided: B better => c (A wrong,B right) large
    n=b+c
    return sum(comb(n,k) for k in range(c,n+1))/2**n if n else 1.0
R=random.Random(7)
def sim(M,pa,pb,rho=0.5,T=4000):
    hit=0
    for _ in range(T):
        b=c=0
        for _ in range(M):
            # correlated errors: with prob rho shared difficulty
            u=R.random()
            if R.random()<rho: ea=u<pa; eb=u<pb
            else: ea=R.random()<pa; eb=R.random()<pb
            if ea and not eb: c+=1
            elif eb and not ea: b+=1
        hit+= p_exact(b,c)<0.05
    return hit/T
for M in (16,32,48,64,96):
    print(M,"FP(equal .3):",sim(M,.3,.3),"power(.3->.18):",sim(M,.3,.18),"power(.3->.15):",sim(M,.3,.15))
