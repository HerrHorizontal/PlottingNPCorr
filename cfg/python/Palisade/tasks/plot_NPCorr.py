
import datetime
import itertools
import os.path

from Karma.PostProcessing.Palisade import (
    ContextValue, LiteralString, PlotProcessor, If, BinOp, Lazy, String,
    LegendHandlerString, LegendHandlerTuple
)

from PlottingNPCorr.cfg.Palisade import EXPANSIONS, SPLITTINGS, QUANTITIES, FONTPROPERTIES, TEXTS

from matplotlib.font_manager import FontProperties


def build_expression(source_type, sample_name, directory_name, quantity_name):
    """
    Convenience function for putting together paths in the input ROOT file.
    :source_type:           
    :directory_name:        Name of the Rivet analysis which generated the histogram or TDirectory name if not generated by Rivet
    :param quantity_name:   Quantity to plot
    :return:                Lazy string of path to object in the input file
    """
    source_type = source_type.strip()
    assert source_type in ('withNP', 'noNP')

    sample_name = sample_name.strip()
    directory_name = directory_name.strip()

    if all(directory_name != _str for _str in ["", None]): 
        return '"{type}_{sample}:{directory}/{quantity}{{split[name]}}"'.format(
            type = source_type,
            sample=sample_name,
            directory=directory_name,
            quantity=quantity_name
            )
    else:
        return '"{type}_{sample}:{quantity}{{split[name]}}"'.format(
            type = source_type,
            sample=sample_name,
            directory=directory_name,
            quantity=quantity_name
            )


LOOKUP_CHANNEL_LABEL = {
    'mm': r'Z$\rightarrow\mathrm{{\bf \mu\mu}}$',
    'ee': r'Z$\rightarrow\mathrm{{\bf ee}}$',
}

LOOKUP_SAMPLE_EXPANSION = {}
for _s in EXPANSIONS['sample']:
    # make samples identifyable by their name and/or identifier
    LOOKUP_SAMPLE_EXPANSION[_s['name']] = _s
    LOOKUP_SAMPLE_EXPANSION[_s['ident']] = _s


# tweak legend
LEGEND_KWARGS = dict(
    loc='upper right',
    # handler for legend entries by type
    handler_map={
        # use bold for strings used as pseudo-legend-entries
        str: LegendHandlerString(fontweight='bold'),
        # merged entries: show side-by-side, more padding
        tuple: LegendHandlerTuple(ndivide=None, pad=6),
    },
)


