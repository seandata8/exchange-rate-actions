from pathlib import Path

import matplotlib
import pandas as pd
import requests

matplotlib.use("Agg")
import matplotlib.pyplot as plt

URL = "https://www.bankofcanada.ca/valet/observations/FXUSDCAD/json"
DATA = Path("data")
CSV = DATA / "usdcad.csv"
PNG = DATA / "usdcad_60d.png"

DATA.mkdir(exist_ok=True)

response = requests.get(URL, params={"recent": 60}, timeout=30)
response.raise_for_status()

new = pd.DataFrame(
    [
        {"date": obs["d"], "rate": float(obs["FXUSDCAD"]["v"])}
        for obs in response.json()["observations"]
    ]
)

if CSV.exists():
    new = pd.concat([pd.read_csv(CSV), new])

new = new.drop_duplicates(subset="date", keep="last").sort_values("date")
new.to_csv(CSV, index=False)

recent = new.tail(60).copy()
recent["date"] = pd.to_datetime(recent["date"])

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(recent["date"], recent["rate"])
ax.set_title("USD/CAD, last 60 observations")
ax.set_ylabel("CAD per USD")
fig.autofmt_xdate()
fig.savefig(PNG, dpi=150, bbox_inches="tight")