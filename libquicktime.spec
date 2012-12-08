%define major 0
%define libname %mklibname quicktime %{major}
%define develname %mklibname quicktime -d

######################
# Hardcore PLF build
%define build_plf 0
######################

%{?_with_plf: %{expand: %%global build_plf 1}} 
%if %{build_plf}
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%define distsuffix plf
%endif

Summary:	A library for manipulating QuickTime files
Name:		libquicktime
Version:	1.2.4
Release:	2%{?extrarelsuffix}
%if %{build_plf}
License:	GPLv2+
%else
License:	LGPLv2+
%endif
Group:		Video
URL:		http://libquicktime.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/libquicktime/%{name}-%{version}.tar.gz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	pkgconfig(libpng)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	ffmpeg-devel
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(schroedinger-1.0)
BuildRequires:	doxygen

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

%package -n %{develname}
Summary:	Header files and development documentation for libquicktime
Group:		Development/C
Provides:	libquicktime-devel = %{version}-%{release}
Provides:	quicktime-devel = %{version}-%{release}
Provides:	quicktime-static-devel = %{version}-%{release}
Provides:	%{libname}-static-devel = %{version}-%{release}
Provides:	%{libname}-static-devel < 1.2.4
Requires:	%{libname} = %{version}-%{release}

%description -n %develname
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
Summary: Libquicktime plugin for encoding H.264/MPEG-4 streams
Group:		Video
Requires:	%{name} = %{version}-%{release}
BuildRequires:	x264-devel

%description x264
This is a libquicktime plugin for encoding H.264/MPEG-4 streams.

This package is in restricted as it violates some patents.
%endif

%prep
%setup -q

