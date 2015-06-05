#####################################################################
#                                                                   #
#                                                                   #
# Copyright 2015, JQI                                               #
#                                                                   #
# This file is part of the program BLACS, in the labscript suite    #
# (see http://labscriptsuite.org), and is licensed under the        #
# Simplified BSD License. See the license.txt file in the root of   #
# the project for the full license.                                 #
#                                                                   #
#####################################################################
import os

def is_rep_name(h5_filepath):
    """
    Decides if a filename is a repeating filename and if so
    returns true along with the basename and the index
    """
    basename = os.path.basename(h5_filepath).split('.h5')[0]
    
    chunks = basename.split('_rep')

    # '_rep' not found    
    if len(chunks) == 1:
        return (False, basename, 0)
    
    try:
        reps = int(basename.split('_rep')[-1])
    except:
        # tail not an integer
        return (False, basename, 0)
    else:
        basename = basename.split('_rep')[-2]
        return (True, basename, reps)

def new_rep_name(h5_filepath, repeats=0):
    """
    Create a new repeating file name
    """
    
    (isRep, basename, reps) = is_rep_name(h5_filepath)
        
    if isRep:
        reps += 1
        if repeats > 1:
            reps %= repeats
        return basename + '_rep%05d.h5'% reps
    return basename + '_rep%05d.h5'%1
