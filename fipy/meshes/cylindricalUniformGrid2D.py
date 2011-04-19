#!/usr/bin/env python

## -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "CylindricalUniformGrid2D.py"
 #
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
 # ###################################################################
 ##

"""
2D cylindrical rectangular Mesh with constant spacing in x and constant spacing in y
"""
__docformat__ = 'restructuredtext'

from fipy.meshes.uniformGrid2D import UniformGrid2D
from fipy.tools import numerix
from fipy.tools import parallel

class CylindricalUniformGrid2D(UniformGrid2D):
    r"""
    Creates a 2D cylindrical grid in the radial and axial directions,
    appropriate for axial symmetry.
    """
    def __init__(self, dx=1., dy=1., nx=1, ny=1, origin=((0,),(0,)), 
                 overlap=2, communicator=parallel):
        super(CylindricalUniformGrid2D, self).__init__(dx=dx, dy=dy, nx=nx, ny=ny, 
                               origin=origin, overlap=overlap, 
                               communicator=communicator)

    def _translate(self, vector):
        return CylindricalUniformGrid2D(dx = self.args['dx'], nx = self.args['nx'], 
                                        dy = self.args['dy'], ny = self.args['ny'], 
                                        origin=numerix.array(self.args['origin']) + vector,
                                        overlap=self.args['overlap'])

    @property
    def _faceAreas(self):
        faceAreas = numerix.zeros(self.numberOfFaces, 'd')
        faceAreas[:self.numberOfHorizontalFaces] = self.dx
        faceAreas[self.numberOfHorizontalFaces:] = self.dy
        return faceAreas * self._faceCenters[0]
        
    @property
    def _cellVolumes(self):
        return numerix.ones(self.numberOfCells, 'd') * self.dx * self.dy

    @property
    def _cellAreas(self):
        areas = numerix.ones((4, self.numberOfCells), 'd')
        areas[0] = self.dx * self._cellCenters[0]
        areas[1] = self.dy * (self._cellCenters[0] + self.dx / 2)
        areas[2] = self.dx * self._cellCenters[0]
        areas[3] = self.dy * (self._cellCenters[0] - self.dx / 2)
        return areas
 
    """
    def _calcAreaProjections(self):
        return self._getAreaProjectionsPy()
    """
 
    def _calcAreaProjections(self):
        return self._faceNormals * self._faceAreas
 
    @property
    def cellVolumes(self):
        return self._cellVolumes * self.cellCenters[0]

    def _test(self):
        """
        These tests are not useful as documentation, but are here to ensure
        everything works as expected.

            >>> from fipy.tools import parallel

            >>> dx = 0.5
            >>> dy = 2.
            >>> nx = 3
            >>> ny = 2
            
            >>> mesh = CylindricalUniformGrid2D(nx = nx, ny = ny, dx = dx, dy = dy)     
            
            >>> vertices = numerix.array(((0., 1., 2., 3., 0., 1., 
            ...                            2., 3., 0., 1., 2., 3.),
            ...                           (0., 0., 0., 0., 1., 1., 
            ...                            1., 1., 2., 2., 2., 2.)))
            >>> vertices *= numerix.array([[dx], [dy]])
            >>> print parallel.procID > 0 or numerix.allequal(vertices,
            ...                                               mesh.vertexCoords)
            True
        
            >>> faces = numerix.array([[1, 2, 3, 5, 6, 7, 9, 10, 11,  
            ...                         4, 5, 6, 7, 8, 9, 10, 11], 
            ...                        [0, 1, 2, 4, 5, 6, 8, 9, 10,  
            ...                         0, 1, 2, 3, 4, 5, 6, 7]])            
            >>> print parallel.procID > 0 or numerix.allequal(faces,
            ...                                               mesh.faceVertexIDs)
            True

            >>> cells = numerix.array(((0,  1,  2,  3,  4,  5),
            ...                       (10, 11, 12, 14, 15, 16),
            ...                       ( 3,  4,  5,  6,  7,  8),
            ...                       ( 9, 10, 11, 13, 14, 15)))
            >>> print parallel.procID > 0 or numerix.allequal(cells,
            ...                                               mesh.cellFaceIDs)
            True

            >>> externalFaces = numerix.array((0, 1, 2, 6, 7, 8, 9 , 12, 13, 16))
            >>> print parallel.procID > 0 or  numerix.allequal(externalFaces, 
            ...                                                numerix.nonzero(mesh.exteriorFaces))
            True

            >>> internalFaces = numerix.array((3, 4, 5, 10, 11, 14, 15))
            >>> print parallel.procID > 0 or numerix.allequal(internalFaces, 
            ...                                               numerix.nonzero(mesh.interiorFaces))
            True

            >>> from fipy.tools.numerix import MA
            >>> faceCellIds = MA.masked_values((( 0,  1,  2, 0,  1,  2,  3,  4, 
            ...                                   5,  0,  0, 1,  2,  3,  3,  4,  5),
            ...                                 (-1, -1, -1, 3,  4,  5, -1, -1, 
            ...                                  -1, -1,  1, 2, -1, -1,  4,  5, -1)), -1)
            >>> print parallel.procID > 0 or numerix.allequal(faceCellIds, mesh.faceCellIDs)
            True
            
            >>> faceAreas = numerix.array((dx, dx, dx, dx, dx, dx, dx, dx, dx,
            ...                            dy, dy, dy, dy, dy, dy, dy, dy))
            >>> if parallel.procID == 0: 
            ...     faceAreas = faceAreas * mesh.faceCenters[0]
            >>> print parallel.procID > 0 or numerix.allclose(faceAreas, mesh._faceAreas, atol = 1e-10, rtol = 1e-10)
            True
            
            >>> faceCoords = numerix.take(vertices, faces, axis=1)
            >>> faceCenters = (faceCoords[...,0,:] + faceCoords[...,1,:]) / 2.
            >>> print parallel.procID > 0 or numerix.allclose(faceCenters, mesh.faceCenters, atol = 1e-10, rtol = 1e-10)
            True

            >>> faceNormals = numerix.array(((0., 0., 0., 0., 0., 0., 0., 0., 0., 
            ...                               -1., 1., 1., 1., -1., 1., 1., 1.),
            ...                              (-1., -1., -1., 1., 1., 1., 1., 1., 
            ...                               1., 0, 0, 0, 0, 0, 0, 0, 0)))
            >>> print parallel.procID > 0 or numerix.allclose(faceNormals, mesh._faceNormals, atol = 1e-10, rtol = 1e-10)
            True

            >>> cellToFaceOrientations = numerix.array(((1,  1,  1, -1, -1, -1), 
            ...                                         (1,  1,  1,  1,  1,  1),
            ...                                         (1,  1,  1,  1,  1,  1),
            ...                                         (1, -1, -1,  1, -1, -1)))
            >>> print parallel.procID > 0 or numerix.allequal(cellToFaceOrientations, mesh._cellToFaceOrientations)
            True
                                             
            >>> type(mesh.cellCenters)
            <class 'fipy.variables.cellVariable.CellVariable'>

            >>> testCellVolumes = mesh.cellCenters[0].globalValue * numerix.array((dx*dy, dx*dy, dx*dy, dx*dy, dx*dy, dx*dy))

            >>> type(mesh.cellVolumes)
            <class 'fipy.variables.binaryOperatorVariable.binOp'>

            >>> print numerix.allclose(testCellVolumes, mesh.cellVolumes.globalValue, atol = 1e-10, rtol = 1e-10)
            True

            >>> cellCenters = numerix.array(((dx/2., 3.*dx/2., 5.*dx/2.,    dx/2., 3.*dx/2., 5.*dx/2.),
            ...                              (dy/2.,    dy/2.,    dy/2., 3.*dy/2., 3.*dy/2., 3.*dy/2.)))
            >>> print numerix.allclose(cellCenters, mesh.cellCenters, atol = 1e-10, rtol = 1e-10)
            True
                                              
            >>> cellDistances = numerix.array((dy / 2., dy / 2., dy / 2.,
            ...                                dy, dy, dy,
            ...                                dy / 2., dy / 2., dy / 2.,
            ...                                dx / 2., dx, dx,
            ...                                dx / 2.,
            ...                                dx / 2., dx, dx,
            ...                                dx / 2.))
            >>> print parallel.procID > 0 or numerix.allclose(cellDistances, mesh._cellDistances, atol = 1e-10, rtol = 1e-10)
            True
            
            >>> faceToCellDistances = MA.masked_values(((dy / 2., dy / 2., dy / 2., dy / 2., dy / 2., dy / 2., dy / 2., dy / 2., dy / 2., dx / 2., dx / 2., dx / 2., dx / 2., dx / 2., dx / 2., dx / 2., dx / 2.),
            ...                                         (     -1,      -1,      -1, dy / 2., dy / 2., dy / 2.,      -1,      -1,      -1,      -1, dx / 2., dx / 2.,      -1,      -1, dx / 2., dx / 2.,      -1)), -1)
            >>> faceToCellDistanceRatios = faceToCellDistances[0] / cellDistances
            >>> print parallel.procID > 0 or numerix.allclose(faceToCellDistanceRatios, mesh._faceToCellDistanceRatio, atol = 1e-10, rtol = 1e-10)
            True

            >>> areaProjections = faceNormals * faceAreas
            >>> print parallel.procID > 0 or numerix.allclose(areaProjections, mesh._areaProjections, atol = 1e-10, rtol = 1e-10)
            True

            >>> tangents1 = numerix.array(((1., 1., 1., -1., -1., -1., -1., -1., 
            ...                             -1., 0., 0., 0., 0., 0., 0., 0., 0.),
            ...                            (0, 0, 0, 0, 0, 0, 0, 0, 0, -1., 1., 
            ...                             1., 1., -1., 1., 1., 1.)))
            >>> print parallel.procID > 0 or numerix.allclose(tangents1, mesh._faceTangents1, atol = 1e-10, rtol = 1e-10)
            True

            >>> tangents2 = numerix.zeros((2, 17), 'd')
            >>> print parallel.procID > 0 or numerix.allclose(tangents2, mesh._faceTangents2, atol = 1e-10, rtol = 1e-10)
            True

            >>> cellToCellIDs = MA.masked_values(((-1, -1, -1,  0,  1,  2),
            ...                                   ( 1,  2, -1,  4,  5, -1),
            ...                                   ( 3,  4,  5, -1, -1, -1),
            ...                                   (-1,  0,  1, -1,  3,  4)), -1)
            >>> print parallel.procID > 0 or numerix.allequal(cellToCellIDs, mesh._cellToCellIDs)
            True

            >>> cellToCellDistances = MA.masked_values(((dy / 2., dy / 2., dy / 2.,      dy,      dy,      dy),
            ...                                         (     dx,      dx, dx / 2.,      dx,      dx, dx / 2.),
            ...                                         (     dy,      dy,      dy, dy / 2., dy / 2., dy / 2.),
            ...                                         (dx / 2.,      dx,      dx, dx / 2.,      dx,      dx)), -1)
            >>> print parallel.procID > 0 or numerix.allclose(cellToCellDistances, mesh._cellToCellDistances, atol = 1e-10, rtol = 1e-10)
            True

            >>> cellNormals = numerix.array(((( 0,  0,  0,  0,  0,  0),
            ...                               ( 1,  1,  1,  1,  1,  1),
            ...                               ( 0,  0,  0,  0,  0,  0),
            ...                               (-1, -1, -1, -1, -1, -1)),
            ...                              ((-1, -1, -1, -1, -1, -1),
            ...                               ( 0,  0,  0,  0,  0,  0),
            ...                               ( 1,  1,  1,  1,  1,  1),
            ...                               ( 0,  0,  0,  0,  0,  0))))
            >>> print parallel.procID > 0 or numerix.allclose(cellNormals, mesh._cellNormals, atol = 1e-10, rtol = 1e-10)
            True

            >>> cellAreaProjections = numerix.array((((0,) * 6, (dy,) * 6, (0,) * 6, (-dy,) * 6),
            ...                                      ((-dx,) * 6, (0,) * 6, (dx,) * 6, (0,) * 6)))
            
            >>> if parallel.procID == 0:
            ...     cellAreaProjections[:,0] = cellAreaProjections[:,0] * mesh.cellCenters[0]
            ...     cellAreaProjections[:,1] = cellAreaProjections[:,1] * (mesh.cellCenters[0] + mesh.dx / 2.)
            ...     cellAreaProjections[:,2] = cellAreaProjections[:,2] * mesh.cellCenters[0]
            ...     cellAreaProjections[:,3] = cellAreaProjections[:,3] * (mesh.cellCenters[0] - mesh.dx / 2.)
            >>> print parallel.procID > 0 or numerix.allclose(cellAreaProjections, mesh._cellAreaProjections, atol = 1e-10, rtol = 1e-10)
            True

            >>> cellVertexIDs = MA.masked_array(((5, 6, 7, 9, 10, 11),
            ...                                  (4, 5, 6, 8, 9, 10),
            ...                                  (1, 2, 3, 5, 6, 7),
            ...                                  (0, 1, 2, 4, 5, 6)), -1000)

            >>> print parallel.procID > 0 or numerix.allclose(mesh._cellVertexIDs, cellVertexIDs)
            True

            >>> from fipy.tools import dump            
            >>> (f, filename) = dump.write(mesh, extension = '.gz')
            >>> unpickledMesh = dump.read(filename, f)

            >>> print numerix.allclose(mesh.cellCenters, unpickledMesh.cellCenters)
            True
            
            >>> faceVertexIDs = [[ 1, 2, 3, 5, 6, 7, 9, 10, 11, 4, 5, 6, 7, 8, 9, 10, 11],   
            ...                  [ 0, 1, 2, 4, 5, 6, 8,  9, 10, 0, 1, 2, 3, 4, 5,  6,  7]] 
            >>> print parallel.procID > 0 or numerix.allequal(mesh.faceVertexIDs, faceVertexIDs)
            True

            >>> mesh = CylindricalUniformGrid2D(nx=3)
            >>> print parallel.procID > 0 or numerix.allequal(mesh._adjacentCellIDs[0],
            ...                                               [0, 1, 2, 0, 1, 2, 0, 0, 1, 2])
            True
            >>> print parallel.procID > 0 or numerix.allequal(mesh._adjacentCellIDs[1],
            ...                                               [0, 1, 2, 0, 1, 2, 0, 1, 2, 2])
            True
            >>> faceCellIDs = [[0, 1, 2, 0, 1, 2, 0, 0, 1, 2],
            ...                [-1, -1, -1, -1, -1, -1, -1, 1, 2, -1]]
            >>> print parallel.procID > 0 or numerix.allequal(mesh.faceCellIDs.filled(-1),
            ...                                               faceCellIDs)
            True

            >>> mesh = CylindricalUniformGrid2D(ny=3)
            >>> print parallel.procID > 0 or numerix.allequal(mesh._adjacentCellIDs[0],
            ...                                               [0, 0, 1, 2, 0, 0, 1, 1, 2, 2])
            True
            >>> print parallel.procID > 0 or numerix.allequal(mesh._adjacentCellIDs[1],
            ...                                               [0, 1, 2, 2, 0, 0, 1, 1, 2, 2])
            True
            >>> faceCellIDs = [[0, 0, 1, 2, 0, 0, 1, 1, 2, 2],
            ...                [-1, 1, 2, -1, -1, -1, -1, -1, -1, -1]]
            >>> print parallel.procID > 0 or numerix.allequal(mesh.faceCellIDs.filled(-1),
            ...                                               faceCellIDs)
            True

        Following test added to change nx, ny argment to integer when its a float to prevent
        warnings from the solver.

            >>> from fipy import *
            >>> mesh = CylindricalUniformGrid2D(nx=3., ny=3., dx=1., dy=1.)
            >>> var = CellVariable(mesh=mesh)
            >>> DiffusionTerm().solve(var)

        """

def _test():
    import doctest
    return doctest.testmod()

if __name__ == "__main__":
    _test()
