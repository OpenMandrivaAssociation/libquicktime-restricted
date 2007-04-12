%define name libquicktime
%define major 0
%define version 0.9.10
%define fversion %version
%define release %mkrel 2
%define build_plf 0
%define mdkversion		%(perl -pe '/(\\d+)\\.(\\d)\\.?(\\d)?/; $_="$1$2".($3||0)' /etc/mandrake-release)
%if %mdkversion <= 900
%define libname %name%major
%else
%define libname %mklibname quicktime %major
%endif
#fixed2
%{?!mkrel:%define mkrel(c:) %{-c: 0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}
%{?_with_plf: %{expand: %%global build_plf 1}} 
%if %build_plf
%define distsuffix plf
%endif

Summary:	A library for manipulating QuickTime files
Name:		%name
Version:	%version
Release:	%release
%if %build_plf
License:	GPL
%else
License:	LGPL
%endif
Group:		Video
Source0:	http://prdownloads.sourceforge.net/libquicktime/%{name}-%{fversion}.tar.bz2
Patch0:		libquicktime-0.9.3-lib64.patch
Patch1:		libquicktime-0.9.10-x264.patch
Patch3:		libquicktime-0.9.3-automake-man_MANS.patch
URL:		http://libquicktime.sourceforge.net/
BuildRequires:	png-devel
BuildRequires:	jpeg-devel
BuildRequires: 	oggvorbis-devel
BuildRequires:  autoconf2.5
BuildRequires:	automake1.9
BuildRequires:  MesaGLU-devel
BuildRequires:	libgtk+2.0-devel
BuildRequires:	libffmpeg-devel
BuildRequires:	libalsa-devel
%if %mdkversion >= 200700
BuildRequires:	libice-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxv-devel
%else
BuildRequires:	X11-devel
%endif
BuildRoot:	%_tmppath/%name-%version

%description
Libquicktime is a library for reading and writing QuickTime files
on UNIX systems. Video CODECs supported by this library are OpenDivX, MJPA,
JPEG Photo, PNG, RGB, YUV 4:2:2, and YUV 4:2:0 compression.  Supported
audio CODECs are Ogg Vorbis, IMA4, ulaw, and any linear PCM format.

Libquicktime is based on the quicktime4linux library.  Libquicktime add
features such as a GNU build tools-based build process and dynamically
loadable CODECs.

%if %build_plf
This package is in PLF as it violates some patents.
%endif

%package -n %libname
Summary:	Shared library of libquicktime
Group:		System/Libraries

%description -n %libname
Libquicktime is a library for reading and writing QuickTime files
on UNIX systems. Video CODECs supported by this library are OpenDivX, MJPA,
JPEG Photo, PNG, RGB, YUV 4:2:2, and YUV 4:2:0 compression.  Supported
audio CODECs are Ogg Vorbis, IMA4, ulaw, and any linear PCM format.

Libquicktime is based on the quicktime4linux library.  Libquicktime add
features such as a GNU build tools-based build process and dynamically
loadable CODECs.


%package -n %libname-devel
Summary:	Header files and development documentation for libquicktime
Group:		Development/C
Provides:	libquicktime-devel = %version-%release
Provides:	quicktime-devel = %version-%release
Provides:	%libname-static-devel = %version-%release
Obsoletes:	%libname-static-devel = %version-%release
Requires:	%{libname} = %{version}

%description -n %libname-devel
Header files and development documentation for libquicktime.


%package dv
Summary:	Libquicktime plugin supporting the DV codec
Group:		Video
Requires:	%{name} = %{version}
BuildRequires:	libdv-devel >= 0.9

%description dv
Libquicktime plugin supporting the DV codec

%package -n %libname-static-devel
Summary:	Static libquicktime libraries
Group:		Development/C
Requires:	%{libname}-devel = %{version}

%description -n %libname-static-devel
Static libquicktime libraries.

%package progs
Summary:	Useful tools to operate at QuickTime files
Group:		Video
Requires:	%name = %version

%description progs
Useful tools to operate on QuickTime files.

%if %build_plf
%package lame
Summary: Libquicktime plugin supporting the MP3 codec
Group:		Video
Requires:	%{name} = %{version}
BuildRequires: liblame-devel

%description lame
This is a libquicktime plugin supporting the MP3 codec based on lame.

This package is in PLF as it violates some patents.
%package faac
Summary: Libquicktime plugin for encoding AAC
Group:		Video
Requires:	%{name} = %{version}
BuildRequires: libfaac-devel

%description faac
This is a libquicktime plugin for AAC encoding based on faac.

This package is in PLF as it violates some patents.
%package faad
Summary: Libquicktime plugin for decoding AAC
Group:		Video
Requires:	%{name} = %{version}
BuildRequires: libfaad2-devel

%description faad
This is a libquicktime plugin for AAC decoding based on faad2.

This package is in PLF as it violates some patents.

%package x264
Summary: Libquicktime plugin for encoding H.264/MPEG-4 streams.
Group:		Video
Requires:	%{name} = %{version}
BuildRequires: libx264-devel

%description x264
This is a libquicktime plugin for encoding H.264/MPEG-4 streams.

This package is in PLF as it violates some patents.
%endif

%prep
%setup -q -n %name-%fversion
%patch0 -p1 -b .lib64
%patch1 -p1 -b .x264
%patch3 -p1 -b .automake-man_MANS

%build
# needed for updated libtool & fixed Makefile.am
aclocal-1.9 -I m4
autoheader
autoconf
automake-1.9 -a -c --foreign

%if %build_plf 
%configure2_5x --enable-gpl
%else
%configure2_5x                      
%endif
 
%make 

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std
rm -f %buildroot%_libdir/libquicktime/*a
rm -f %buildroot%_libdir/*.la
rm -f %buildroot%_libdir/libquicktime/lqt_opendivx.so
cp lqt-config %buildroot%_bindir 
 
%clean
rm -rf $RPM_BUILD_ROOT

%post  -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%dir %{_libdir}/libquicktime/
%{_libdir}/libquicktime/lqt_audiocodec.so
%{_libdir}/libquicktime/lqt_ffmpeg.so
%{_libdir}/libquicktime/lqt_mjpeg.so
%{_libdir}/libquicktime/lqt_png.so
%{_libdir}/libquicktime/lqt_videocodec.so
%{_libdir}/libquicktime/lqt_rtjpeg.so
%{_libdir}/libquicktime/lqt_vorbis.so
 
%files dv
%defattr(-,root,root)
%{_libdir}/libquicktime/lqt_dv.so

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libquicktime.so.%{major}*

%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/lqt
%_datadir/aclocal/lqt.m4
%{_bindir}/lqt-config
%_libdir/pkgconfig/*.pc

%files progs
%defattr(-,root,root)
%doc README TODO
%{_bindir}/libquicktime_config
%_bindir/lqtplay
%_bindir/lqt_transcode
%_bindir/qt*
%_mandir/man1/lqtplay.1*

%if %build_plf
%files lame
%defattr(-,root,root)
%{_libdir}/libquicktime/lqt_lame.so

%files faac
%defattr(-,root,root)
%{_libdir}/libquicktime/lqt_faac.so

%files faad
%defattr(-,root,root)
%{_libdir}/libquicktime/lqt_faad2.so

%files x264
%defattr(-,root,root)
%{_libdir}/libquicktime/lqt_x264.so
%endif


