import numpy as np

from copy import deepcopy

__all__ = ["EXPANSIONS", "QUANTITIES", "SPLITTINGS"]


# -- quantities
QUANTITIES = {
    'global': {
        # quantities for tripple differential Z+jet analysis
        'phiStarEta': {
            'name': 'PhiStarEta', # name as displayed in the root file
            'label': '$\\Phi^{*}_{\\eta}$', # desired label on the axis
            'scale': 'log', # scale of the axis in the plot
            'expected_values': (91.1876,) # position for a marker (optional) (must be iterable!)
        },
        'zpt': {
            'name': 'ZPt',
            'label': '$p_{\\mathrm{T}}^{\\mathrm{Z}}$ / GeV',
            'scale': 'log',
        },
    },
}

_QUANTITY_EXPECTED_VALUES = {
    # used to mark the approximate value of the factorization scale
    # make sure to define a tuple!
    'zpt' : (91.1876,),
}

# define generic LaTeX labels for some quantities
_QUANTITY_LABELS = {
    'phiStarEta' : '$\\Phi^{*}_{\\eta}$',
    'mpf' : 'MPF',
    'ptbalance' : '$p_{\\mathrm{T}}$ balance',
    'alpha' : '$\\alpha$ (=$p_{\\mathrm{T}}^{\\mathrm{jet2}}/p_{\\mathrm{T}}^{\\mathrm{Z}}$)',
    'jet12DeltaR' : '$\\Delta R(\\mathrm{jet1}, \\mathrm{jet2})$',
    'zJet1DeltaR' : '$\\Delta R(\\mathrm{jet1}, \\mathrm{Z})$',
    'jet12DeltaPhi' : '$\\Delta \\phi(\\mathrm{jet1}, \\mathrm{jet2})$',
    'zJet1DeltaPhi' : '$\\Delta \\phi(\\mathrm{jet1}, \\mathrm{Z})$',
    'jet12DeltaEta' : '$\\Delta \\eta(\\mathrm{jet1}, \\mathrm{jet2})$',
    'zJet1DeltaEta' : '$\\Delta \\eta(\\mathrm{jet1}, \\mathrm{Z})$',
    'met' : '$E_{\\mathrm{T}}^{\\mathrm{miss.}}}$ / GeV',
    'metphi' : '$\\phi (E_{\\mathrm{T}}^{\\mathrm{miss.}})$',
    #'npumean' : '$\\langle n_{\\mathrm{PU}} \\rangle$',
    'npumean' : 'Expected pile-up $\\mu$',
    'npv' : '$n_{\\mathrm{PV}}$',
    'zmass' : '$m^{\\mathrm{Z}}$ / GeV',
    'rho' : 'Pile-up density $\\rho$ / GeV',
    'run2016' : 'Run number (2016)',
    'run2017' : 'Run number (2017)',
    'run2018' : 'Run number (2018)',
}

# define generic scale for some quantities
_QUANTITY_SCALES = {
    'phiStarEta' : 'log'
}

# construct labels and scales for some quantities programatically
for _o in ('Z', 'jet1', 'jet2', 'jet3'):
    for _p, _pl, _pu in zip(
        ['pt', 'eta', 'phi'],
        ['p_{\\mathrm{T}}', '\\eta', '\\phi'],
        ['GeV', None, None]):

        _QUANTITY_LABELS[_o.lower()+_p] = "${prop}^{{\\mathrm{{{obj}}}}}${unit}".format(
            obj=_o,
            prop=_pl,
            unit=' / {}'.format(_pu) if _pu is not None else '',
        )

        # log scale x axis on all pt plots
        if _p == 'pt':
            _QUANTITY_SCALES[_o.lower()+_p] = 'log'

    _QUANTITY_LABELS["abs{}eta".format(_o.lower())] =  "$|{}|$".format(_QUANTITY_LABELS[_o.lower()+"eta"][1:-1])


# -- splittings
# bin splittings
_YSTAR_BIN_EDGES = [0., 0.5, 1., 1.5, 2., 2.5]
_YBOOST_BIN_EDGES = [0., 0.5, 1., 1.5, 2., 2.5]

SPLITTINGS = {}

SPLITTINGS['ystar'] = dict({
    "Ys{:-f}".format(_low): dict(ystar=(_low, _high))
    for _low, _high in zip(_YSTAR_BIN_EDGES[:-1], _YSTAR_BIN_EDGES[1:])
})
SPLITTINGS['yboost'] = dict({
    "Yb{:-f}".format(_low): dict(yboost=(_low, _high))
    for _low, _high in zip(_YBOOST_BIN_EDGES[:-1], _YBOOST_BIN_EDGES[1:])
})


# -- samples
# plot style information for samples
_default_plotstyle = dict(color='k', marker='d')
_SAMPLE_PLOTSTYLES = {
    0: dict(color='#ffc0cb', marker='s'),
    1: dict(color='#e11e1e', marker='p'),
    2: dict(color='#7c1010', marker='H'),
    3: dict(color='#d92626', marker='o'),
    4: dict(color='#1e9ce1', marker='^'),
    5: dict(color='#10447c', marker='v'),
    6: dict(color='#4169e1', marker='*'),
    7: dict(color='#8cc90d', marker='<'),
    8: dict(color='#f0b117', marker='>'),
    9: dict(color='#b0861e', marker='P'),
    10: _default_plotstyle
}

SAMPLES = {
    # samples for tripple differential Z+jet analysis
    'zjet': {
        'herwigLO1Jet': {
            'name': 'LHC-LO-Z1JetMerging', # name as in the file name
            'label': 'Hw 7.2 LO+PS Z+0,1jets', # desired label in the plot legend
            'style': _SAMPLE_PLOTSTYLES.get(0, _default_plotstyle) # plot style
        },
        'herwigLO2Jet': {
            'name': 'LHC-LO-Z2JetMerging',
            'label': 'Hw 7.2 LO+PS Z+0,1,2jets',
            'style': _SAMPLE_PLOTSTYLES.get(1, _default_plotstyle)
        },
        'cmsMGPythiaNLO': {
            'name': 'aMCatNLOPythia',
            'label': 'MG+Py NLO+PS Z+0,1,2jets',
            'style': _SAMPLE_PLOTSTYLES.get(2, _default_plotstyle)
        },
    },

    # samples for dijet analysis
    'dijet': {
    },

    # samples for inclusive jet analysis
    'incljet': {
    }
}


# -- expansions
EXPANSIONS = {}

# build basic `quantity` expansion
EXPANSIONS['quantity'] = [
    {
        'name' : _q.get('name', _qn),
        'label' : _q.get('label', _QUANTITY_LABELS.get(_qn, _qn)),
        'scale' : _q.get('scale', _QUANTITY_SCALES.get(_qn, 'linear')),
        'expected_values' : list(_q.get('expected_values', _QUANTITY_EXPECTED_VALUES.get(_qn, ()) )),
    }
    for _qn, _q in QUANTITIES['global'].iteritems()
]

# build basic sample expansion
EXPANSIONS['sample'] = [
    {
        'ident': _sn,
        'name': _s['name'],
        'label': _s['label'],
        'style': _s['style']
    }
    for _sn, _s in SAMPLES['zjet'].iteritems()
]




