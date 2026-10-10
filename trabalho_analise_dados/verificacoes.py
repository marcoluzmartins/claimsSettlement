import numpy as np
from scipy import stats
# Tabela 5: Cramér V = sqrt(chi2/(n*min(r-1,c-1))), Abandono binario -> min=1
tab5 = {"Sexo":(0.525,1,0.469,0.042),"Regiao":(1.364,3,0.714,0.039),"Canal":(0.418,2,0.811,0.037),
        "GrupoEtario":(2.263,2,0.323,0.087),"Plano":(0.013,2,0.994,0.007),"MetodoPag":(7.234,3,0.065,0.155),
        "Fidelizacao":(2.904,1,0.088,0.098),"Perfil":(4.828,2,0.090,0.127)}
print("== Tabela 5 (n=300) ==")
for k,(c,df,p,v) in tab5.items():
    print(f"{k:12s} chi2={c:6.3f} df={df} p_rep={p:.3f} p_calc={stats.chi2.sf(c,df):.3f}  V_rep={v:.3f} V_calc={np.sqrt(c/300):.3f}")
# PCA
ev = np.array([3.846,2.211,0.829,0.535,0.449,0.396,0.325,0.299,0.143])
rep = np.array([42.58,24.48,9.18,5.93,4.99,4.40,3.61,3.32,1.59]); cum=np.array([42.58,67.06,76.23,82.16,87.15,91.55,95.16,98.48,100.0])
print("\n== PCA ==")
print("soma eigenvalues", ev.sum(), "(deveria ser 9)")
print("ev/9 %", np.round(ev/9*100,2))
print("var% reportada", rep, "soma", rep.sum())
print("cum reportada vs cumsum(ev/9):", np.round(np.cumsum(ev/9)*100,2))
n=280;p=9
lnR=np.log(ev).sum(); chi=-(n-1-(2*p+5)/6)*lnR
print("Bartlett recalc (a partir dos ev):", round(chi,1), "df", p*(p-1)//2, "reportado 1295.599")
L = np.array([[0.231,-0.467],[0.437,0.148],[0.298,-0.389],[0.458,0.115],[0.394,-0.129],[-0.111,0.575],[0.285,0.385],[0.413,0.134],[-0.194,-0.288]])
print("norma colunas (eigenvectores?)", (L**2).sum(0), "produto interno", (L[:,0]*L[:,1]).sum())
names=["Idade","Rend","Antig","Desp","Visitas","%dig","Satisf","Prod","Reclam"]
corrload = L*np.sqrt(ev[:2])
for nm,a,b in zip(names,corrload[:,0],corrload[:,1]): print(f"  {nm:8s} corr c/ CP1={a:6.3f} CP2={b:6.3f}")
# Clusters
print("\n== Clusters ==")
sz=np.array([62,83,135]); rate=np.array([8.1,9.6,23.0])/100
ch=np.round(sz*rate); print("churners por cluster (n*taxa):", sz*rate, "->", ch, "total", ch.sum(), "de 280 =", round(ch.sum()/280*100,1),"%")
print("churners fora da amostra completa:", 50-ch.sum(), "de 20 ->", (50-ch.sum())/20*100,"%")
obs=np.array([[5,57],[8,75],[31,104]]); chi2,pv,df,_=stats.chi2_contingency(obs,correction=False)
print("chi2 cluster x abandono", round(chi2,3), "p", round(pv,4), "V", round(np.sqrt(chi2/280),3))
tab=np.array([[6,14],[44,236]]); print("Fisher excluidos vs completos (abandono):", stats.fisher_exact(tab))
# Wilson CI
def wilson(x,n,z=1.96):
    ph=x/n; d=1+z*z/n; c=(ph+z*z/(2*n))/d; h=z*np.sqrt(ph*(1-ph)/n+z*z/(4*n*n))/d; return c-h,c+h
for i,(x,nn) in enumerate(zip(ch,sz),1): print("cluster",i,x,nn,[round(v*100,1) for v in wilson(x,nn)])
# consistencia medias ponderadas
T10=np.array([[47.2,3647.70,6.51,150.44,7.03,53.49,8.48,5.08,0.89],[33.4,1769.36,2.87,59.96,3.18,86.07,7.82,2.54,1.01],[47.9,1653.70,5.65,59.69,4.41,35.30,6.36,2.40,2.07]])
print("media ponderada clusters:", np.round((sz[:,None]*T10).sum(0)/280,2))
# outliers z
print("z max rendimento", (5544.20-2133.97)/912.83, " z max despesa", (241.03-80.71)/43.69, "z max idade",(74.6-43.46)/10.68)
print("Despesa/Rendimento skew indicador media-mediana:",2133.97-1796.42, 80.71-62.67)