def get_config(directory_name, channel, sample_names, quantities, split_quantity, basename_fullsim, basename_noNP, file_suffix_fullsim, file_suffix_noNP, output_format, info_labels, upper_label):
    """
    function to create configurations for the plots
    :param directory_name:      Name of the analysis which produced the histograms or identifying prefix
    :param channel:             Lepton channel of the corresponding data
    :param sample_names:        Name of the samples
    :param quantities:          Quantities to plot 
    :param split_quantities:    Quantities for which the data was selected and ordered
    :param basename_fullsim:    prefix for (path to) ROOT files containing histograms from full simulation
    :param basename_noNP:       prefix for (path to) ROOT files containing histograms from simulation with turned-off non-perturbative part
    :param file_suffix_fullsim: suffix of ROOT files containing histograms from full simulation
    :param file_suffix_noNP:    suffix of ROOT files containing histograms with turned-off non-perturbative part
    :param output_format:       format string indicating full path to output plot
    :param info_labels:         labels indicating additional information, shown as annotations in plot
    :param upper_label:         label to use in upper-right corner of plot
    :return:                    Karma config dictionary for plotting in the format described in the [Palisade user doc](https://karma-hep.readthedocs.io/en/latest/parts/palisade/user_guide.html)
    """

    # raise exception if samples specified are unknown
    _unknown_quantities = set(sample_names).difference(LOOKUP_SAMPLE_EXPANSION.keys())
    if _unknown_quantities:
        raise ValueError("Unknown samples: {}".format(', '.join(_unknown_quantities)))

    # raise exception if quantities specified are unknown
    _unknown_quantities = set(quantities).difference(QUANTITIES['global'].keys())
    if _unknown_quantities:
        raise ValueError("Unknown quantities: {}".format(', '.join(_unknown_quantities)))

    # -- construct list of input files and correction level expansion dicts
    _input_files = dict()
    for _sample in sample_names:
        # fullsim: with non-perturbative parts
        _input_file_withNP = os.path.join(
            "{BASENAME_FULLSIM}".format(BASENAME_FULLSIM=basename_fullsim), 
            "{SAMPLE_NAME}{SUFFIX_FULLSIM}.root".format(
                SUFFIX_FULLSIM="_"+str(file_suffix_fullsim) if str(file_suffix_fullsim) else "", 
                SAMPLE_NAME=_sample
            )
        )
        # raise exception if inputfile doesn't exist
        if not os.path.exists(_input_file_withNP):
            raise ValueError("Couldn't find inputfile {} for sample {}".format(_input_file_withNP,_sample))
        _input_files['withNP_{}'.format(_sample)] = _input_file_withNP

        # NP off: non-perturbative parts of simulation turned-off
        _input_file_noNP = os.path.join(
            "{BASENAME_NONP}".format(BASENAME_NONP=basename_noNP),
            "{SAMPLE_NAME}{SUFFIX_NONP}.root".format(
                SUFFIX_NONP="_"+str(file_suffix_noNP), 
                SAMPLE_NAME=_sample
            )
        )
        # raise exception if inputfile doesn't exist
        if not os.path.exists(_input_file_noNP):
            raise ValueError("Couldn't find inputfile {} for sample {}".format(_input_file_noNP,_sample))
        _input_files['noNP_{}'.format(_sample)] = _input_file_noNP

    # -- expansions
    # quantities to plot
    _expansions = {
        'quantity': [
            _q_dict
            for _q_dict in EXPANSIONS['quantity']
            if _q_dict['name'] in quantities
        ]
    }

    # ystar-yboost-bins
    if split_quantity == 'ystar':
        _expansions.update({'split': [
            dict(name=_k,
                 label=r"${}\leq y^{{*}}<{}$".format(_v['ystar'][0], _v['ystar'][1]))
            for _k, _v in SPLITTINGS['ystar'].iteritems()]})
    elif split_quantity == 'yboost':
        _expansions.update({'split': [
            dict(name=_k,
                 label=r"${}\leq y^{{\mathrm{{b}}}}<{}$".format(_v['yboost'][0], _v['yboost'][1]))
            for _k, _v in SPLITTINGS['zpt'].iteritems()]})
    elif split_quantity is None:
        _expansions['split'] = [
            dict(name='',
                 label=r"incl.")
        ]
    elif split_quantity == 'ystar*yboost':
        _expansions.update({'split': [
            dict(name=_k1+_k2,
                 label=(
                     r"${}\leq y^{{\mathrm{{b}}}}<{}$".format(_v2['yboost'][0], _v2['yboost'][1]) + 
                     r", ${}\leq y^{{*}}<{}$".format(_v1['ystar'][0], _v1['ystar'][1])
                 )
            )
            for _k1, _v1 in SPLITTINGS['ystar'].iteritems()
            for _k2, _v2 in SPLITTINGS['yboost'].iteritems()
        ]})
    else:
        raise ValueError('Expansions not implemented for split quantity {}!'.format(split_quantity))

    # append '[name]' to format keys that correspond to above expansion keys
    output_format = output_format.format(
        channel=channel,
        # get other possible replacements from expansions definition
        **{_expansion_key: "{{{0}[name]}}".format(_expansion_key) for _expansion_key in _expansions.keys()}
    )

    # check which samples are requested with their identifier or sample name
    _sample_dicts = [LOOKUP_SAMPLE_EXPANSION[_s] for _s in sample_names]


    return {
        'input_files': _input_files,
        'figures': [
            {
                'filename': output_format,
                'dump_yaml': True,
                'figsize': (6, 6),
                'subplots': [
                    # NP-Corr = Ratio withNP/noNP
                    dict(
                        expression="({})/({})".format(
                                build_expression("withNP", _s.get('name'), directory_name,"{quantity[name]}"),
                                build_expression("noNP", _s.get('name'), directory_name, "{quantity[name]}")
                        ),
                        label=_s.get('label', _s.get('name')), plot_method='errorbar', 
                        color=_s.get('style',dict()).get('color','k'),
                        marker=_s.get('style',dict()).get('marker','d'), marker_style="full", pad=0
                    )
                    for _s in _sample_dicts
                ] + [
                    # Ratio to first sample
                    dict(
                        expression="({})/({})".format(
                            "({})/({})".format(
                                build_expression("withNP", _s.get('name'), directory_name,"{quantity[name]}"),
                                build_expression("noNP", _s.get('name'), directory_name, "{quantity[name]}")
                            ),
                            "({})/({})".format(
                                build_expression("withNP", _sample_dicts[0].get('name'), directory_name,"{quantity[name]}"),
                                build_expression("noNP", _sample_dicts[0].get('name'), directory_name, "{quantity[name]}")
                            )
                        ),
                        label=None, plot_method='errorbar',
                        color=_s.get('style',dict()).get('color','k'),
                        marker=_s.get('style',dict()).get('marker','d'), marker_style="full", pad=1
                    )
                    for _s in _sample_dicts
                ],
                'pad_spec': {
                    'right': 0.95,
                    'bottom': 0.15,
                    'top': 0.925,
                    'hspace': 0.075,
                },
                'pads': [
                    # top pad
                    {
                        'height_share': 3,
                        'x_range': None,
                        'x_scale': '{quantity[scale]}',
                        'y_label': 'non-pert. corr.',
                        # 'y_range' : (1e-3, 1e9),
                        'axvlines': [dict(values=ContextValue('quantity[expected_values]'))],
                        'x_ticklabels': [],
                        'y_scale': 'linear',
                        'legend_kwargs': dict(loc='upper right'),
                    },
                    # ratio pad
                    {
                        'height_share': 1,
                        'x_label': '{quantity[label]}',
                        'x_range': None,
                        'x_scale': '{quantity[scale]}',
                        'y_label': 'Ratio',
                        'y_range': (0.8, 1.2),
                        'axhlines': [dict(values=[1.0])],
                        'axvlines': [dict(values=ContextValue('quantity[expected_values]'))],
                        'y_scale': 'linear',
                        'legend_kwargs': dict(loc='upper right'),
                    },
                ],
                'texts': [
                    dict(TEXTS['bold_label'], xy=(0, 0), xycoords='axes fraction', xytext=(15, 15), textcoords='offset points',
                         text="{split[label]}"),
                    TEXTS["CMS-in-plot-v2"],
                    TEXTS["Preliminary-in-plot-v2"],
                    TEXTS["Z{}".format(channel)],
                    dict(TEXTS['upper_label'], text=upper_label if upper_label is not None else ""),
                ] + [
                    # labels with other information
                    dict(text=_label,
                         xy=(0, 0), xycoords='axes fraction',
                         xytext=(15, 35+15*_i_label), textcoords='offset points')
                    for _i_label, _label in enumerate(reversed(info_labels))
                ],
            },
        ],
        'expansions': _expansions
    }



