// SPDX-FileCopyrightText: Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
// SPDX-License-Identifier: BSD-3-Clause
#ifndef vtkPythonConfigure_h
#define vtkPythonConfigure_h

/* This header is configured by VTK's build process.  */

/* E.g. on BlueGene and Cray there is no multithreading */
/* #undef VTK_NO_PYTHON_THREADS */
/* #undef VTK_PYTHON_FULL_THREADSAFE */

/* Whether the real python debug library has been provided.  */
/* #undef VTK_WINDOWS_PYTHON_DEBUGGABLE */

/* build specific site-packages suffix. This is used to setup Python
 * module paths during initialization.
 */
#define VTK_PYTHON_SITE_PACKAGES_SUFFIX "lib/python3.11/site-packages"

#endif
