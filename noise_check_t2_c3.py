import random, math
from math import comb
class binom:
    @staticmethod
    def pmf(k,n,p): return comb(n,k)*p**k*(1-p)**(n-k)
    @staticmethod
    def cdf(k,n,p): return sum(binom.pmf(i,n,p) for i in range(k+1))
def _bis(f,lo=0.0,hi=1.0):
    for _ in range(60):
        m=(lo+hi)/2
        if f(m): hi=m
        else: lo=m
    return (lo+hi)/2
def cp(k,n,a=0.05):
    lo=0 if k==0 else _bis(lambda p: 1-binom.cdf(k-1,n,p)>=a/2)
    hi=1 if k==n else _bis(lambda p: binom.cdf(k,n,p)<=a/2)
    return lo,hi
print("== t2: closure 'models guessed' fires although model off by d (n per task, 2 solved tasks, same direction)")
for n in (10,12,15,20):
  row=[]
  for f,d in ((0.5,0.2),(0.5,0.3),(0.3,0.2),(0.7,-0.2)):
    p=f+d; q=sum(binom.pmf(k,n,p) for k in range(n+1) if cp(k,n)[0]<=f<=cp(k,n)[1])
    row.append(f"f{f}/d{d:+}: {q**2:.2f}")
  print(n,"  ".join(row))
print("== t2: model counted as miss on one solved task though exact (f=p)")
for n in (10,15,20):
  print(n,[round(sum(binom.pmf(k,n,f) for k in range(n+1) if not cp(k,n)[0]<=f<=cp(k,n)[1]),3) for f in (0.3,0.5,0.7)])
print("== t2: swarm false alarms >1/3 (m causes reported)")
for m in (3,4,6,9,12):
  a=[round(sum(binom.pmf(k,m,e) for k in range(m+1) if k/m>1/3),2) for e in (0.15,0.25,0.45)]
  print(m,"true e=.15/.25/.45 -> P(>1/3):",a)
# c3
print("== c3: B 'better' (>=30% fewer errors, A>=4) when B no better; decisions per arm N, error rate p")
R=random.Random(1); T=40000
for N in (12,16,24):
  for p in (0.2,0.3,0.4):
    fb=und=0
    for _ in range(T):
      a=sum(R.random()<p for _ in range(N)); b=sum(R.random()<p for _ in range(N))
      if a<4: und+=1
      elif b<=0.7*a: fb+=1
    pw=0
    for _ in range(T//4):
      a=sum(R.random()<p for _ in range(N)); b=sum(R.random()<p*0.6 for _ in range(N))
      if a>=4 and b<=0.7*a: pw+=1
    print(f"N{N} p{p}: false 'better' {fb/T:.2f}, undecided {und/T:.2f}, power if B truly -40%: {pw/(T//4):.2f}")
print("== c3: confidence +0.5 (1-5 scale, sd 1.0) with no true difference, N ratings per arm")
for N in (8,12,16,24):
  c=0
  for _ in range(T):
    ma=sum(min(5,max(1,round(R.gauss(3.5,1)))) for _ in range(N))/N
    mb=sum(min(5,max(1,round(R.gauss(3.5,1)))) for _ in range(N))/N
    c+= mb-ma>=0.5
  print(N, round(c/T,3))
print("== c3: refuted >=2 by chance, M claims, refute rate r")
for M in (8,16,24):
  print(M,[round(1-binom.cdf(1,M,r),2) for r in (0.0,0.03,0.06,0.1)])

# --- added 23.10 after observer: t2 "better than bare model", route (a) only ---
# Null: one model forecasts exactly (true share = forecast f on every task).
# "Better" needs that model to miss (forecast outside 95% CP interval) on >=2 solved tasks.
# Route (b) (missing 2 of 3 cause classes) and the swarm false-alarm veto are NOT modelled.
print("== t2: 'better' via route (a) although one model is exact; k solved tasks, n answers each")
def q_miss(n,f): return sum(binom.pmf(k,n,f) for k in range(n+1) if not cp(k,n)[0]<=f<=cp(k,n)[1])
for n in (10,15,20):
  row=[]
  for f in (0.3,0.5,0.7):
    q=q_miss(n,f)
    row.append(f"f{f}: "+" ".join(f"k{k}={1-sum(comb(k,j)*q**j*(1-q)**(k-j) for j in range(2)):.4f}" for k in (2,4,6)))
  print(n,"  |  ".join(row))
