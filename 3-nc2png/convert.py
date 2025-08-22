#!/usr/bin/env python3
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import numpy as np

def main():
    p = argparse.ArgumentParser(description="Converte una variabile NetCDF in PNG")
    p.add_argument("--in",  dest="infile",  required=True, help="File NetCDF di input (anche URL)")
    p.add_argument("--out", dest="outfile", required=True, help="PNG di output")
    p.add_argument("--var", default="va",   help="Nome variabile (default: va)")
    p.add_argument("--time",  type=int, default=0, help="Indice temporale se presente (default: 0)")
    p.add_argument("--level", type=int, default=0, help="Indice di livello/plevel se presente (default: 0)")
    p.add_argument("--step",  type=int, default=10, help="Campionamento spaziale (default: 10)")
    args = p.parse_args()

    ds = Dataset(args.infile, "r")

    if args.var not in ds.variables:
        raise KeyError(f"Variabile '{args.var}' non trovata. Disponibili: {list(ds.variables.keys())}")

    var = ds.variables[args.var]

    # Costruisci slicing: time/plevel → indici; lat/lon → slice(None) poi campionati
    slices = []
    for dim in var.dimensions:
        d = dim.lower()
        if d in ("time", "t"):
            slices.append(args.time)
        elif d in ("plevel", "lev", "level", "depth", "z"):
            slices.append(args.level)
        elif d in ("latitude", "lat", "y"):
            slices.append(slice(None))
        elif d in ("longitude", "lon", "x"):
            slices.append(slice(None))
        else:
            # dimensione sconosciuta: prendi il primo indice
            slices.append(0)

    data = np.array(var[tuple(slices)]).squeeze()

    # Ora data dovrebbe essere almeno 2D: campiona spazialmente l’ultima 2D
    if data.ndim < 2:
        raise ValueError(f"La variabile {args.var} non è 2D dopo lo slicing: shape={data.shape}")
    while data.ndim > 2:
        data = np.array(data[0]).squeeze()

    data = data[::args.step, ::args.step]

    # extent con lat/lon se esistono
    extent = None
    lat_name = next((n for n in ("latitude","lat","y") if n in ds.variables), None)
    lon_name = next((n for n in ("longitude","lon","x") if n in ds.variables), None)
    if lat_name and lon_name:
        lat = ds.variables[lat_name][::args.step]
        lon = ds.variables[lon_name][::args.step]
        try:
            extent = [float(lon.min()), float(lon.max()), float(lat.min()), float(lat.max())]
        except Exception:
            extent = None

    # Plot
    fig = plt.figure(figsize=(10, 10), dpi=150)
    ax = plt.gca()
    im = ax.imshow(data, origin="lower", extent=extent, cmap="viridis", aspect="auto")
    units = getattr(var, "units", "")
    plt.colorbar(im, ax=ax, label=units)
    title = getattr(ds, "title", args.var)
    ax.set_title(title)
    ax.set_xlabel("Longitude" if extent else "X index")
    ax.set_ylabel("Latitude"  if extent else "Y index")

    fig.tight_layout()
    fig.savefig(args.outfile, bbox_inches="tight")
    plt.close(fig)
    ds.close()
    print(f"PNG salvato in {args.outfile}")

if __name__ == "__main__":
    main()
