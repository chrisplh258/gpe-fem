#if !defined(SLEPCSLEPCEPSDEF_H)
#define SLEPCSLEPCEPSDEF_H

#include "slepc/finclude/slepcst.h"
#include "slepc/finclude/slepcbv.h"
#include "slepc/finclude/slepcds.h"
#include "slepc/finclude/slepcrg.h"
#include "slepc/finclude/slepclme.h"
#include "petsc/finclude/petscsnes.h"

#define EPSProblemType type(eEPSProblemType)
#define EPSExtraction type(eEPSExtraction)
#define EPSWhich type(eEPSWhich)
#define EPSBalance type(eEPSBalance)
#define EPSErrorType type(eEPSErrorType)
#define EPSConv type(eEPSConv)
#define EPSStop type(eEPSStop)
#define EPSConvergedReason type(eEPSConvergedReason)
#define EPSPowerShiftType type(eEPSPowerShiftType)
#define EPSKrylovSchurBSEType type(eEPSKrylovSchurBSEType)
#define EPSLanczosReorthogType type(eEPSLanczosReorthogType)
#define EPSPRIMMEMethod type(eEPSPRIMMEMethod)
#define EPSCISSQuadRule type(eEPSCISSQuadRule)
#define EPSCISSExtraction type(eEPSCISSExtraction)
#define EPSEVSLDOSMethod type(eEPSEVSLDOSMethod)
#define EPSEVSLDamping type(eEPSEVSLDamping)

#define EPSType CHARACTER(80)

#define EPS type(tEPS)
#define EPSStoppingCtx type(tEPSStoppingCtx)

#endif
