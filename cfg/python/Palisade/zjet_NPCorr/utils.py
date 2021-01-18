"""Various helper tools, variables and utilities"""

from matplotlib.font_manager import FontProperties


__all__ = ["FONTPROPERTIES", "TEXTS"]


FONTPROPERTIES = dict(
    big_bold=FontProperties(
        weight='bold',
        family='Nimbus Sans',
        size=18,
    ),
    big_italic=FontProperties(
        style='italic',
        family='Nimbus Sans',
        size=16,
    ),
    bold=FontProperties(
        weight='bold',
        family='Nimbus Sans',
        size=12,
    ),
    italic=FontProperties(
        style='italic',
        family='Nimbus Sans',
        size=14,
    ),
    small=FontProperties(
        family='Nimbus Sans',
        size=12,
    ),
)

TEXTS = {
    "CMS": dict(
        text=r"CMS",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(0, 5), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_bold']
    ),
    "Preliminary": dict(
        text=r"Preliminary",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(45, 4), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_italic']
    ),
    "Simulation": dict(
        text=r"Simulation",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(45, 4), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_italic']
    ),
    "Simulation Preliminary": dict(
        text=r"Simulation Preliminary",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(45, 4), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_italic']
    ),
    "CMS-in-plot": dict(
        text=r"CMS",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(15, -35), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_bold']
    ),
    "Preliminary-in-plot": dict(
        text=r"Preliminary",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(65, -35), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_italic']
    ),
    "CMS-in-plot-v2": dict(
        text=r"CMS",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(15, -25), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_bold']
    ),
    "Preliminary-in-plot-v2": dict(
        text=r"Preliminary",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(15, -45), textcoords='offset points',
        fontproperties=FONTPROPERTIES['big_italic']
    ),
    "Zmm": dict(
        text=r"Z$\rightarrow\mathrm{{\bf \mu\mu}}$",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(0, 5), textcoords='offset points',
        fontproperties=FONTPROPERTIES['bold']
    ),
    "Zee": dict(
        text=r"Z$\rightarrow\mathrm{{\bf ee}}$",
        xy=(0, 1), xycoords='axes fraction',
        xytext=(0, 5), textcoords='offset points',
        fontproperties=FONTPROPERTIES['bold']
    ),
    "upper_label": dict(
        xy=(1, 1), xycoords='axes fraction',
        xytext=(0, 5), textcoords='offset points',
        ha='right',
    ),
    "bold_label": dict(
        xy=(0, 0), xycoords='axes fraction',
        xytext=(15, 15), textcoords='offset points',
        fontproperties=FONTPROPERTIES['bold'],
        ha='left',
    ),
    "side_label": dict(
        xy=(1, 0), xycoords='axes fraction',
        xytext=(5, 4), textcoords='offset points',
        va='bottom', ha='left', rotation=90
    ),

}
