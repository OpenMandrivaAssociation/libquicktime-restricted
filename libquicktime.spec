%define major 0
%define fversion %version
%define build_plf 0
%define libname %mklibname quicktime %major
%define develname %mklibname quicktime -d
%{?_with_plf: %{expand: %%global build_plf 1}} 
%if %build_plf
%if %mdvver >= 201100
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif
%define distsuffix plf
%endif

Summary:	A library for manipulating QuickTime files
Name:		libquicktime
Version:	1.2.4
Release:	2%{?extrarelsuffix}
%if %build_plf
License:	GPLv2+
%else
License:        LGPLv2+
%endif
Group:		Video
Source0:	http://prdownloads.sourceforge.net/libquicktime/%{name}-%{fversion}.tar.gz
URL:		http://libquicktime.sourceforge.net/
BuildRequires:	png-devel
BuildRequires:	jpeg-devel
BuildRequires: 	oggvorbis-devel
BuildRequires:  autoconf
BuildRequires:	automake
BuildRequires:  mesaglu-devel
BuildRequires:	libgtk+2.0-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	libalsa-devel
BuildRequires:	libice-devel
BuildRequires:	libxaw-devel
BuildRequires:	libxv-devel
BuildRequires:	libschroedinger-devel
BuildRequires:	doxygen
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


%package -n %develname
Summary:	Header files and development documentation for libquicktime
Group:		Development/C
Provides:	libquicktime-devel = %version-%release
Provides:	quicktime-devel = %version-%release
Provides:	quicktime-static-devel = %version-%release
Provides:	%libname-static-devel = %version-%release
Obsoletes:	%libname-static-devel = %version-%release
Obsoletes:	%mklibname -d quicktime 0
Requires:	%{libname} = %{version}

%description -n %develname
Header files and development documentation for libquicktime.


%package dv
Summary:	Libquicktime plugin supporting the DV codec
Group:		Video
Requires:	%{name} = %{version}
BuildRequires:	libdv-devel >= 0.103

%description dv
Libquicktime plugin supporting the DV codec

#%package -n %libname-static-devel
#Summary:	Static libquicktime libraries
#Group:		Development/C
#Requires:	%{libname}-devel = %{version}

#%description -n %libname-static-devel
#Static libquicktime libraries.

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
Summary: Libquicktime plugin for encoding H.264/MPEG-4 streams
Group:		Video
Requires:	%{name} = %{version}
BuildRequires: libx264-devel

%description x264
This is a libquicktime plugin for encoding H.264/MPEG-4 streams.

This package is in PLF as it violates some patents.
%endif

%prep
%setup -q -n %name-%fversion

%build

%configure2_5x \
--with-libdv \
%ifarch x86_64
--with-pic \
%endif
%if %build_plf
--enable-gpl 
%endif
 
%make 

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %buildroot%_libdir/libquicktime/*a
rm -f %buildroot%_libdir/*.la
rm -f %buildroot%_libdir/libquicktime/lqt_opendivx.so
%find_lang %name

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post  -n %libname -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif

%files -f %name.lang
%defattr(-,root,root)
%doc README
%dir %{_libdir}/libquicktime/
%{_libdir}/libquicktime/lqt_audiocodec.so
%{_libdir}/libquicktime/lqt_ffmpeg.so
%{_libdir}/libquicktime/lqt_mjpeg.so
%{_libdir}/libquicktime/lqt_png.so
%{_libdir}/libquicktime/lqt_videocodec.so
%{_libdir}/libquicktime/lqt_rtjpeg.so
%{_libdir}/libquicktime/lqt_schroedinger.so
%{_libdir}/libquicktime/lqt_vorbis.so
 
%files dv
%defattr(-,root,root)
%{_libdir}/libquicktime/lqt_dv.so

%files -n %libname
%defattr(-,root,root)
%{_libdir}/libquicktime.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%{_libdir}/lib*.so
%{_includedir}/lqt
%_libdir/pkgconfig/*.pc

%files progs
%defattr(-,root,root)
%doc README TODO
%{_bindir}/libquicktime_config
%_bindir/lqtplay
%_bindir/lqtremux
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


