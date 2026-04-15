#if !defined(PETSCPETSCDMPLEXDEF_H)
#define PETSCPETSCDMPLEXDEF_H

#include "petsc/finclude/petscsection.h"
#include "petsc/finclude/petscpartitioner.h"
#include "petsc/finclude/petscdm.h"
#include "petsc/finclude/petscdmplex.h"
#include "petsc/finclude/petscdt.h"
#include "petsc/finclude/petscfe.h"
#include "petsc/finclude/petscfv.h"
#include "petsc/finclude/petscsf.h"
#include "petsc/finclude/petscdmfield.h"
#include "petsc/finclude/petscviewer.h"

#define DMPlexShape type(eDMPlexShape)
#define DMPlexCoordMap type(eDMPlexCoordMap)
#define DMPlexCSRAlgorithm type(eDMPlexCSRAlgorithm)
#define DMPlexInterpolatedFlag type(eDMPlexInterpolatedFlag)
#define DMPlexTPSType type(eDMPlexTPSType)
#define JacActionCtx PetscFortranAddr


#define DMPlexPointQueue type(tDMPlexPointQueue)
#define PetscGridHash type(tPetscGridHash)
#define DMPlexStorageVersion type(tDMPlexStorageVersion)

#endif
