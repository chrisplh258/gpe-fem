#if !defined(SLEPCSLEPCSVDDEF_H)
#define SLEPCSLEPCSVDDEF_H

#include "slepc/finclude/slepceps.h"
#include "slepc/finclude/slepcbv.h"
#include "slepc/finclude/slepcds.h"

#define SVDProblemType type(eSVDProblemType)
#define SVDWhich type(eSVDWhich)
#define SVDErrorType type(eSVDErrorType)
#define SVDConv type(eSVDConv)
#define SVDStop type(eSVDStop)
#define SVDConvergedReason type(eSVDConvergedReason)
#define SVDTRLanczosGBidiag type(eSVDTRLanczosGBidiag)
#define SVDPRIMMEMethod type(eSVDPRIMMEMethod)
#define SVDKSVDEigenMethod type(eSVDKSVDEigenMethod)
#define SVDKSVDPolarMethod type(eSVDKSVDPolarMethod)

#define SVDType CHARACTER(80)

#define SVD type(tSVD)
#define SVDStoppingCtx type(tSVDStoppingCtx)

#endif
