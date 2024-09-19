%define major 0
%define libname %mklibname btrfs %{major}
%define majorutil 1
%define libutilname %mklibname btrfsutil %{majorutil}
%define devname %mklibname -d btrfs
%global optflags %{optflags} -Oz

%bcond_without docs

Summary:	Userspace programs for btrfs
Name:		btrfs-progs
Version:	6.11
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2
URL:		https://btrfs.wiki.kernel.org/
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}%{?beta:-%{beta}}.tar.xz
# From http://www.spinics.net/lists/linux-btrfs/msg15899.html
Source1:	btrfs-completion.sh
BuildRequires:	pkgconfig(libacl)
BuildRequires:	asciidoc
%if %{with docs}
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
%endif
BuildRequires:	pkgconfig(lzo2)
BuildRequires:	pkgconfig(gdlib)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(python)
BuildRequires:	python3egg(setuptools)
BuildRequires:	python3dist(sphinx)
BuildRequires:	python3dist(sphinx-rtd-theme)
BuildRequires:	systemd-rpm-macros

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package -n %{libname}
Summary:	Library for btrfs
Group:		System/Libraries

%description -n %{libname}
This package contains libraries for creating, checking, modifying and
correcting any inconsistiencies in the btrfs filesystem.

%package -n %{devname}
Summary:	Development headers & libraries for btrfs
Group:		Development/C
Provides:	btrfs-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libutilname} = %{EVRD}

%description -n %{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%package -n %{libutilname}
Summary:	Util library for btrfs
Group:		System/Libraries

%description -n %{libutilname}
This package contains the util library needed to run programs dynamically
linked with btrfs

%prep
%autosetup -n %{name}-v%{version}%{?beta:-%{beta}} -p1

%build
# As of btrfs-progs 6.0, kernel 6.0.2, clang 15.0.2, building
# btrfs-progs with clang results in a hang while upgrading
# kernels and while loading the partitions module in calamares
export CC=gcc
export CXX=g++
export UDEVDIR=%{_udevrulesdir}

# FIXME workaround for crypto bits not compiling with
# SSE4 optimizations (upstream bug as of 6.2.1)
if echo %{optflags} |grep -q msse4; then
	export CFLAGS="%{optflags} -mno-sse4.2 -mno-sse4.1"
fi

./autogen.sh
%configure \
%if !%{with docs}
	--disable-documentation \
%endif
	--enable-zstd

%make_build udevdir="%{_udevrulesdir}"

%install
%make_install

install -p -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/bash-completion/completions/btrfs

# (tpg) somehow makefile does not want to install this
install -m755 -d %{buildroot}%{_udevrulesdir}
install -m644 64-btrfs-dm.rules %{buildroot}%{_udevrulesdir}

%files
%{_bindir}/*
%if %{with docs}
%doc %{_mandir}/man2/btrfs-ioctl.2.*
%doc %{_mandir}/man5/btrfs.5*
%doc %{_mandir}/man8/btrfs.8*
%doc %{_mandir}/man8/btrfs-balance.8*
%doc %{_mandir}/man8/btrfs-convert.8*
%doc %{_mandir}/man8/btrfs-check.8*
%doc %{_mandir}/man8/btrfs-device.8*
%doc %{_mandir}/man8/btrfs-filesystem.8*
%doc %{_mandir}/man8/btrfs-find-root.8*
%doc %{_mandir}/man8/btrfs-image.8*
%doc %{_mandir}/man8/btrfs-inspect-internal.8*
%doc %{_mandir}/man8/btrfs-map-logical.8*
%doc %{_mandir}/man8/btrfs-property.8*
%doc %{_mandir}/man8/btrfs-qgroup.8*
%doc %{_mandir}/man8/btrfs-quota.8*
%doc %{_mandir}/man8/btrfs-receive.8*
%doc %{_mandir}/man8/btrfs-replace.8*
%doc %{_mandir}/man8/btrfs-rescue.8*
%doc %{_mandir}/man8/btrfs-restore.8*
%doc %{_mandir}/man8/btrfs-select-super.8*
%doc %{_mandir}/man8/btrfs-scrub.8*
%doc %{_mandir}/man8/btrfs-send.8*
%doc %{_mandir}/man8/btrfs-subvolume.8*
%doc %{_mandir}/man8/btrfsck.8*
%doc %{_mandir}/man8/btrfstune.8*
%doc %{_mandir}/man8/fsck.btrfs.8*
%doc %{_mandir}/man8/mkfs.btrfs.8*
%endif
%{_datadir}/bash-completion/completions/btrfs
%{_udevrulesdir}/*.rules

%files -n %{libname}
%{_libdir}/libbtrfs.so.%{major}*

%files -n %{libutilname}
%{_libdir}/libbtrfsutil.so.%{majorutil}*

%files -n %{devname}
%doc INSTALL
%{_libdir}/*.so
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*
%{_includedir}/*.h
%{_libdir}/pkgconfig/*
