"""Small, reproducible educational experiment. See README for limitations."""
import json
from pathlib import Path
import numpy as np

def save(result, output):
    Path(output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result

from scipy.stats import ks_2samp

def fit_bins(reference,n=10):
    cuts=np.unique(np.quantile(reference,np.linspace(0,1,n+1)))
    return np.r_[-np.inf,cuts[1:-1],np.inf]
def psi(reference,current,bins,eps=1e-6):
    a=np.histogram(reference,bins=bins)[0].astype(float); b=np.histogram(current,bins=bins)[0].astype(float)
    a=np.clip(a/a.sum(),eps,None); b=np.clip(b/b.sum(),eps,None)
    a/=a.sum(); b/=b.sum()
    return float(np.sum((b-a)*np.log(b/a)))
def run(output="results.json"):
    rng=np.random.default_rng(42); reference=rng.normal(0,1,2000)
    groups={"stable":rng.normal(0,1,2000),"mean_shift":rng.normal(1,1,2000),"scale_shift":rng.normal(0,1.8,2000)}
    bins=fit_bins(reference); rows={}
    for name,current in groups.items():
        ks=ks_2samp(reference,current)
        rows[name]={"psi":psi(reference,current,bins),"ks_statistic":float(ks.statistic),"ks_pvalue":float(ks.pvalue),"current_mean":float(current.mean()),"current_std":float(current.std())}
    return save({"seed":42,"reference_rows":len(reference),"reference_mean":float(reference.mean()),"bins_source":"reference-only quantiles with infinite outer edges","comparison_rows_each":2000,"features":rows},output)

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
