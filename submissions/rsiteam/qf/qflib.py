"""qflib - small, vetted quant-finance helpers (numpy/pandas/scipy only, offline).

Usage inside a task container:

    import sys; sys.path.insert(0, "/harbor/skills/stbench-skill")
    import qflib as q

Every function states its convention in the docstring. If the task text defines
a convention differently (sign of VaR, ddof, annualisation factor, lag
direction, day count), follow the task text and pass the matching argument.
"""

from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

try:  # scipy is present in the finance image; keep a fallback anyway
    from scipy.stats import norm as _norm

    def _Phi(x):
        return _norm.cdf(x)

    def _phi(x):
        return _norm.pdf(x)
except Exception:  # pragma: no cover
    def _Phi(x):
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    def _phi(x):
        return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


# ----------------------------------------------------------------- returns

def log_returns(prices):
    """ln(P_t / P_{t-1}). First row dropped. Works on Series or DataFrame."""
    return np.log(prices / prices.shift(1)).iloc[1:]


def simple_returns(prices):
    """P_t / P_{t-1} - 1. First row dropped."""
    return (prices / prices.shift(1) - 1.0).iloc[1:]


def annualized_vol(returns, periods_per_year=252, ddof=1):
    """Sample std (ddof=1) * sqrt(periods_per_year). 252 for daily equity data."""
    return returns.std(ddof=ddof) * math.sqrt(periods_per_year)


def annualized_return(returns, periods_per_year=252, geometric=True):
    """Geometric: prod(1+r)^(N/n) - 1. Arithmetic: mean(r) * N."""
    r = np.asarray(returns, dtype=float)
    if geometric:
        return float(np.prod(1.0 + r) ** (periods_per_year / len(r)) - 1.0)
    return float(r.mean() * periods_per_year)


def sharpe(returns, rf_per_period=0.0, periods_per_year=252, ddof=1):
    """mean(r - rf) / std(r - rf, ddof) * sqrt(N)."""
    ex = np.asarray(returns, dtype=float) - rf_per_period
    sd = ex.std(ddof=ddof)
    return float(ex.mean() / sd * math.sqrt(periods_per_year)) if sd > 0 else float("nan")


def max_drawdown(prices_or_index):
    """Largest peak-to-trough drop as a NEGATIVE fraction (e.g. -0.35)."""
    p = pd.Series(prices_or_index, dtype=float)
    dd = p / p.cummax() - 1.0
    return float(dd.min())


# -------------------------------------------------------------- risk

def historical_var_es(returns, confidence=0.95, positive_loss=True):
    """Historical VaR and ES at `confidence` (e.g. 0.95).
    positive_loss=True -> both reported as positive loss numbers.
    VaR = -(quantile of returns at 1-confidence); ES = -(mean of returns <= that quantile)."""
    r = np.asarray(returns, dtype=float)
    r = r[~np.isnan(r)]
    q = np.quantile(r, 1.0 - confidence)
    tail = r[r <= q]
    var, es = -q, -tail.mean()
    if not positive_loss:
        var, es = -var, -es
    return float(var), float(es)


def parametric_var(mean, std, confidence=0.95, positive_loss=True):
    """Normal VaR = -(mean + z_{1-c} * std). z_{0.05} = -1.6449."""
    from scipy.stats import norm
    v = -(mean + norm.ppf(1.0 - confidence) * std)
    return float(v if positive_loss else -v)


def ewma_cov(returns, lam=0.94, demean=False):
    """RiskMetrics EWMA covariance: S_t = lam*S_{t-1} + (1-lam)*outer(r_{t-1}, r_{t-1}),
    seeded with the sample covariance of the first row(s). Returns the final matrix (k x k).
    Uses RAW returns unless demean=True."""
    x = np.asarray(returns, dtype=float)
    if x.ndim == 1:
        x = x[:, None]
    if demean:
        x = x - x.mean(axis=0)
    s = np.outer(x[0], x[0])
    for row in x[1:]:
        s = lam * s + (1.0 - lam) * np.outer(row, row)
    return s


def ewma_vol_series(returns, lam=0.94):
    """Per-period EWMA volatility path sigma_t (same length as returns), sigma_0^2 = r_0^2."""
    r = np.asarray(returns, dtype=float)
    v = np.empty_like(r)
    v[0] = r[0] ** 2
    for t in range(1, len(r)):
        v[t] = lam * v[t - 1] + (1.0 - lam) * r[t - 1] ** 2
    return np.sqrt(v)


def hhi(weights):
    """Herfindahl index = sum(w^2). Effective number of names = 1/HHI."""
    w = np.asarray(weights, dtype=float)
    return float(np.sum(w * w))


