#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 #
 #  FILE: "periodicGrid2D.py"
 #                                    created: 11/10/03 {3:30:42 PM} 
 #                                last update: 3/8/06 {11:49:17 AM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

"""
2D periodic rectangular Mesh
"""
__docformat__ = 'restructuredtext'

from fipy.meshes.numMesh.grid2D import Grid2D

class PeriodicGrid2D(Grid2D):
    """
    Creates a periodic2D grid mesh with horizontal faces numbered
    first and then vertical faces. Vertices and cells are numbered 
    in the usual way.

        >>> mesh = PeriodicGrid2D(dx = 1., dy = 0.5, nx = 2, ny = 2)

        >>> print mesh.getExteriorFaces()
        [ 4, 5, 8,11,]

        >>> print mesh.getFaceCellIDs()
        [[2 ,0 ,]
         [3 ,1 ,]
         [0 ,2 ,]
         [1 ,3 ,]
         [2 ,-- ,]
         [3 ,-- ,]
         [1 ,0 ,]
         [0 ,1 ,]
         [1 ,-- ,]
         [3 ,2 ,]
         [2 ,3 ,]
         [3 ,-- ,]]

        >>> print mesh._getCellDistances()
        [ 0.5 , 0.5 , 0.5 , 0.5 , 0.25, 0.25, 1.  , 1.  , 0.5 , 1.  , 1.  , 0.5 ,]
 
        >>> print mesh._getCellFaceIDs()
        [[ 0, 7, 2, 6,]
         [ 1, 6, 3, 7,]
         [ 2,10, 0, 9,]
         [ 3, 9, 1,10,]]

        >>> print mesh._getCellToCellDistances()
        [[ 0.5, 1. , 0.5, 1. ,]
         [ 0.5, 1. , 0.5, 1. ,]
         [ 0.5, 1. , 0.5, 1. ,]
         [ 0.5, 1. , 0.5, 1. ,]]

        >>> normals = [[0, 1],
        ...            [0, 1],
        ...            [0, 1],
        ...            [0, 1],
        ...            [0, 1],
        ...            [0, 1],
        ...            [1, 0],
        ...            [1, 0],
        ...            [1, 0],
        ...            [1, 0],
        ...            [1, 0],
        ...            [1, 0]]

        >>> import Numeric
        >>> Numeric.allclose(mesh._getFaceNormals(), normals)
        1

        >>> print mesh._getCellVertexIDs()
        [[4 ,3 ,1 ,0 ,]
         [5 ,4 ,2 ,1 ,]
         [7 ,6 ,4 ,3 ,]
         [8 ,7 ,5 ,4 ,]]

    """
    def __init__(self, dx = 1., dy = 1., nx = None, ny = None):
        Grid2D.__init__(self, dx = dx, dy = dy, nx = nx, ny = ny)
        self.nonPeriodicCellVertexIDs = Grid2D._getCellVertexIDs(self)
        self.nonPeriodicOrderedCellVertexIDs = Grid2D._getOrderedCellVertexIDs()
        self._connectFaces(self.getFacesLeft(), self.getFacesRight())
        self._connectFaces(self.getFacesBottom(), self.getFacesTop())

    def _getCellVertexIDs(self):
        return self.nonPeriodicCellVertexIDs

    def _getOrderedCellVertexIDs(self):
        return self.nonPeriodicOrderedCellVertexIDs
               
class PeriodicGrid2DLeftRight(PeriodicGrid2D):
    def __init__(self, dx = 1., dy = 1., nx = None, ny = None):
        Grid2D.__init__(self, dx = dx, dy = dy, nx = nx, ny = ny)
        self.nonPeriodicCellVertexIDs = Grid2D._getCellVertexIDs(self)
        self.nonPeriodicOrderedCellVertexIDs = Grid2D._getOrderedCellVertexIDs(self)
        self._connectFaces(self.getFacesLeft(), self.getFacesRight())

class PeriodicGrid2DTopBottom(PeriodicGrid2D):
    def __init__(self, dx = 1., dy = 1., nx = None, ny = None):
        Grid2D.__init__(self, dx = dx, dy = dy, nx = nx, ny = ny)
        self.nonPeriodicCellVertexIDs = Grid2D._getCellVertexIDs(self)
        self.nonPeriodicOrderedCellVertexIDs = Grid2D._getOrderedCellVertexIDs(self)
        self._connectFaces(self.getFacesBottom(), self.getFacesTop())
    
def _test():
    import doctest
    return doctest.testmod()

if __name__ == "__main__":
    _test()
