:: This is better than patching I think. We should remove the patch
:: that sets the other variables in NTMakefile and do them all like
:: this instead.
set prefix=%LIBRARY_PREFIX%
set LMDB_INCLUDE=%LIBRARY_INC%
set LMDB_LIBPATH=%LIBRARY_LIB%
set DB_INCLUDE=%LIBRARY_INC%
set DB_LIBPATH=%LIBRARY_LIB%
set OPENSSL_INCLUDE=%LIBRARY_INC%
set OPENSSL_LIBPATH=%LIBRARY_LIB%
set GSSAPI_INCLUDE=%LIBRARY_INC%
set GSSAPI_LIBPATH=%LIBRARY_LIB%
set SQLITE_INCLUDE=%LIBRARY_INC%
set SQLITE_LIBPATH=%LIBRARY_LIB%
set SQLITE_INCLUDE3=%LIBRARY_INC%
set SQLITE_LIBPATH3=%LIBRARY_LIB%
set LDAP_LIB_BASE=%LIBRARY_LIB%
set LDAP_INCLUDE=%LIBRARY_INC%
:: https://social.msdn.microsoft.com/Forums/vstudio/en-US/82304c15-37e2-4761-8928-0c67e074bf47/error-c1069-cannot-read-compiler-command-line-on-visual-studio-2013-rc?forum=vcgeneral
set TMP=%TEMP%

:: 2.1.26 tarball comes with these files. For from-git
:: this is done via a patch instead (but can be done here
:: too, in theory, in-fact this was and can be used to
:: generate or update the patch.
:: goto skip_makeinit
set MSYSTEM=MINGW%ARCH%
set MSYS2_PATH_TYPE=inherit
set CHERE_INVOKING=1
pushd plugins
  if not exist anonymous_init.c bash -lc "./makeinit.sh anonymous_init.c"
  if not exist crammd5_init.c bash -lc "./makeinit.sh crammd5_init.c"
  if not exist digestmd5_init.c bash -lc "./makeinit.sh digestmd5_init.c"
  if not exist scram_init.c bash -lc "./makeinit.sh scram_init.c"
  if not exist gssapiv2_init.c bash -lc "./makeinit.sh gssapiv2_init.c"
  if not exist kerberos4_init.c bash -lc "./makeinit.sh kerberos4_init.c"
  if not exist login_init.c bash -lc "./makeinit.sh login_init.c"
  if not exist ntlm_init.c bash -lc "./makeinit.sh ntlm_init.c"
  if not exist otp_init.c bash -lc "./makeinit.sh otp_init.c"
  if not exist passdss_init.c bash -lc "./makeinit.sh passdss_init.c"
  if not exist plain_init.c bash -lc "./makeinit.sh plain_init.c"
  if not exist sasldb_init.c bash -lc "./makeinit.sh sasldb_init.c"
  if not exist sql_init.c bash -lc "./makeinit.sh sql_init.c"
  if not exist srp_init.c bash -lc "./makeinit.sh srp_init.c"
  if not exist gs2_init.c bash -lc "./makeinit.sh gs2_init.c"
popd
:skip_makeinit
:: We could modify makeinit.sh to include ../common/plugin_common.h
xcopy /I /F /Y common\plugin_common.h plugins
:: .. but then we also hit
:: ntlm.c
:: ntlm.c(100): fatal error C1083: Cannot open include file: 'crypto-compat.h': No such file or directory
:: .. so something more fundamental is not working
xcopy /I /F /Y common\crypto-compat.h plugins

nmake /f NTMakefile ^
        VERBOSE=1 ^
        DB_LIB=libdb62.lib ^
        STATIC=no ^
        NTLM=1 ^
        GSSAPI=MIT ^
        SQL=SQLITE3 ^
        SRP=1 ^
        OTP=1 ^
        install

pushd %LIBRARY_BIN%
:: These are autoloaded, so need to be beside the exes.
copy sasl2\*.dll .
move testsuite.exe cyrus-sasl-testsuite.exe