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

    # Directories
    DIR_TOA = 'dir_toa'
    DIR_TARGET = 'dir_target'
    DIR_CLOUDMASK = 'dir_cloudmask'
    DIR_OUTPUT = 'dir_out'
    DIR_WARP = 'dir_warp'

    # File names
    FN_DEST = 'fn_dest'
    FN_SRC = 'fn_src'
    FN_WARP = 'fn_warp'
    FN_LIST = 'fn_list'
    DS_LIST = 'ds_list'
    MA_LIST = 'ma_list'
    PRED_LIST = 'pred_list'

    FN_TOA = 'fn_toa'
    FN_TOA_DOWNSCALE = 'fn_toa_downscale'
    FN_TARGET = 'fn_target'
    FN_TARGET_DOWNSCALE = 'fn_target_downscale'
    FN_CLOUDMASK = 'fn_cloudmask'
    FN_CLOUDMASK_DOWNSCALE = 'fn_cloudmask_downscale'
    FN_PREFIX = 'fn_prefix'
    FN_COG = 'fn_cog'
    FN_SUFFIX = 'fn_suffix'

    # File name suffixes
    FN_TOA_SUFFIX = '-toa.tif'
    FN_TOA_DOWNSCALE_SUFFIX = '-toa-30m.tif'
#    FN_TARGET_SUFFIX = '.tif'
    FN_TARGET_SUFFIX = '-target.tif'
    FN_TARGET_DOWNSCALE_SUFFIX = '-target-30m.tif'
    FN_CLOUDMASK_SUFFIX = '-toa.clouds.tif'
    FN_CLOUDMASK_DOWNSCALE_SUFFIX = '-toa-clouds-30m.tif'
    FN_CLOUDMASK_WARP_SUFFIX = '-toa_pred-warp.tif'
    FN_SRLITE_NONCOG_SUFFIX = '-noncog.tif'
    FN_SRLITE_SUFFIX = '-sr-02m.tif'

    # Band pairs
    LIST_BAND_PAIRS = 'list_band_pairs'
    LIST_BAND_PAIR_INDICES = 'list_band_pairs_indices'
    LIST_TOA_BANDS = 'list_toa_bands'
    BAND_NUM = 'band_num'
    BAND_DESCRIPTION_LIST= 'band_description_list'

    # Target vars and defaults
    TARGET_ATTR = 'target_attr'
    TARGET_EXTENT = 'target_extent'
    TARGET_XRES = 'target_xres'
    TARGET_YRES = 'target_yres'
    TARGET_PRJ = 'target_prj'
    TARGET_SRS = 'target_srs'
    TARGET_OUTPUT_TYPE = 'target_output_type'
    TARGET_DTYPE = 'target_dtype'
    TARGET_NODATA_VALUE = 'target_nodata_value'

    # Default values
    DEFAULT_XRES = 30.0
    DEFAULT_YRES = 30.0
    DEFAULT_NODATA_VALUE = -9999

    # Regression algorithms
    REGRESSION_MODEL = 'regressor'
    REGRESSOR_MODEL_SIMPLE = 'simple'
    REGRESSOR_MODEL_ROBUST = 'robust'

    # Algorithm classes
    # ALGORITHM_CLASS = 'algorithm'
    # ALGORITHM_CLASS_TARGET = 'target'
    # ALGORITHM_CLASS_QF = 'landsat'
    # ALGORITHM_CLASS_THRESHOLD = 'threshold'

    # Storage type
    STORAGE_TYPE = 'storage'
    STORAGE_TYPE_MEMORY = 'memory'
    STORAGE_TYPE_FILE = 'file'

    # Debug & log values
    DEBUG_NONE_VALUE = 0
    DEBUG_TRACE_VALUE = 1
    DEBUG_VIZ_VALUE = 2
    DEBUG_LEVEL = 'debug_level'
    LOG_FLAG = 'log_flag'
    CLEAN_FLAG = 'clean_flag'
    COG_FLAG = 'cog_flag'

    # Quality flag and list of values
    QUALITY_MASK_FLAG = 'qf_mask_flag'
    LIST_QUALITY_MASK = 'list_quality_mask'

    # Cloud mask flag
    CLOUD_MASK_FLAG = 'cloud_mask_flag'

    # Threshold flag
    THRESHOLD_MASK_FLAG = 'threshold_mask_flag'
    THRESHOLD_MIN = 'threshold_min'
    THRESHOLD_MAX = 'threshold_max'

    # Global instance variables
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
            self.context_dict[Context.DIR_TARGET] = str(args.target_dir)
            self.context_dict[Context.DIR_CLOUDMASK] = str(args.cloudmask_dir)
            self.context_dict[Context.DIR_OUTPUT] = str(args.out_dir)
            self.context_dict[Context.DIR_WARP] = self.context_dict[Context.DIR_OUTPUT]
            if not (args.warp_dir == None):
                self.context_dict[Context.DIR_WARP] = str(args.warp_dir)

            self.context_dict[Context.LIST_BAND_PAIRS] = str(args.band_pairs_list)
            self.context_dict[Context.TARGET_XRES] = self.DEFAULT_XRES
            if not (args.target_xres == None):
                self.context_dict[Context.TARGET_YRES] = float(args.target_xres)
            self.context_dict[Context.TARGET_YRES] = self.DEFAULT_YRES
            if not (args.target_yres == None):
                self.context_dict[Context.TARGET_YRES] = float(args.target_yres)
            self.context_dict[Context.REGRESSION_MODEL] = str(args.regressor)
            self.context_dict[Context.DEBUG_LEVEL] = int(args.debug_level)
            self.context_dict[Context.CLEAN_FLAG] = str(args.cleanbool)
            self.context_dict[Context.LOG_FLAG] = str(args.logbool)
            if eval(self.context_dict[Context.LOG_FLAG]):
                self._create_logfile(self.context_dict[Context.REGRESSION_MODEL],
                                     self.context_dict[Context.DIR_OUTPUT])
            if (int(self.context_dict[Context.DEBUG_LEVEL]) >= int(self.DEBUG_TRACE_VALUE)):
                    print(sys.path)
            # self.context_dict[Context.ALGORITHM_CLASS] = str(args.algorithm)
            self.context_dict[Context.STORAGE_TYPE] = str(args.storage)
            self.context_dict[Context.CLOUD_MASK_FLAG] = str(args.cmaskbool)
            self.context_dict[Context.QUALITY_MASK_FLAG] = str(args.qfmaskbool)
            self.context_dict[Context.LIST_QUALITY_MASK] = str(args.qfmask_list)

            self.context_dict[Context.THRESHOLD_MASK_FLAG] = str(args.thmaskbool)
            threshold_range = (str(args.threshold_range)).partition(",")
            self.context_dict[Context.THRESHOLD_MIN] = int(threshold_range[0])
            self.context_dict[Context.THRESHOLD_MAX] = int(threshold_range[2])

        except BaseException as err:
            print('Check arguments: ', err)
            sys.exit(1)

        # Initialize instance variables
        self.debug_level = int(self.context_dict[Context.DEBUG_LEVEL])
        plotLib = self.plot_lib = PlotLib(self.context_dict[Context.DEBUG_LEVEL])
        os.system(f'mkdir -p {self.context_dict[Context.DIR_OUTPUT]}')
        os.system(f'mkdir -p {self.context_dict[Context.DIR_WARP]}')

        # Echo input parameter values
        plotLib.trace(f'Initializing SRLite Regression script with the following parameters')
        plotLib.trace(f'TOA Directory:    {self.context_dict[Context.DIR_TOA]}')
        plotLib.trace(f'TARGET Directory:    {self.context_dict[Context.DIR_TARGET]}')
        plotLib.trace(f'Cloudmask Directory:    {self.context_dict[Context.DIR_CLOUDMASK]}')
        plotLib.trace(f'Warp Directory:    {self.context_dict[Context.DIR_WARP]}')
        plotLib.trace(f'Output Directory: {self.context_dict[Context.DIR_OUTPUT]}')
        plotLib.trace(f'Band Pairs:    {self.context_dict[Context.LIST_BAND_PAIRS]}')
        plotLib.trace(f'Regression Model:    {self.context_dict[Context.REGRESSION_MODEL]}')
        plotLib.trace(f'Debug Level: {self.context_dict[Context.DEBUG_LEVEL]}')
        plotLib.trace(f'Clean Flag: {self.context_dict[Context.CLEAN_FLAG]}')
        plotLib.trace(f'Log: {self.context_dict[Context.LOG_FLAG]}')
        plotLib.trace(f'Storage:    {self.context_dict[Context.STORAGE_TYPE]}')
        if (eval(self.context_dict[Context.CLOUD_MASK_FLAG] )):
            plotLib.trace(f'Cloud Mask:    {self.context_dict[Context.CLOUD_MASK_FLAG]}')
        if (eval(self.context_dict[Context.QUALITY_MASK_FLAG])):
            plotLib.trace(f'Quality Mask:    {self.context_dict[Context.QUALITY_MASK_FLAG]}')
            plotLib.trace(f'Quality Mask Values:    {self.context_dict[Context.LIST_QUALITY_MASK]}')
        if (eval(self.context_dict[Context.THRESHOLD_MASK_FLAG])):
            plotLib.trace(f'Threshold Mask:    {self.context_dict[Context.THRESHOLD_MASK_FLAG]}')
            plotLib.trace(f'Threshold Min:    {self.context_dict[Context.THRESHOLD_MIN]}')
            plotLib.trace(f'Threshold Max:    {self.context_dict[Context.THRESHOLD_MAX]}')

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
            "-toa_dir", "--input-toa-dir", type=str, required=True, dest='toa_dir',
            default=None, help="Specify directory path containing TOA files."
        )
        parser.add_argument(
            "-target_dir", "--input-target-dir", type=str, required=False, dest='target_dir',
            default=None, help="Specify directory path containing TARGET files."
        )
        parser.add_argument(
            "-cloudmask_dir", "--input-cloudmask-dir", type=str, required=True, dest='cloudmask_dir',
            default=None, help="Specify directory path containing Cloudmask files."
        )
        parser.add_argument(
            "-bandpairs", "--input-list-of-band-pairs", type=str, required=False, dest='band_pairs_list',
            default="[['blue_target', 'BAND-B'], ['green_target', 'BAND-G'], ['red_target', 'BAND-R'], ['nir_target', 'BAND-N']]",
            help="Specify list of band pairs to be processed per scene."
        )
        parser.add_argument(
            "-output_dir", "--output-directory", type=str, required=False, dest='out_dir',
            default="./", help="Specify output directory."
        )
        parser.add_argument(
            "--warp_dir", "--input-warp-dir", type=str, required=False, dest='warp_dir',
            default="./", help="Specify directory path containing warped files."
        )
        parser.add_argument(
            "--xres", "--input-x-resolution", type=str, required=False, dest='target_xres',
            default=None, help="Specify target X resolution (default = 30.0)."
        )
        parser.add_argument(
            "--yres", "--input-y-resolution", type=str, required=False, dest='target_yres',
            default=None, help="Specify target Y resolution (default = 30.0)."
        )
        parser.add_argument(
            "--debug", "--debug_level", type=int, required=False, dest='debug_level',
            default=0, help="Specify debug level [0,1,2,3]"
        )
        parser.add_argument(
            "--clean", "--clean", required=False, dest='cleanbool',
            action='store_true', help="Force cleaning of generated artifacts prior to run (e.g, warp files)."
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

        # parser.add_argument('--algorithm',
        #                     required=False,
        #                     dest='algorithm',
        #                     default='target',
        #                     choices=['target', 'landsat', 'threshold'],
        #                     help='Choose which algorithm to apply to regression')

        parser.add_argument('--storage',
                            required=False,
                            dest='storage',
                            default='memory',
                            choices=['memory', 'file'],
                            help='Choose which storage model to use')

        parser.add_argument('--cloudmask',
                            required=False,
                            dest='cmaskbool',
                            default=False,
                            action='store_true',
                            help='Apply cloud mask values to common mask')

        parser.add_argument('--qfmask',
                            required=False,
                            dest='qfmaskbool',
                            default=False,
                            action='store_true',
                            help='Apply quality flag values to common mask')

        parser.add_argument('--qfmasklist',
                            required=False,
                            dest='qfmask_list',
                            default='0,3,4',
                            type=str,
                            help='Choose quality flag values to mask')

        parser.add_argument('--thmask',
                            required=False,
                            dest='thmaskbool',
                            default=False,
                            action='store_true',
                            help='Apply threshold mask values to common mask')

        parser.add_argument('--thrange',
                            required=False,
                            dest='threshold_range',
                            default='-100, 2000',
                            type=str,
                            help='Choose quality flag values to mask')

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
    # getDebugLevel()
    #
    # Get debug_level
    # -------------------------------------------------------------------------
    def getDebugLevel(self):
        return self.debug_level

    # -------------------------------------------------------------------------
    # getFileNames()
    #
    # Get input file names
    # -------------------------------------------------------------------------
    def getFileNames(self, prefix, context):
        """
        :param prefix: core TOA file name (must match core target and cloudmask file name)
        :param context: input context object dictionary
        :return: updated context
        """
        context[Context.FN_PREFIX] = str((prefix[1]).split("-toa.tif", 1)[0])
        context[Context.FN_TOA] = os.path.join(context[Context.DIR_TOA] + '/' +
                                               context[Context.FN_PREFIX] + self.FN_TOA_SUFFIX)
        context[Context.FN_TOA_DOWNSCALE] = os.path.join(context[Context.DIR_OUTPUT] + '/' +
                                               context[Context.FN_PREFIX] + self.FN_TOA_DOWNSCALE_SUFFIX)
        context[Context.FN_TARGET] = os.path.join(context[Context.DIR_TARGET] + '/' +
                                                context[Context.FN_PREFIX] + self.FN_TARGET_SUFFIX)
        context[Context.FN_TARGET_DOWNSCALE] = os.path.join(context[Context.DIR_OUTPUT] + '/' +
                                                context[Context.FN_PREFIX] + self.FN_TARGET_DOWNSCALE_SUFFIX)
        context[Context.FN_CLOUDMASK] = os.path.join(context[Context.DIR_CLOUDMASK] + '/' +
                                                     context[Context.FN_PREFIX] + self.FN_CLOUDMASK_SUFFIX)
        context[Context.FN_CLOUDMASK_DOWNSCALE] = os.path.join(context[Context.DIR_OUTPUT] + '/' +
                                                     context[Context.FN_PREFIX] + self.FN_CLOUDMASK_DOWNSCALE_SUFFIX)
        context[Context.FN_WARP] = os.path.join(context[Context.DIR_WARP] + '/' +
                                                context[Context.FN_PREFIX] + self.FN_CLOUDMASK_WARP_SUFFIX)
        context[Context.FN_COG] = os.path.join(context[Context.DIR_OUTPUT] + '/' +
                                               context[Context.FN_PREFIX] + self.FN_SRLITE_SUFFIX)

        if not (os.path.exists(context[Context.FN_TOA])):
            raise FileNotFoundError("TOA File not found: {}".format(context[Context.FN_TOA]))
        if not (os.path.exists(context[Context.FN_TARGET])):
            raise FileNotFoundError("TARGET File not found: {}".format(context[Context.FN_TARGET]))
        if not (os.path.exists(context[Context.FN_CLOUDMASK])):
            raise FileNotFoundError("Cloudmask File not found: {}".format(context[Context.FN_CLOUDMASK]))

        return context

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