def turnover(w_new, w_old):
    """One-way turnover = 0.5 * sum |w_new - w_old|."""
    return float(0.5 * np.abs(np.asarray(w_new) - np.asarray(w_old)).sum())


# ----------------------------------------------------- correlation / lead-lag

def lagged_corr(x, y, lag):
    """Pearson corr(x_t, y_{t+lag}). Positive lag = x LEADS y by `lag` periods.
    Aligns on index if Series, else on position."""
    xs, ys = pd.Series(x).reset_index(drop=True), pd.Series(y).reset_index(drop=True)
    if lag >= 0:
        a, b = xs.iloc[: len(xs) - lag] if lag else xs, ys.iloc[lag:]
    else:
        a, b = xs.iloc[-lag:], ys.iloc[: len(ys) + lag]
    a, b = a.reset_index(drop=True), b.reset_index(drop=True)
    return float(np.corrcoef(a, b)[0, 1])


def lead_lag_table(x, y, max_lag):
    """DataFrame with columns lag, corr for lag in [-max_lag, max_lag]; lag>0 means x leads y."""
    rows = [(k, lagged_corr(x, y, k)) for k in range(-max_lag, max_lag + 1)]
    return pd.DataFrame(rows, columns=["lag", "corr"])


def fisher_z_pvalue(r, n):
    """Two-sided p-value for corr r from n pairs via Fisher z."""
    r = max(min(float(r), 0.999999), -0.999999)
    z = 0.5 * math.log((1 + r) / (1 - r)) * math.sqrt(max(n - 3, 1))
    return float(2.0 * (1.0 - _Phi(abs(z))))


def kendall_to_copula(tau, family):
    """Kendall tau -> copula parameter. gaussian/t: rho = sin(pi*tau/2);
    clayton: theta = 2tau/(1-tau); gumbel: theta = 1/(1-tau); frank: numeric (not provided)."""
    f = family.lower()
    if f in ("gaussian", "normal", "t", "student", "student_t"):
        return math.sin(math.pi * tau / 2.0)
    if f == "clayton":
        return 2.0 * tau / (1.0 - tau)
    if f == "gumbel":
        return 1.0 / (1.0 - tau)
    raise ValueError(f"unknown copula family {family!r}")


# --------------------------------------------------------------- options

def bs_price(S, K, T, r, sigma, q=0.0, kind="call"):
    """Black-Scholes(-Merton) European price with continuous dividend yield q."""
    if T <= 0 or sigma <= 0:
        return float(max(S - K, 0.0) if kind == "call" else max(K - S, 0.0))
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    if kind == "call":
        return float(S * math.exp(-q * T) * _Phi(d1) - K * math.exp(-r * T) * _Phi(d2))
    return float(K * math.exp(-r * T) * _Phi(-d2) - S * math.exp(-q * T) * _Phi(-d1))


def bs_greeks(S, K, T, r, sigma, q=0.0, kind="call"):
    """dict(delta, gamma, vega, theta, rho). vega per 1.0 of vol (divide by 100 for per 1%),
    theta per year (divide by 365 for per day)."""
    sq = math.sqrt(T)
    d1 = (math.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sq)
    d2 = d1 - sigma * sq
    disc_r, disc_q = math.exp(-r * T), math.exp(-q * T)
    gamma = disc_q * _phi(d1) / (S * sigma * sq)
    vega = S * disc_q * _phi(d1) * sq
    if kind == "call":
        delta = disc_q * _Phi(d1)
        theta = (-S * disc_q * _phi(d1) * sigma / (2 * sq) - r * K * disc_r * _Phi(d2) + q * S * disc_q * _Phi(d1))
        rho = K * T * disc_r * _Phi(d2)
    else:
        delta = -disc_q * _Phi(-d1)
        theta = (-S * disc_q * _phi(d1) * sigma / (2 * sq) + r * K * disc_r * _Phi(-d2) - q * S * disc_q * _Phi(-d1))
        rho = -K * T * disc_r * _Phi(-d2)
    return {"delta": float(delta), "gamma": float(gamma), "vega": float(vega), "theta": float(theta), "rho": float(rho)}


def bs_implied_vol(price, S, K, T, r, q=0.0, kind="call", lo=1e-6, hi=5.0, tol=1e-10):
    """Implied vol by bisection on bs_price. Returns nan if price is outside no-arbitrage bounds."""
    f_lo, f_hi = bs_price(S, K, T, r, lo, q, kind) - price, bs_price(S, K, T, r, hi, q, kind) - price
    if f_lo * f_hi > 0:
        return float("nan")
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        f_mid = bs_price(S, K, T, r, mid, q, kind) - price
        if abs(f_mid) < tol:
            return float(mid)
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return float(0.5 * (lo + hi))


