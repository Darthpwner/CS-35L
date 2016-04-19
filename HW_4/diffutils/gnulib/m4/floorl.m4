# floorl.m4 serial 6
dnl Copyright (C) 2007, 2009-2010 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_FUNC_FLOORL],
[
  AC_REQUIRE([gl_MATH_H_DEFAULTS])
  dnl Persuade glibc <math.h> to declare floorl().
  AC_REQUIRE([gl_USE_SYSTEM_EXTENSIONS])
  dnl Test whether floorl() is declared.
  AC_CHECK_DECLS([floorl], , , [#include <math.h>])
  if test "$ac_cv_have_decl_floorl" = yes; then
    dnl Test whether floorl() can be used without libm.
    gl_FUNC_FLOORL_LIBS
    if test "$FLOORL_LIBM" = "?"; then
      dnl Sun C 5.0 on Solaris declares floorl() and has it in the system-wide
      dnl libm.so, but not in the libm.so that the compiler uses.
      REPLACE_FLOORL=1
    fi
  else
    HAVE_DECL_FLOORL=0
  fi
  if test $HAVE_DECL_FLOORL = 0 || test $REPLACE_FLOORL = 1; then
    AC_LIBOBJ([floorl])
    FLOORL_LIBM=
  fi
  AC_SUBST([FLOORL_LIBM])
])

# Determines the libraries needed to get the floorl() function.
# Sets FLOORL_LIBM.
AC_DEFUN([gl_FUNC_FLOORL_LIBS],
[
  gl_CACHE_VAL_SILENT([gl_cv_func_floorl_libm], [
    gl_cv_func_floorl_libm=?
    AC_TRY_LINK([
       #ifndef __NO_MATH_INLINES
       # define __NO_MATH_INLINES 1 /* for glibc */
       #endif
       #include <math.h>
       long double x;],
      [x = floorl(x);],
      [gl_cv_func_floorl_libm=])
    if test "$gl_cv_func_floorl_libm" = "?"; then
      save_LIBS="$LIBS"
      LIBS="$LIBS -lm"
      AC_TRY_LINK([
         #ifndef __NO_MATH_INLINES
         # define __NO_MATH_INLINES 1 /* for glibc */
         #endif
         #include <math.h>
         long double x;],
        [x = floorl(x);],
        [gl_cv_func_floorl_libm="-lm"])
      LIBS="$save_LIBS"
    fi
  ])
  FLOORL_LIBM="$gl_cv_func_floorl_libm"
])