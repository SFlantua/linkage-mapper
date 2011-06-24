#!/usr/bin/env python2.

"""Linkage Mapper configuration module.

Assigns input parameters from ToolBox to variables, and sets constants

"""

__filename__ = "lm_config.py"
__version__ = "0.6.4"

import os.path as path
import sys

import arcgisscripting


def str2bool(pstr):
    """Convert ESRI boolean string to Python boolean type"""
    return pstr == 'true'


def setadjmeth(inparam):
    """Return boolean variables for distance methods"""
    if inparam == "Cost-Weighted":
        meth_cw = True
        meth_eu = False
    elif inparam == "Euclidean":
        meth_cw = False
        meth_eu = True
    else:
        meth_cw = True
        meth_eu = True
    return meth_cw, meth_eu


def nullfloat(innum):
    """Convert ESRI float or null to Python float"""
    if innum == '#':
        nfloat = None
    else:
        nfloat = float(innum)
    return nfloat



class Config():
    """Class to enscapulate all global constants"""

    # Model inputs from ArcGIS tool
    scriptDir, script = path.split(str(sys.argv[0]))
    if script == "lm_master.py":
        TOOL = 'linkage_mapper'
        PROJECTDIR = sys.argv[1]  # Project directory
        COREFC = sys.argv[2]  # Core area feature class
        COREFN = sys.argv[3]  # Core area field name
        RESRAST = sys.argv[4]  # Resistance raster

        # Processing steps inputs
        STEP1 = str2bool(sys.argv[5])
        S1ADJMETH_CW, S1ADJMETH_EU = setadjmeth(sys.argv[6])
        STEP2 = str2bool(sys.argv[7])
        S2EUCDISTFILE = sys.argv[8]
        S2ADJMETH_CW, S2ADJMETH_EU = setadjmeth(sys.argv[9])
        STEP3 = str2bool(sys.argv[10])
        S3DROPLCCS = sys.argv[11]  # Drop LCC's with intermediate cores
        STEP4 = str2bool(sys.argv[12])
        S4MAXNN = int(sys.argv[13])  # No of connected nearest neighbors
        S4DISTTYPE_CW, S4DISTTYPE_EU = setadjmeth(sys.argv[14])  # NN Unit
        S4CONNECT = str2bool(sys.argv[15])
        STEP5 = str2bool(sys.argv[16])

        # Optional input parameters
        BUFFERDIST = nullfloat(sys.argv[17])
        MAXCOSTDIST = nullfloat(sys.argv[18])
        MAXEUCDIST = nullfloat(sys.argv[19])

        CWDTHRESH = 100000  # CWD corridor width in a truncated raster
        if MAXCOSTDIST is None:
            TMAXCWDIST = None
        else:
            TMAXCWDIST = MAXCOSTDIST + CWDTHRESH  # This will limit cw calcs
       
    elif script == "barrier_master.py":  #Barrier Mapper    
        TOOL = 'barrier_mapper'
        PROJECTDIR = sys.argv[1]  # Project directory
        RESRAST = sys.argv[2]
        STARTRADIUS = sys.argv[3]  # 
        ENDRADIUS = sys.argv[4]  # 
        RADIUSSTEP = sys.argv[5]  # 
    
    else:
        TOOL = 'pinchpoint_mapper'
        PROJECTDIR = sys.argv[1]  # Project directory
        DOPINCH = str2bool(sys.argv[2])
        RESRAST = sys.argv[3]
        CWDCUTOFF = sys.argv[4] # To clip resistance rasters for Circuitscape
        SQUARERESISTANCES = str2bool(sys.argv[5]) # Square resistance values 
        DOCENTRALITY = str2bool(sys.argv[6])
        COREFC = sys.argv[7]
        COREFN = sys.argv[8]
    # Ouput directory paths & folder names
    OUTPUTDIR = path.join(PROJECTDIR, "output")
    SCRATCHDIR = path.join(PROJECTDIR, "scratch")
    LOGDIR = path.join(PROJECTDIR, "log")
    DATAPASSDIR = path.join(PROJECTDIR, "datapass")
    ADJACENCYDIR = path.join(PROJECTDIR, "adj")
    CWDBASEDIR = path.join(PROJECTDIR, "cwd")
    CWDSUBDIR_NM = "cw"
    LCCBASEDIR = path.join(PROJECTDIR, "nlcc")
    LCCNLCDIR_NM = "nlc"
    LCCMOSAICDIR = path.join(LCCBASEDIR, "mosaic")
    FOCALSUBDIR1_NM = "focalr"
    FOCALSUBDIR2_NM = "f"
    FOCALGRID_NM = "focal"
    BARRIERBASEDIR = path.join(PROJECTDIR, "barrier")
    BARRIERDIR_NM = "bar"
    BARRIERMOSAICDIR = "mosaic"
    CIRCUITBASEDIR = path.join(PROJECTDIR, "pinchpoints")
    CENTRALITYBASEDIR = path.join(PROJECTDIR, "centrality")
    CIRCUITCONFIGDIR_NM = "config"
    CIRCUITOUTPUTDIR_NM =  "output"
        
    
    # Other global constants
    MINCOSTDIST = None
    MINEUCDIST = None
    SAVENORMLCCS = False  # Set to True to save individual normalized LCC grids
    SAVEFOCALRASTERS = False # Save individual focal grids for barrier analysis
    SAVEBARRIERRASTERS = False # Save individual barrier grids
    SAVECURRENTMAPS = False# Save individual current maps from Circuitscape
    FCORES = "fcores"
    OUTPUTGDB = path.join(OUTPUTDIR, "linkages.gdb")
    CWDGDB = path.join(OUTPUTDIR,"cwd.gdb")
    BARRIERGDB = path.join(OUTPUTDIR, "barriers.gdb")
    PINCHGDB = path.join(OUTPUTDIR, "pinchpoints.gdb")
    CENTRALITYGDB = path.join(OUTPUTDIR, "centrality.gdb")
    BNDCIRCEN = "boundingCircleCenter.shp"
    BNDCIR = "boundingCircle.shp"
    
    
    # Link table column numbers
    LTB_LINKID = 0  # Link ID
    LTB_CORE1 = 1  # Core ID of 1st core area link connects
    LTB_CORE2 = 2  # Core ID of 2nd core area link connects
    LTB_CLUST1 = 3  # Component ID of 1st core area link connects
    LTB_CLUST2 = 4  # Component ID of 2nd core area link connects
    LTB_LINKTYPE = 5
    LTB_EUCDIST = 6
    LTB_CWDIST = 7
    LTB_EUCADJ = 8
    LTB_CWDADJ = 9
    LTB_LCPLEN = 10
    LTB_CWDEUCR = 11
    LTB_CWDPATHR = 12
    LTB_EFFRESIST = 13
    LTB_CURRENT = 14
    
    # Linkage type values (NOTE- these map to codes in get_linktype_desc)
    LT_CPLK = -1  # Not_nearest N neighbors
    LT_TLEC = -11  # Too long Euclidean distance
    LT_TLLC = -12  # Too long Cost-Weighted distance
    LT_TSEC = -13  # Too short Euclidean distance
    LT_TSLC = -14  # Too short Cost-Weighted distance
    LT_INT = -15  # Intermediate corea area detected
    LT_CORR = 1  # Connects cores (corridor)
    LT_NNC = 10  # Corridor connecting N Nearest Neighbors
    LT_CLU = 20  # Connects_constellations (corridor)
    LT_NNCT = 30  # TEMP NN corridor links (s4), may be able to get rid of this
    # 1 corridor
    # 10 NN corridor
    # 11 1st nn (future)
    # 12 2nd nn etc (future)
    # 20 constel
    # 21 1st nn constel (future)
    # 22 2nd nn constel etc (future)
    # 30 temp saved nnconstel.  maybe able to get rid fo this

    # Create single geoprocessor object to be used throughout
    gp = arcgisscripting.create(9.3)
    gp.CheckOutExtension("Spatial")
    gp.OverwriteOutput = True
    gp.SnapRaster = RESRAST

    