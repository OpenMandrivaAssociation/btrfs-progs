%define major 0
%define libname %mklibname btrfs %{major}
%define majorutil 1
%define libutilname %mklibname btrfsutil %{majorutil}
%define devname %mklibname -d btrfs
%global optflags %{optflags} -Oz
%bcond_without	docs

Summary:	Userspace programs for btrfs
Name:		btrfs-progs
Version:	5.4.1
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz
# From http://www.spinics.net/lists/linux-btrfs/msg15899.html
Source1:	btrfs-completion.sh
BuildRequires:	acl-devel
BuildRequires:	asciidoc
%if %{with docs}
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	xmlto
%endif
BuildRequires:	lzo-devel
BuildRequires:	gd-devel
BuildRequires:	jpeg-devel
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
BuildRequires:	systemd-macros

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package -n %{libname}
Summary:	Library for btrfs
Group:		System/Libraries

%description -n	%{libname}
This package contains libraries for creating, checking, modifying and
correcting any inconsistiencies in the btrfs filesystem.

%package -n %{devname}
Summary:	Development headers & libraries for btrfs
Group:		Development/C
Provides:	btrfs-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{libutilname} = %{EVRD}

%description -n	%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%package -n     %{libutilname}
Summary:	Util library for btrfs
Group:		System/Libraries

%description -n %{libutilname}
This package contains the util library needed to run programs dynamically
linked with btrfs

%prep
%autosetup -n %{name}-v%{version} -p1

%build
export UDEVDIR=%{_udevrulesdir}

./autogen.sh
%configure \
	--bindir=/sbin \
	--libdir=/%{_lib} \
%if !%{with docs}
	--disable-documentation \
%endif
	--enable-zstd

%make_build udevdir="%{_udevrulesdir}"

%install
%make_install
rm -f %{buildroot}/%{_lib}/libbtrfs.so
rm -f %{buildroot}/%{_lib}/libbtrfsutil.so

mkdir -p %{buildroot}%{_libdir}
ln -sr %{buildroot}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{_libdir}/libbtrfs.so
ln -sr %{buildroot}/%{_lib}/libbtrfsutil.so.%{majorutil}.* %{buildroot}%{_libdir}/libbtrfsutil.so

install -p -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/bash-completion/completions/btrfs

# (tpg) somehow makefile does not want to install this
install -m755 -d %{buildroot}%{_udevrulesdir}
install -m644 64-btrfs-dm.rules %{buildroot}%{_udevrulesdir}

find %{buildroot} -name \*.a -delete

%files
/sbin/btrfs
/sbin/btrfs-convert
/sbin/btrfs-find-root
/sbin/btrfs-image
/sbin/btrfs-map-logical
/sbin/btrfsck
/sbin/btrfstune
/sbin/btrfs-select-super
/sbin/fsck.btrfs
/sbin/mkfs.btrfs
%if %{with docs}
%{_mandir}/man5/btrfs.5*
%{_mandir}/man8/btrfs.8*
%{_mandir}/man8/btrfs-balance.8*
%{_mandir}/man8/btrfs-convert.8*
%{_mandir}/man8/btrfs-check.8*
%{_mandir}/man8/btrfs-device.8*
%{_mandir}/man8/btrfs-filesystem.8*
%{_mandir}/man8/btrfs-find-root.8*
%{_mandir}/man8/btrfs-image.8*
%{_mandir}/man8/btrfs-inspect-internal.8*
%{_mandir}/man8/btrfs-map-logical.8*
%{_mandir}/man8/btrfs-property.8*
%{_mandir}/man8/btrfs-qgroup.8*
%{_mandir}/man8/btrfs-quota.8*
%{_mandir}/man8/btrfs-receive.8*
%{_mandir}/man8/btrfs-replace.8*
%{_mandir}/man8/btrfs-rescue.8*
%{_mandir}/man8/btrfs-restore.8*
%{_mandir}/man8/btrfs-select-super.8*
%{_mandir}/man8/btrfs-scrub.8*
%{_mandir}/man8/btrfs-send.8*
%{_mandir}/man8/btrfs-subvolume.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/btrfstune.8*
%{_mandir}/man8/fsck.btrfs.8*
%{_mandir}/man8/mkfs.btrfs.8*
%endif
%{_datadir}/bash-completion/completions/btrfs
%{_udevrulesdir}/64-btrfs-dm.rules

%files -n %{libname}
/%{_lib}/libbtrfs.so.%{major}*

%files -n %{libutilname}
/%{_lib}/libbtrfsutil.so.%{majorutil}*

%files -n %{devname}
%doc INSTALL
%{_libdir}/*.so
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*
%{_includedir}/*.h