def first_passage_prob_bm(level, mu, sigma, T):
    """P(drifted Brownian motion X_t = mu*t + sigma*W_t hits `level` > 0 by time T).
    = Phi((-a + mu T)/(sigma sqrt T)) + exp(2 mu a / sigma^2) Phi((-a - mu T)/(sigma sqrt T))."""
    a, s = float(level), sigma * math.sqrt(T)
    return float(_Phi((-a + mu * T) / s) + math.exp(2.0 * mu * a / sigma**2) * _Phi((-a - mu * T) / s))


def first_passage_prob_gbm(S0, barrier, mu, sigma, T):
    """P(GBM with drift mu, vol sigma hits `barrier` by T). Uses log-space BM with drift mu - sigma^2/2.
    Works for barrier above or below S0."""
    a = math.log(barrier / S0)
    nu = mu - 0.5 * sigma**2
    if a > 0:
        return first_passage_prob_bm(a, nu, sigma, T)
    return first_passage_prob_bm(-a, -nu, sigma, T)


def expected_first_passage_time_bm(level, mu):
    """E[tau] for drifted BM hitting level a>0 with drift mu>0: a/mu (infinite if mu<=0)."""
    return float(level / mu) if mu > 0 else float("inf")


def simulate_gbm_paths(S0, mu, sigma, T, steps, n_paths, seed=42, antithetic=False):
    """(n_paths, steps+1) GBM paths, exact discretisation, fixed seed (np.random.default_rng)."""
    rng = np.random.default_rng(seed)
    dt = T / steps
    z = rng.standard_normal((n_paths // 2 if antithetic else n_paths, steps))
    if antithetic:
        z = np.vstack([z, -z])
    inc = (mu - 0.5 * sigma**2) * dt + sigma * math.sqrt(dt) * z
    paths = np.empty((z.shape[0], steps + 1))
    paths[:, 0] = S0
    paths[:, 1:] = S0 * np.exp(np.cumsum(inc, axis=1))
    return paths


# ------------------------------------------------------- rates / curves

def nelson_siegel(t, beta0, beta1, beta2, tau):
    """NS yield at maturity t: b0 + b1*(1-e^{-t/tau})/(t/tau) + b2*((1-e^{-t/tau})/(t/tau) - e^{-t/tau})."""
    t = np.asarray(t, dtype=float)
    x = t / tau
    f1 = (1.0 - np.exp(-x)) / x
    return beta0 + beta1 * f1 + beta2 * (f1 - np.exp(-x))


def discount_factor(rate, t, compounding="continuous"):
    """DF for zero rate. continuous: e^{-rt}; annual: (1+r)^-t; simple: 1/(1+rt)."""
    if compounding == "continuous":
        return float(math.exp(-rate * t))
    if compounding == "annual":
        return float((1.0 + rate) ** (-t))
    if compounding == "simple":
        return float(1.0 / (1.0 + rate * t))
    raise ValueError(compounding)


# ---------------------------------------------------------- utilities

def bootstrap_ci(values, stat=np.mean, n_boot=1000, ci=0.95, seed=42):
    """Percentile bootstrap CI (lo, hi) of `stat` over `values`, fixed seed."""
    rng = np.random.default_rng(seed)
    v = np.asarray(values, dtype=float)
    stats = np.array([stat(rng.choice(v, size=len(v), replace=True)) for _ in range(n_boot)])
    a = (1.0 - ci) / 2.0
    return float(np.quantile(stats, a)), float(np.quantile(stats, 1.0 - a))


def to_jsonable(obj):
    """Recursively convert numpy / pandas scalars, NaN and inf so json.dump works.
    NaN/inf -> None (change if the task wants a number)."""
    if isinstance(obj, dict):
        return {str(k): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        f = float(obj)
        return None if (math.isnan(f) or math.isinf(f)) else f
    if isinstance(obj, (pd.Timestamp,)):
        return obj.isoformat()
    if isinstance(obj, np.ndarray):
        return [to_jsonable(v) for v in obj.tolist()]
    return obj


def write_json(path, data, indent=2):
    """json.dump with to_jsonable applied; creates parent dirs."""
    import os
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(to_jsonable(data), fh, indent=indent)


def write_csv(path, df, columns=None):
    """DataFrame to CSV without index, reordering/selecting `columns` if given; creates parent dirs."""
    import os
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    if columns is not None:
        df = df.reindex(columns=list(columns))
    df.to_csv(path, index=False)


__all__ = [n for n in dir() if not n.startswith("_")]
