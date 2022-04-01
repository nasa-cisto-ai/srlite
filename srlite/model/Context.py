#!/usr/bin/env python
# coding: utf-8
import os
import sys
import argparse  # system libraries
from datetime import datetime
from srlite.model.PlotLib import PlotLib

# -----------------------------------------------------------------------------
# class Context
#
# This class is a serializable context for orchestration.
# -----------------------------------------------------------------------------
class Context(object):

    DIR_TOA = 'toa'
    DIR_CCDC = 'ccdc'
    DIR_CLOUDMASK = 'cloudmask'
    DIR_OUTPUT = 'out_dir'
    LIST_BAND_PAIRS = 'band_pairs_list'

    REGRESSOR_SIMPLE = 'simple'
    REGRESSOR_ROBUST = 'robust'
    REGRESSION_MODEL = 'regressor'

    DEBUG_NONE_VALUE = 0
    DEBUG_TRACE_VALUE = 1
    DEBUG_VIZ_VALUE = 2
    DEBUG_LEVEL = 'debug_level'

    LOG_FLAG = 'log_flag'

    context_dict = {}
    plotLib = None
    debug_level = 0

    # -------------------------------------------------------------------------
    # __init__
    # -------------------------------------------------------------------------
    def __init__(self):

        args = self._getParser()
        # Initialize serializable context for orchestration
        try:
            self.context_dict[Context.DIR_TOA] = str(args.toa_dir)
            self.context_dict[Context.DIR_CCDC] = str(args.ccdc_dir)
            self.context_dict[Context.DIR_CLOUDMASK] = str(args.cloudmask_dir)
            self.context_dict[Context.DIR_OUTPUT] = str(args.out_dir)
            self.context_dict[Context.LIST_BAND_PAIRS] = str(args.band_pairs_list)
            self.context_dict[Context.REGRESSION_MODEL]  = str(args.regressor)
            self.context_dict[Context.DEBUG_LEVEL]  = int(args.debug_level)
            self.context_dict[Context.LOG_FLAG]  = str(args.logbool)
            if eval(self.context_dict[Context.LOG_FLAG]):
                self._create_logfile(self.context_dict[Context.REGRESSION_MODEL],
                                     self.context_dict[Context.DIR_OUTPUT])
            if (int(self.context_dict[Context.DEBUG_LEVEL]) >= int(self.DEBUG_TRACE_VALUE)):
                    print(sys.path)

        except BaseException as err:
            print('Check arguments: ', err)
            sys.exit(1)

        # Initialize serializable context for orchestration
        self.debug_level = int(self.context_dict[Context.DEBUG_LEVEL])
        plotLib = self.plot_lib = PlotLib(self.context_dict[Context.DEBUG_LEVEL])

        # Echo input parameter values
        plotLib.trace(f'Initializing SRLite Regression script with the following parameters')
        plotLib.trace(f'TOA Directory:    {self.context_dict[Context.DIR_TOA]}')
        plotLib.trace(f'CCDC Directory:    {self.context_dict[Context.DIR_CCDC]}')
        plotLib.trace(f'Cloudmask Directory:    {self.context_dict[Context.DIR_CLOUDMASK]}')
        plotLib.trace(f'Output Directory: {self.context_dict[Context.DIR_OUTPUT]}')
        plotLib.trace(f'Band pairs:    {self.context_dict[Context.LIST_BAND_PAIRS]}')
        plotLib.trace(f'Regression Model:    {self.context_dict[Context.REGRESSION_MODEL]}')
        plotLib.trace(f'Log: {self.context_dict[Context.LOG_FLAG]}')

        return

    # -------------------------------------------------------------------------
    # getParser()
    #
    # Print trace debug (cus
    # -------------------------------------------------------------------------
    def _getParser(self):
        """
        :return: argparser object with CLI commands.
        """
        parser = argparse.ArgumentParser()

        parser.add_argument(
            "-toa", "--input-toa-dir", type=str, required=True, dest='toa_dir',
            default=None, help="Specify directory path containing TOA files."
        )
        parser.add_argument(
            "-ccdc", "--input-ccdc-dir", type=str, required=False, dest='ccdc_dir',
            default=None, help="Specify directory path containing CCDC files."
        )
        parser.add_argument(
            "-cloudmask", "--input-cloudmask-dir", type=str, required=True, dest='cloudmask_dir',
            default=None, help="Specify directory path containing Cloudmask files."
        )
        parser.add_argument(
            "-bandpairs", "--input-list-of-band-pairs", type=str, required=False, dest='band_pairs_list',
            default="[['blue_ccdc', 'BAND-B'], ['green_ccdc', 'BAND-G'], ['red_ccdc', 'BAND-R'], ['nir_ccdc', 'BAND-N']]",
            help="Specify list of band pairs to be processed per scene."
        )
        parser.add_argument(
            "-o", "--output-directory", type=str, required=False, dest='out_dir',
            default="./", help="Specify output directory."
        )
        parser.add_argument(
            "--debug", "--debug_level", type=int, required=False, dest='debug_level',
            default=0, help="Specify debug level [0,1,2,3]"
        )
        parser.add_argument(
            "--log", "--log", required=False, dest='logbool',
            action='store_true', help="Set logging."
        )
        parser.add_argument('--regressor',
                            required=False,
                            dest='regressor',
                            default='robust',
                            choices=['simple', 'robust'],
                            help='Choose which regression algorithm to use')

        return parser.parse_args()

    # -------------------------------------------------------------------------
    # getDict()
    #
    # Get context dictionary
    # -------------------------------------------------------------------------
    def getDict(self):
        return self.context_dict

    # -------------------------------------------------------------------------
    # getPlotLib()
    #
    # Get handle to plotting library
    # -------------------------------------------------------------------------
    def getPlotLib(self):
        return self.plot_lib

    # -------------------------------------------------------------------------
    # getPlotLib()
    #
    # Get handle to plotting library
    # -------------------------------------------------------------------------
    def getDebugLevel(self):
        return self.debug_level

    # -------------------------------------------------------------------------
    # create_logfile()
    #
    # Print trace debug (cus
    # -------------------------------------------------------------------------
    def _create_logfile(self, model, logdir='results'):
        """
        :param args: argparser object
        :param logdir: log directory to store log file
        :return: logfile instance, stdour and stderr being logged to file
        """
        logfile = os.path.join(logdir, '{}_log_{}_model.txt'.format(
        datetime.now().strftime("%Y%m%d-%H%M%S"), model))
        print('See ', logfile)
        so = se = open(logfile, 'w')  # open our log file
        sys.stdout = os.fdopen(sys.stdout.fileno(), 'w')  # stdout buffering
        os.dup2(so.fileno(), sys.stdout.fileno())  # redirect to the log file
        os.dup2(se.fileno(), sys.stderr.fileno())
        return logfile
