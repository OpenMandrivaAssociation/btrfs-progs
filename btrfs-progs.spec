%bcond_with uclibc

%define _root_sbindir /sbin

%define major 0
%define libname %mklibname btrfs %{major}
%define devname %mklibname -d btrfs

Name:		btrfs-progs
Version:	4.0.1
Release:	4
Summary:	Userspace programs for btrfs

Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/%{name}/%{name}-v%{version}.tar.xz
# From http://www.spinics.net/lists/linux-btrfs/msg15899.html
Source1:	btrfs-completion.sh
Patch0:		btrfs-progs-recognize-fsck.btrfs-like-btrfsck.patch
Patch1:		btrfs-init-dev-list.patch
Patch2:		btrfs-progs-v4.0.1-build-extra_progs-rule.patch
# use nftw rather than obsolescent ftw call
Patch3:		btrfs-progs-v4.0.1-nftw.patch
BuildRequires:	acl-devel
BuildRequires:	asciidoc
BuildRequires:	lzo-devel
BuildRequires:	gd-devel
BuildRequires:	jpeg-devel
BuildRequires:	xmlto
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(zlib)
%if %{with uclibc}
BuildRequires:	uClibc-devel
BuildRequires:	uclibc-acl-devel
BuildRequires:	uclibc-lzo-devel
BuildRequires:	uclibc-jpeg-devel
BuildRequires:	uclibc-libblkid-devel
BuildRequires:	uclibc-ext2fs-devel
BuildRequires:	uclibc-libuuid-devel
BuildRequires:	uclibc-zlib-devel
%endif

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package	extra
Summary:	Additional userspace programs for btrfs
Group:		System/Kernel and hardware

%description	extra
This package contains the following extra btrfs utils:
* btrfs-calc-size
* btrfs-corrupt-block
* btrfs-fragments
* btrfs-select-super

%if %{with uclibc}
%package -n	uclibc-%{name}
Summary:	Userspace programs for btrfs (uClibc build)
Group:		System/Kernel and hardware

%description -n uclibc-%{name}
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.
%endif

%package -n	%{libname}
Summary:	Library for btrfs
Group:		System/Libraries

%description -n	%{libname}
This package contains libraries for creating, checking, modifying and
correcting any inconsistiencies in the btrfs filesystem.

%if %{with uclibc}
%package -n	uclibc-%{libname}
Summary:	Library for btrfs (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains libraries for creating, checking, modifying and
correcting any inconsistiencies in the btrfs filesystem.

%package -n	uclibc-%{devname}
Summary:	Development headers & libraries for btrfs
Group:		Development/C
Provides:	uclibc-btrfs-devel = %{EVRD}
Requires:	%{devname} = %{EVRD}
Requires:	uclibc-%{libname} = %{EVRD}
Conflicts:		%{devname} < 4.0.1-2

%description -n	uclibc-%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.
%endif

%package -n	%{devname}
Summary:	Development headers & libraries for btrfs
Group:		Development/C
Provides:	btrfs-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}

%description -n	%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%prep
%setup -q -n %{name}-v%{version}
%apply_patches

%if %{with uclibc}
mkdir -p .uclibc
cp -a * .uclibc
%endif

%build
%if %{with uclibc}
pushd .uclibc
CFLAGS="%{uclibc_cflags} -Wstrict-aliasing=3" \
%uclibc_configure	--bindir=%{uclibc_root}%{_root_sbindir} \
			--libdir=%{uclibc_root}/%{_lib} \
			--disable-documentation
%make V=1 all btrfs-select-super btrfs-calc-size btrfs-corrupt-block
popd
%endif

CFLAGS="%{optflags} -Wstrict-aliasing=3" \
%configure		--bindir=%{_root_sbindir} \
			--libdir=/%{_lib}
%make V=1 all extra

%install
%makeinstall_std install-extra
install -m755 btrfs-select-super btrfs-calc-size btrfs-corrupt-block %{buildroot}%{_root_sbindir}

rm %{buildroot}/%{_lib}/libbtrfs.so
mkdir -p %{buildroot}%{_libdir}
ln -sr %{buildroot}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{_libdir}/libbtrfs.so

%if %{with uclibc}
%makeinstall_std -C .uclibc
install -m755 btrfs-select-super btrfs-calc-size btrfs-corrupt-block %{buildroot}%{uclibc_root}%{_root_sbindir}
rm %{buildroot}%{uclibc_root}/%{_lib}/libbtrfs.so
mkdir -p %{buildroot}%{uclibc_root}%{_libdir}
ln -sr %{buildroot}%{uclibc_root}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libbtrfs.so
%endif

install -p -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/bash-completion/completions/btrfs

find %{buildroot} -name \*.a -delete

%files
%doc INSTALL
%{_root_sbindir}/btrfs
%{_root_sbindir}/btrfs-convert
%{_root_sbindir}/btrfs-debug-tree
%{_root_sbindir}/btrfs-find-root
%{_root_sbindir}/btrfs-image
%{_root_sbindir}/btrfs-map-logical
%{_root_sbindir}/btrfs-show-super
%{_root_sbindir}/btrfs-zero-log
%{_root_sbindir}/btrfsck
%{_root_sbindir}/btrfstune
%{_root_sbindir}/fsck.btrfs
%{_root_sbindir}/mkfs.btrfs
%{_mandir}/man5/btrfs.5*
%{_mandir}/man8/btrfs.8*
%{_mandir}/man8/btrfs-balance.8*
%{_mandir}/man8/btrfs-convert.8*
%{_mandir}/man8/btrfs-check.8*
%{_mandir}/man8/btrfs-debug-tree.8*
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
%{_mandir}/man8/btrfs-scrub.8*
%{_mandir}/man8/btrfs-send.8*
%{_mandir}/man8/btrfs-show-super.8*
%{_mandir}/man8/btrfs-subvolume.8*
%{_mandir}/man8/btrfs-zero-log.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/btrfstune.8*
%{_mandir}/man8/fsck.btrfs.8*
%{_mandir}/man8/mkfs.btrfs.8*
%{_datadir}/bash-completion/completions/btrfs

%files extra
%{_root_sbindir}/btrfs-calc-size
%{_root_sbindir}/btrfs-corrupt-block
%{_root_sbindir}/btrfs-fragments
%{_root_sbindir}/btrfs-select-super

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_root_sbindir}/btrfs
%{uclibc_root}%{_root_sbindir}/btrfs-calc-size
%{uclibc_root}%{_root_sbindir}/btrfs-convert
%{uclibc_root}%{_root_sbindir}/btrfs-corrupt-block
%{uclibc_root}%{_root_sbindir}/btrfs-debug-tree
%{uclibc_root}%{_root_sbindir}/btrfs-find-root
%{uclibc_root}%{_root_sbindir}/btrfs-image
%{uclibc_root}%{_root_sbindir}/btrfs-map-logical
%{uclibc_root}%{_root_sbindir}/btrfs-select-super
%{uclibc_root}%{_root_sbindir}/btrfs-show-super
%{uclibc_root}%{_root_sbindir}/btrfs-zero-log
%{uclibc_root}%{_root_sbindir}/btrfsck
%{uclibc_root}%{_root_sbindir}/btrfstune
%{uclibc_root}%{_root_sbindir}/fsck.btrfs
%{uclibc_root}%{_root_sbindir}/mkfs.btrfs
%endif

%files -n %{libname}
/%{_lib}/libbtrfs.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libbtrfs.so.%{major}*

%files -n uclibc-%{devname}
%{uclibc_root}%{_libdir}/libbtrfs.so
%endif

%files -n %{devname}
%{_libdir}/libbtrfs.so
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*
