import json
from pathlib import Path
from typing import Optional
import logging

import plotly.graph_objs

from supercells.config import CUTOFFS_DICT
from pathlib import Path
import pandas as pd


def read_and_check_cutoff_dict(cutoff_dict_path: str) -> Optional[dict]:
    if not cutoff_dict_path:
        logging.warning(f"cutoff_dict_path was not passed, using default params")
        return CUTOFFS_DICT

    try:
        cutoff_dict_path = Path(cutoff_dict_path)
        logging.info(f"Reading cutoff_dict from '{cutoff_dict_path}'")
        with cutoff_dict_path.open("r") as f:
            cutoff_dict = json.load(f)
            if extra_keys := set(cutoff_dict.keys()) - set(CUTOFFS_DICT.keys()):
                logging.error(f"cutoff_dict read from '{cutoff_dict_path}', contains extra keys: {extra_keys}")
                raise Exception
            else:
                return cutoff_dict

    except (TypeError, FileNotFoundError, PermissionError):
        logging.error(f"Could not read '{cutoff_dict_path}', using default cutoff params.")
        return CUTOFFS_DICT


def get_scatterplot_fig(df: pd.DataFrame) -> plotly.graph_objs.Figure:
    pd.options.plotting.backend = "plotly"

    metrics = ["Reads Mapped Confidently to Transcriptome", "Sequencing Saturation"]
    df = df.loc[metrics].T.map(lambda x: float(x.strip("%")) / 100).reset_index()
    df = df.rename({"name": "sample"}, axis=1)

    fig = df.plot.scatter(x="Sequencing Saturation", y="Reads Mapped Confidently to Transcriptome", color="sample")
    fig.add_hline(y=0.6, line_width=3, line_color="red")
    fig.add_vline(x=0.1, line_width=3, line_color="red")
    fig.update_xaxes(range=[0, 1])
    fig.update_yaxes(range=[0, 1])

    fig.update_traces(
        marker=dict(
            size=12,
            line=dict(
                width=2,
                color='DarkSlateGrey'
            )
        ),
        selector=dict(mode='markers')
    )

    fig.update_xaxes(title_font={"size": 20}, tickfont={"size": 20})
    fig.update_yaxes(title_font={"size": 20}, tickfont={"size": 20})

    fig.update_layout(template="plotly_white")

    fig.update_layout(
        xaxis=dict(
            tickmode='array',
            tickvals=[x / 10 for x in range(11)],
            ticktext=[x / 10 for x in range(11)],
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[x / 10 for x in range(11)],
            ticktext=[""] + [(x + 1) / 10 for x in range(10)],
        ),
        font=dict(size=18, color="black"),
        autosize=False,
        width=1900,
        height=800
    )

    return fig
