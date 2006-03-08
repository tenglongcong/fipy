#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "test.py"
 #                                    created: 11/10/03 {3:23:47 PM}
 #                                last update: 3/6/06 {8:57:23 AM} 
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

"""Test numeric implementation of the mesh
"""

from fipy.tests.doctestPlus import _LateImportDocTestSuite
import fipy.tests.testProgram

def _suite():
    return _LateImportDocTestSuite(
        docTestModuleNames = (
            'fipy.meshes.numMesh.mesh',
            'fipy.meshes.numMesh.mesh2D',
            'fipy.meshes.numMesh.grid1D',
            'fipy.meshes.numMesh.grid2D',
            'fipy.meshes.numMesh.grid3D',
            'fipy.meshes.numMesh.tri2D',
            'fipy.meshes.numMesh.gmshImport',
            'fipy.meshes.numMesh.adaptiveMesh',
            'fipy.meshes.numMesh.refinedMesh',
            'fipy.meshes.numMesh.periodicGrid1D',
            'fipy.meshes.numMesh.periodicGrid2D',
            'fipy.meshes.numMesh.uniformGrid1D',
            'fipy.meshes.numMesh.uniformGrid2D',
            'fipy.meshes.numMesh.uniformGrid3D',
        ))
    
if __name__ == '__main__':
    fipy.tests.testProgram.main(defaultTest='_suite')
