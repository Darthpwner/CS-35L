# isfinite.m4 serial 7
dnl Copyright (C) 2007-2010 Free Software Foundation, Inc.
dnl This file is free software; the Free Software Foundation
dnl gives unlimited permission to copy and/or distribute it,
dnl with or without modifications, as long as this notice is preserved.

AC_DEFUN([gl_ISFINITE],
[
  AC_REQUIRE([gl_MATH_H_DEFAULTS])
  dnl Persuade glibc <math.h> to declare isfinite.
  AC_REQUIRE([gl_USE_SYSTEM_EXTENSIONS])
  AC_CHECK_DECLS([isfinite], , , [#include <math.h>])
  if test "$ac_cv_have_decl_isfinite" = yes; then
    gl_CHECK_MATH_LIB([ISFINITE_LIBM], [x = isfinite (x);])
    if test "$ISFINITE_LIBM" != missing; then
      dnl Test whether isfinite() on 'long double' works.
      gl_ISFINITEL_WORKS
      case "$gl_cv_func_isfinitel_works" in
        *yes) ;;
        *)    ISFINITE_LIBM=missing;;
      esac
      dnl Also, isfinite() on 'double' does not work on Linux/ia64 (because of
      dnl signalling NaNs). But this does not have to be tested, since
      dnl isfinite(long double) also does not work in this situation.
    fi
  fi
  if test "$ac_cv_have_decl_isfinite" != yes ||
     test "$ISFINITE_LIBM" = missing; then
    REPLACE_ISFINITE=1
    AC_LIBOBJ([isfinite])
    ISFINITE_LIBM=
  fi
  AC_SUBST([ISFINITE_LIBM])
])

dnl Test whether isfinite() on 'long double' recognizes all numbers which are
dnl neither finite nor infinite. This test fails e.g. on i686, x86_64, ia64,
dnl because of
dnl - pseudo-denormals on x86_64,
dnl - pseudo-zeroes, unnormalized numbers, and pseudo-denormals on i686,
dnl - pseudo-NaN, pseudo-Infinity, pseudo-zeroes, unnormalized numbers, and
dnl   pseudo-denormals on ia64.
AC_DEFUN([gl_ISFINITEL_WORKS],
[
  AC_REQUIRE([AC_PROG_CC])
  AC_REQUIRE([gl_BIGENDIAN])
  AC_REQUIRE([AC_CANONICAL_HOST]) dnl for cross-compiles
  AC_CACHE_CHECK([whether isfinite(long double) works], [gl_cv_func_isfinitel_works],
    [
      AC_RUN_IFELSE([AC_LANG_SOURCE([[
#include <float.h>
#include <limits.h>
#include <math.h>
#define NWORDS \
  ((sizeof (long double) + sizeof (unsigned int) - 1) / sizeof (unsigned int))
typedef union { unsigned int word[NWORDS]; long double value; }
        memory_long_double;
/* On Irix 6.5, gcc 3.4.3 can't compute compile-time NaN, and needs the
   runtime type conversion.  */
#ifdef __sgi
static long double NaNl ()
{
  double zero = 0.0;
  return zero / zero;
}
#else
# define NaNl() (0.0L / 0.0L)
#endif
int main ()
{
  memory_long_double m;
  unsigned int i;

  /* The isfinite macro should be immune against changes in the sign bit and
     in the mantissa bits.  The xor operation twiddles a bit that can only be
     a sign bit or a mantissa bit (since the exponent never extends to
     bit 31).  */
  m.value = NaNl ();
  m.word[NWORDS / 2] ^= (unsigned int) 1 << (sizeof (unsigned int) * CHAR_BIT - 1);
  for (i = 0; i < NWORDS; i++)
    m.word[i] |= 1;
  if (isfinite (m.value))
    return 1;

#if ((defined __ia64 && LDBL_MANT_DIG == 64) || (defined __x86_64__ || defined __amd64__) || (defined __i386 || defined __i386__ || defined _I386 || defined _M_IX86 || defined _X86_))
/* Representation of an 80-bit 'long double' as an initializer for a sequence
   of 'unsigned int' words.  */
# ifdef WORDS_BIGENDIAN
#  define LDBL80_WORDS(exponent,manthi,mantlo) \
     { ((unsigned int) (exponent) << 16) | ((unsigned int) (manthi) >> 16), \
       ((unsigned int) (manthi) << 16) | (unsigned int) (mantlo) >> 16),    \
       (unsigned int) (mantlo) << 16                                        \
     }
# else
#  define LDBL80_WORDS(exponent,manthi,mantlo) \
     { mantlo, manthi, exponent }
# endif
  { /* Quiet NaN.  */
    static memory_long_double x =
      { LDBL80_WORDS (0xFFFF, 0xC3333333, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
  {
    /* Signalling NaN.  */
    static memory_long_double x =
      { LDBL80_WORDS (0xFFFF, 0x83333333, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
  /* The isfinite macro should recognize Pseudo-NaNs, Pseudo-Infinities,
     Pseudo-Zeroes, Unnormalized Numbers, and Pseudo-Denormals, as defined in
       Intel IA-64 Architecture Software Developer's Manual, Volume 1:
       Application Architecture.
       Table 5-2 "Floating-Point Register Encodings"
       Figure 5-6 "Memory to Floating-Point Register Data Translation"
   */
  { /* Pseudo-NaN.  */
    static memory_long_double x =
      { LDBL80_WORDS (0xFFFF, 0x40000001, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
  { /* Pseudo-Infinity.  */
    static memory_long_double x =
      { LDBL80_WORDS (0xFFFF, 0x00000000, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
  { /* Pseudo-Zero.  */
    static memory_long_double x =
      { LDBL80_WORDS (0x4004, 0x00000000, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
  { /* Unnormalized number.  */
    static memory_long_double x =
      { LDBL80_WORDS (0x4000, 0x63333333, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
  { /* Pseudo-Denormal.  */
    static memory_long_double x =
      { LDBL80_WORDS (0x0000, 0x83333333, 0x00000000) };
    if (isfinite (x.value))
      return 1;
  }
#endif

  return 0;
}]])], [gl_cv_func_isfinitel_works=yes], [gl_cv_func_isfinitel_works=no],
      [case "$host_cpu" in
                               # Guess no on ia64, x86_64, i386.
         ia64 | x86_64 | i*86) gl_cv_func_isnanl_works="guessing no";;
         *)                    gl_cv_func_isnanl_works="guessing yes";;
       esac
      ])
    ])
])
