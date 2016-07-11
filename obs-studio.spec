Summary:	Open Broadcaster Software Studio
Name:		obs-studio
Version:	0.15.0
Release:	1%{?dist}

License:	GPLv2+ 
URL:		https://obsproject.com/
Source0:	https://github.com/jp9000/obs-studio/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:	cmake
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
BuildRequires:	gcc-objc
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	jansson-devel
BuildRequires:	libX11-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libcurl-devel
BuildRequires:	libv4l-devel
BuildRequires:	mesa-libGL-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtx11extras-devel
BuildRequires:	x264-devel
BuildRequires:	desktop-file-utils

Requires:	ffmpeg
Requires:	hicolor-icon-theme
Requires:	x264

Requires:	%{name}-libs = %{version}-%{release}

%description
Open Broadcaster Software is free and open source
software for video recording and live streaming.

%package libs
Summary: Open Broadcaster Software Studio libraries

%description libs
Library files for Open Broadcaster Software

%package devel
Summary:	Open Broadcaster Software Studio header files
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for Open Broadcaster Software

%prep
%setup -q

%build
export CPPFLAGS=-DFFMPEG_MUX_FIXED="%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux"
%cmake -DCMAKE_INSTALL_PREFIX=/usr \
%ifarch x86_64
      -DOBS_MULTIARCH_SUFFIX=64 \
%endif
      -DOBS_VERSION_OVERRIDE=%{version}

make %{?_smp_mflags}

%install
%make_install

mkdir -p %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/
mv -f %{buildroot}/%{_datadir}/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux
ln -sf %{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux %{buildroot}/%{_datadir}/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/obs.desktop

%post
update-desktop-database >&/dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc README
%license COPYING
%{_bindir}/obs
%{_datadir}/applications/obs.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/obs
%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux

%files libs
%doc README
%license COPYING
%{_libdir}/libobs*.so.*
%{_libdir}/obs-plugins/

%files devel
%doc README
%license COPYING
%{_includedir}/obs
%{_libdir}/libobs*.so
%{_libdir}/cmake/LibObs

%changelog
* Mon Jul 11 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 0.15.0-1
- update to 0.15.0

* Tue Apr 26 2016 Joe brouhard <joe@tech-3.net> 0.14.1
- Version bump to 0.14.1
- Skipped 0.14.0 due to the quick fix release.
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.14.1

* Wed Feb 24 2016 Joe Brouhard <joe@tech-3.net> 0.13.2-1
- Version Bump to 0.13.2
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.13.2

* Sat Feb 6 2016 Joe Brouhard <joe@tech-3.net> 0.13.1-1
- Version Bump to 0.13.1
- 0.13.1 came out before i could build 0.13.0
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.13.1

* Sat Dec 12 2015 Joe Brouhard <joe@tech-3.net> 0.12.4-1
- Version Bump to 0.12.4
- 0.12.4 came out same week as 0.12.3, and build was not done for 0.12.3.
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.12.4

* Fri Nov 20 2015 Joe Brouhard <joe@tech-3.net> 0.12.2-1
- Version bump to 0.12.2
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.12.2

* Wed Nov 18 2015 Joe Brouhard <joe@tech-3.net> 0.12.1-1
- Version Bump to 0.12.1
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.12.1

* Sun Nov 15 2015 Joe Brouhard <joe@tech-3.net> 0.12.0-2
- Built for Fedora 23

* Fri Oct 16 2015 Joe Brouhard <joe@tech-3.net> 0.12.0-2
- SPEC file fixed to remove %%{epoch} that was depreciated some time ago

* Wed Sep 23 2015 Joe Brouhard <joe@tech-3.net> 0.12.0
- Version bump to 0.12.0
- Full changelog can be found at https://github.com/jp9000/obs-studio/releases/tag/0.12.0

* Sat Aug 1 2015 Joe Brouhard <joe@tech-3.net> 0.11.2-2
- Fixed cmake flags to force OBS versioning to match the downloaded sources

* Mon Jul 27 2015 Joe Brouhard <joe@tech-3.net> 0.11.2
- 0.11.2 Update
- Fixed crash with blackmagic source
- Fixed bug with custom server RTMP authentication not working correctly
- Updated ingests

* Fri Jul 24 2015 Joe Brouhard <joe@tech-3.net> 0.11.1
- bumped .spec file up to 0.11.1 as an update

* Thu Mar 26 2015 Momcilo Medic <fedorauser@fedoraproject.org>
- 0.9.0-1
- Initial .spec file
