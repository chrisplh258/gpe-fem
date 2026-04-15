#if !defined(PETSCPETSCVIEWERDEF_H)
#define PETSCPETSCVIEWERDEF_H

#include "petsc/finclude/petscsys.h"
#include "petsc/finclude/petscviewer.h"
#include "petsc/finclude/petscdraw.h"

#define PetscViewerGLVisType type(ePetscViewerGLVisType)
#define PetscViewerFormat type(ePetscViewerFormat)
#define PetscViewerVTKFieldType type(ePetscViewerVTKFieldType)
#define PetscViewerAndFormat PetscFortranAddr

#define PetscViewerType CHARACTER(80)

#define PetscViewer type(tPetscViewer)
#define PetscViewers type(tPetscViewers)

#endif