def cli(argument_parser):
    """
    Command-line interface. Builds on an existing `argparse.ArgumentParser` instance defined in the 
    [Palisade UI](https://github.com/dsavoiu/Karma/blob/529011377989aff37f86bcc6ae7f201bef96f3f8/PostProcessing/python/Palisade/_ui.py).
    :param argument_parser:
    :return:
    """

    # define CLI arguments
    argument_parser.add_argument('-d', '--dirname', 
                                 help="name of the Rivet analysis, which produced the histograms or corresponding TDirectory name in the ROOT files", required=True, metavar="ANALYSISNAME")
    argument_parser.add_argument('-s', '--samples', help="name of the samples, e.g. 'HerwigLOZplus1Jet'", nargs='+', required=True, metavar="SAMPLES")
    argument_parser.add_argument('-c', '--channels', help="name of the (lepton) channel, e.g. 'mm'", nargs='+',
                                 default=['mm', 'ee'], choices=['mm', 'ee'], metavar="CHANNEL")
    argument_parser.add_argument('-q', '--quantities', help="quantities to plot", nargs='+',
                                 choices=QUANTITIES['global'].keys(), metavar="QUANTITIES")
    argument_parser.add_argument('--basename-fullsim', 
                                 help="prefix for (path to) ROOT files containing histograms from full simulation",
                                 required=True,
                                 metavar="DIRNAME_OF_FULLSIM_FILES")
    argument_parser.add_argument('--basename-noNP', 
                                 help="prefix for (path to) ROOT files containing histograms from simulation with turned-off non-perturbative part", 
                                 required=True,
                                 metavar="DIRNAME_OF_NPOFF_FILES")
    argument_parser.add_argument('--suffix_fullsim', help="suffix of the ROOT files containing fullsim histograms", default="")
    argument_parser.add_argument('--suffix-noNP', help="suffix of the ROOT files containing histograms with turned-off non-perturbative part", default="NPoff")
    argument_parser.add_argument('--split-quantity', help='split quantity: ystar, yboost or both',
                                 choices=['ystar', 'yboost', 'ystar*yboost'], default=None)
    # optional parameters
    argument_parser.add_argument('--output-format', help="format string indicating full path to output plot",
                                 default='Plots/{channel}/{split}/{quantity}.png')

    argument_parser.add_argument('--info-labels', help="labels indicating additional information, shown as annotations in plot", default=[], nargs='*')
    argument_parser.add_argument('--upper-label', help="label to use in upper-right corner of plot", default=None)


def run(args):
    """
    palisade run method
    :param args:
    :return:
    """

    if args.output_dir is None:
        args.output_dir = "plots_{}".format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f"))

    for channel in args.channels:
        print "Making plots for channel '{}'...".format(channel)
        _cfg = get_config(
            directory_name=args.dirname,
            channel=channel,
            sample_names=args.samples,
            quantities=args.quantities,
            split_quantity=args.split_quantity,
            basename_fullsim=args.basename_fullsim,
            basename_noNP=args.basename_noNP,
            file_suffix_fullsim=args.suffix_fullsim, 
            file_suffix_noNP=suffix_noNP,
            output_format=args.output_format,
            info_labels=args.info_labels,
            upper_label=args.upper_label)
        p = PlotProcessor(_cfg, output_folder=args.output_dir)
        p.run()
