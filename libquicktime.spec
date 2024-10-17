%define major 0
%define libname %mklibname quicktime %{major}
%define devname %mklibname quicktime -d

######################
# Hardcore PLF build
%define build_plf 0
######################

%{?_with_plf:	%{expand:	%%global build_plf 1}} 
%if %{build_plf}
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%define distsuffix plf
%endif

Summary:	A library for manipulating QuickTime files
Name:		libquicktime
Version:	1.2.4
Release:	5%{?extrarelsuffix}
%if %{build_plf}
License:	GPLv2+
%else
License:	LGPLv2+
%endif
Group:		Video
Url:		https://libquicktime.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/libquicktime/%{name}-%{version}.tar.gz
Patch1:		libquicktime-1.2.4-ffmpeg-2.0.patch
BuildRequires:	doxygen
BuildRequires:	gettext-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(schroedinger-1.0)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xv)

%description
Libquicktime is a library for reading and writing QuickTime files
on UNIX systems. Video CODECs supported by this library are OpenDivX, MJPA,
JPEG Photo, PNG, RGB, YUV 4:2:2, and YUV 4:2:0 compression.  Supported
audio CODECs are Ogg Vorbis, IMA4, ulaw, and any linear PCM format.

Libquicktime is based on the quicktime4linux library.  Libquicktime add
features such as a GNU build tools-based build process and dynamically
loadable CODECs.

%if %{build_plf}
This package is in restricted as it violates some patents.
%endif

%package -n %{libname}
Summary:	Shared library of libquicktime
Group:		System/Libraries

%description -n %{libname}
Libquicktime is a library for reading and writing QuickTime files
on UNIX systems. Video CODECs supported by this library are OpenDivX, MJPA,
JPEG Photo, PNG, RGB, YUV 4:2:2, and YUV 4:2:0 compression.  Supported
audio CODECs are Ogg Vorbis, IMA4, ulaw, and any linear PCM format.

Libquicktime is based on the quicktime4linux library.  Libquicktime add
features such as a GNU build tools-based build process and dynamically
loadable CODECs.

%package -n %{devname}
Summary:	Header files and development documentation for libquicktime
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	quicktime-devel = %{version}-%{release}

%description -n %{devname}
Header files and development documentation for libquicktime.

%package dv
Summary:	Libquicktime plugin supporting the DV codec
Group:		Video
Requires:	%{name} = %{version}-%{release}
BuildRequires:	pkgconfig(libdv)

%description dv
Libquicktime plugin supporting the DV codec

%package progs
Summary:	Useful tools to operate at QuickTime files
Group:		Video
Requires:	%{name} = %{version}-%{release}

%description progs
Useful tools to operate on QuickTime files.

%if %{build_plf}
%package lame
Summary:	Libquicktime plugin supporting the MP3 codec
Group:		Video
Requires:	%{name} = %{version}-%{release}
BuildRequires:	lame-devel

%description lame
This is a libquicktime plugin supporting the MP3 codec based on lame.

This package is in restricted as it violates some patents.

%package faac
Summary:	Libquicktime plugin for encoding AAC
Group:		Video
Requires:	%{name} = %{version}-%{release}
BuildRequires:	libfaac-devel

%description faac
This is a libquicktime plugin for AAC encoding based on faac.

This package is in restricted as it violates some patents.

%package faad
Summary:	Libquicktime plugin for decoding AAC
Group:		Video
Requires:	%{name} = %{version}-%{release}
BuildRequires:	libfaad2-devel

%description faad
This is a libquicktime plugin for AAC decoding based on faad2.

This package is in restricted as it violates some patents.

%package x264
Summary:	Libquicktime plugin for encoding H.264/MPEG-4 streams
Group:		Video
Requires:	%{name} = %{version}-%{release}
BuildRequires:	x264-devel

%description x264
This is a libquicktime plugin for encoding H.264/MPEG-4 streams.

This package is in restricted as it violates some patents.
%endif

%prep
%setup -q
%autopatch -p1
# remove rpath from libtool
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
autoreconf -fi

%build
%configure2_5x	\
	--with-libdv \
	--disable-rpath \
	--with-cpuflags="$RPM_OPT_FLAGS" \
	--disable-static \
	--enable-libswscale \
%ifarch x86_64
	--with-pic \
%endif
%if %{build_plf}
--enable-gpl
%endif

sed -i.rpath 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i.rpath 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make

%install
%makeinstall_std
#rm -f %{buildroot}%{_libdir}/libquicktime/*a
rm -f %{buildroot}%{_libdir}/libquicktime/lqt_opendivx.so
%find_lang %{name}

%files -f %{name}.lang
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
%{_libdir}/libquicktime/lqt_dv.so

%files -n %{libname}
%{_libdir}/libquicktime.so.%{major}*

%files -n %{devname}
%{_bindir}/libquicktime_config
%{_libdir}/lib*.so
%{_includedir}/lqt
%{_libdir}/pkgconfig/*.pc

%files progs
%doc README TODO
%{_bindir}/lqtplay
%{_bindir}/lqtremux
%{_bindir}/lqt_transcode
%{_bindir}/qt*
%{_mandir}/man1/lqtplay.1*

%if %{build_plf}
%files lame
%{_libdir}/libquicktime/lqt_lame.so

%files faac
%{_libdir}/libquicktime/lqt_faac.so

%files faad
%{_libdir}/libquicktime/lqt_faad2.so

%files x264
%{_libdir}/libquicktime/lqt_x264.so
%endif