%build
%configure2_5x \
--with-libdv \
%ifarch x86_64
--with-pic \
%endif
%if %{build_plf}
--enable-gpl
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm -f %{buildroot}%{_libdir}/libquicktime/*a
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

%files -n %{develname}
%{_libdir}/lib*.so
%{_includedir}/lqt
%{_libdir}/pkgconfig/*.pc

%files progs
%doc README TODO
%{_bindir}/libquicktime_config
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


%changelog
* Fri Jun 08 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.2.4-2
+ Revision: 803570
- Build for ffmpeg 0.11
- Clean up spec file

* Fri Mar 30 2012 Götz Waschk <waschk@mandriva.org> 1.2.4-1
+ Revision: 788313
- update build deps
- new version

* Sun Oct 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.3-3
+ Revision: 702456
- attempt to relink against libpng15.so.15

* Fri Jul 22 2011 Götz Waschk <waschk@mandriva.org> 1.2.3-2
+ Revision: 691077
- fix plf suffix

* Mon Jul 11 2011 Götz Waschk <waschk@mandriva.org> 1.2.3-1
+ Revision: 689499
- update to new version 1.2.3

* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.2.2-2
+ Revision: 661519
- mass rebuild

* Sat Jan 08 2011 Götz Waschk <waschk@mandriva.org> 1.2.2-1mdv2011.0
+ Revision: 630559
- new version
- drop patch

* Mon Dec 06 2010 Götz Waschk <waschk@mandriva.org> 1.2.1-2mdv2011.0
+ Revision: 612343
- rebuild

* Sat Dec 04 2010 Götz Waschk <waschk@mandriva.org> 1.2.1-1mdv2011.0
+ Revision: 609229
- update to new version 1.2.1

* Thu Dec 02 2010 Götz Waschk <waschk@mandriva.org> 1.2.0-1mdv2011.0
+ Revision: 604758
- new version
- update file list

* Mon Nov 29 2010 Funda Wang <fwang@mandriva.org> 1.1.5-3mdv2011.0
+ Revision: 602824
- fix build with newer gtk

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Wed May 05 2010 Götz Waschk <waschk@mandriva.org> 1.1.5-2mdv2010.1
+ Revision: 542327
- rebuild

* Wed Feb 24 2010 Götz Waschk <waschk@mandriva.org> 1.1.5-1mdv2010.1
+ Revision: 510508
- update to new version 1.1.5

* Sat Jan 23 2010 Götz Waschk <waschk@mandriva.org> 1.1.4-3mdv2010.1
+ Revision: 495208
- rebuild

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.1.4-2mdv2010.1
+ Revision: 488781
- rebuilt against libjpeg v8

* Fri Jan 08 2010 Götz Waschk <waschk@mandriva.org> 1.1.4-1mdv2010.1
+ Revision: 487473
- new version
- drop patch

* Thu Dec 10 2009 Götz Waschk <waschk@mandriva.org> 1.1.3-4mdv2010.1
+ Revision: 475967
- rebuild

* Mon Nov 09 2009 Götz Waschk <waschk@mandriva.org> 1.1.3-3mdv2010.1
+ Revision: 463551
- fix build with new x264

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1.1.3-2mdv2010.0
+ Revision: 416624
- rebuilt against libjpeg v7

* Tue Jul 14 2009 Götz Waschk <waschk@mandriva.org> 1.1.3-1mdv2010.0
+ Revision: 395828
- update to new version 1.1.3

* Thu Jun 18 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.2-1mdv2010.0
+ Revision: 387159
- Update to new version 1.1.2
- Remove string format pathc
- Build with schroedinger (dirac) support

* Wed Feb 11 2009 Götz Waschk <waschk@mandriva.org> 1.1.1-2mdv2009.1
+ Revision: 339353
- rebuild for new libfaad

* Fri Dec 19 2008 Götz Waschk <waschk@mandriva.org> 1.1.1-1mdv2009.1
+ Revision: 316064
- new version
- fix build

* Mon Nov 10 2008 Götz Waschk <waschk@mandriva.org> 1.1.0-2mdv2009.1
+ Revision: 301787
- rebuild
- new version
- drop patches

* Mon Oct 13 2008 Götz Waschk <waschk@mandriva.org> 1.0.3-2mdv2009.1
+ Revision: 293152
- fix build with new ffmpeg

* Tue Jul 15 2008 Götz Waschk <waschk@mandriva.org> 1.0.3-1mdv2009.0
+ Revision: 235774
- fix buildrequires
- new version
- drop patch
- explicitly enable dv

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Fri Apr 25 2008 Götz Waschk <waschk@mandriva.org> 1.0.2-4mdv2009.0
+ Revision: 197454
- update the patch

* Fri Apr 25 2008 Götz Waschk <waschk@mandriva.org> 1.0.2-3mdv2009.0
+ Revision: 197424
- fix build with new ffmpeg

* Fri Jan 18 2008 Götz Waschk <waschk@mandriva.org> 1.0.2-2mdv2008.1
+ Revision: 154554
- rebuild

* Wed Jan 09 2008 Götz Waschk <waschk@mandriva.org> 1.0.2-1mdv2008.1
+ Revision: 147169
- new version

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Oct 14 2007 Funda Wang <fwang@mandriva.org> 1.0.1-1mdv2008.1
+ Revision: 98199
- drop old distro conditions
- New version 1.0.1

  + Thierry Vignaud <tv@mandriva.org>
    - fix summary-ended-with-dot
    - s/Mandrake/Mandriva/

* Wed Apr 18 2007 Götz Waschk <waschk@mandriva.org> 1.0.0-1mdv2008.0
+ Revision: 14609
- new version
- drop patches
- fix build on x86_64
- update file list


* Fri Dec 01 2006 Götz Waschk <waschk@mandriva.org> 0.9.10-2mdv2007.0
+ Revision: 89691
- fix description

* Fri Dec 01 2006 Götz Waschk <waschk@mandriva.org> 0.9.10-1mdv2007.1
+ Revision: 89593
- patch for new x264
- unpack patches
- Import libquicktime

* Fri Dec 01 2006 Götz Waschk <waschk@mandriva.org> 0.9.10-1mdv2007.1
- New version 0.9.10

* Fri Sep 01 2006 Anssi Hannula <anssi@mandriva.org> 0.9.9-6mdv2007.0
- fix buildrequires

* Wed Aug 16 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.9-5
- rebuild for fixed libxaw soname

* Thu Jul 20 2006 Jerome Martin <jmartin@mandriva.org> 0.9.9-4mdv2007.0
- fix BuildRequires for backport

* Sun Jul 09 2006 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.9-3
- add BuildRequires: libalsa-devel libice-devel libxaw-devel libxv-devel

* Sat Jul 08 2006 Charles A Edwards <eslrahc@mandriva.org> 0.9.9-2mdv2007.0
- fix disc for x264 pkg

* Wed Jul 05 2006 Charles A Edwards <eslrahc@mandriva.org> 0.9.9-1mdv2007.0
- 0.9.9 
- add plugin
- add conditionals for License and configure for mdv/plf

* Fri Jun 30 2006 G�tz Waschk <waschk@mandriva.org> 0.9.8-2mdv2007.0
- add ffmpeg module
- remove hardcoded devel deps

* Thu Mar 02 2006 G�tz Waschk <waschk@mandriva.org> 0.9.8-1mdk
- add optional support for lame, faac and faad2
- drop libquicktime1394
- update file list
- New release 0.9.8

* Sat May 28 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.7-2mdk
- fix build deps and automake usage

* Fri May 27 2005 G�tz Waschk <waschk@mandriva.org> 0.9.7-1mdk
- fix file list
- mkrel
- New release 0.9.7

* Tue Feb 15 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.4-3mdk
- fix deps

* Sat Jan 29 2005 Austin Acton <austin@mandrake.org> 0.9.4-2mdk
- rebuild for new libraw1394

* Thu Jan 13 2005 G�tz Waschk <waschk@linux-mandrake.com> 0.9.4-1mdk
- update file list
- New release 0.9.4

* Wed Jul 21 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.9.3-1mdk
- obsolete static-devel package
- add new files
- drop old codecs
- drop patch 2
- drop merged patch 1
- rediff patches 0,3
- add souce URL
- New release 0.9.3

* Sun Jun 13 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.9.2-4mdk
- fix rtjpeg build with new libtool

* Thu Apr 15 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 0.9.2-3mdk
- build dso with pic
- lib64 & 64-bit fixes

* Sat Apr 03 2004 G�tz Waschk <waschk@linux-mandrake.com> 0.9.2-2mdk
- use the mdkversion macro
- new libdv

* Wed Jan 14 2004 Franck Villaume <fvill@freesurf.fr> 0.9.2-1mdk
- 0.9.2 version
- fix 64bits buildrequires

