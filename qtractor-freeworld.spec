%ifarch %{ix86}
%global without_sse %{!?_without_sse:0}%{?_without_sse:1}
%endif
%ifarch ia64 x86_64
%global without_sse 0
%endif
%ifnarch %{ix86} ia64 x86_64
%global without_sse 1
%endif

Summary:       Audio/MIDI multi-track sequencer
Name:          qtractor-freeworld
Version:       0.5.7
Release:       1%{?dist}
License:       GPLv2+
Group:         Applications/Multimedia
URL:           http://qtractor.sourceforge.net/
Source0:       http://downloads.sourceforge.net/qtractor/qtractor-%{version}.tar.gz
Patch1:        qtractor-libmad-factorout.patch

BuildRequires: libmad-devel
BuildRequires: alsa-lib-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: libsndfile-devel
BuildRequires: qt-devel
BuildRequires: autoconf
BuildRequires: automake

Requires:      qtractor%{?_isa} >= %{version}
Obsoletes:     qtractor < 0.5.5

%description
Qtractor is an Audio/MIDI multi-track sequencer application written in C++ 
around the Qt4 toolkit using Qt Designer. The initial target platform will be
Linux, where the Jack Audio Connection Kit (JACK) for audio, and the Advanced
Linux Sound Architecture (ALSA) for MIDI, are the main infrastructures to 
evolve as a fairly-featured Linux Desktop Audio Workstation GUI, specially 
dedicated to the personal home-studio.

%prep
%setup -q -n qtractor-%{version}
%patch1 -p1

# Fix odd permissions
chmod -x src/qtractorMmcEvent.*

%build
autoreconf
export PATH=${PATH}:%{_libdir}/qt4/bin
# remove support for everything except libmad as we are only 
# building the libmad plugin
%configure \
   --enable-liblo=no \
   --enable-libmad=yes \
   --enable-dssi=no \
   --enable-vst=no \
   --enable-slv2=no \
   --enable-lv2=no \
   --enable-ladspa=no \
   --enable-libsndfile=no \
   --enable-libsamplerate=no \
   --enable-libvorbis=no \
   --enable-librubberband=no \
%if %{without_sse}
   --enable-sse=no
%endif

make mad_plugin %{?_smp_mflags}

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}%{_libdir}/qtractor
install -m 755 libqtractor_mad.so %{buildroot}%{_libdir}/qtractor 

%files 
%doc AUTHORS ChangeLog COPYING README TODO
%{_libdir}/qtractor

%changelog
* Wed Jan 09 2013 Brendan Jones <brendan.jones.it@gmail.com> 0.5.7-1
- Rebuild for qtractor 0.5.7

* Sat Oct 06 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.5.6-1
- Rebuild for qtractor 0.5.6

* Fri Sep 14 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.5.5-4
- Correct Requires.

* Wed Aug 15 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.5.5-2
- Correct directory ownership

* Tue Jun 19 2012 Brendan Jones <brendan.jones.it@gmail.com> 0.5.5-1
- Initial package 

