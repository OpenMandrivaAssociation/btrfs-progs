%define major 0
%define libname %mklibname btrfs %{major}
%define devname %mklibname -d btrfs

Summary:	Userspace programs for btrfs
Name:		btrfs-progs
Version:	4.4.1
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/
Source0:	https://github.com/kdave/btrfs-progs/archive/%{name}-%{version}.tar.gz
# From http://www.spinics.net/lists/linux-btrfs/msg15899.html
Source1:	btrfs-completion.sh
Patch0:		btrfs-progs-recognize-fsck.btrfs-like-btrfsck.patch
Patch1:		btrfs-init-dev-list.patch
Patch2:		btrfs-progs-v4.0.1-build-extra_progs-rule.patch
# use nftw rather than obsolescent ftw call
Patch3:		btrfs-progs-v4.0.1-nftw.patch
BuildRequires:	acl-devel
BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
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

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package extra
Summary:	Additional userspace programs for btrfs
Group:		System/Kernel and hardware

%description extra
This package contains the following extra btrfs utils:
* btrfs-calc-size
* btrfs-corrupt-block
* btrfs-fragments
* btrfs-select-super

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

%description -n	%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%prep
%setup -q
%apply_patches

%build
./autogen.sh
%configure \
	--bindir=/sbin \
	--libdir=/%{_lib}

%make CFLAGS="%{optflags} -include config.h -DBTRFS_FLAT_INCLUDES -D_XOPEN_SOURCE=700" LDFLAGS="%{ldflags}"

%install
%makeinstall_std install-extra
install -m755 btrfs-select-super btrfs-calc-size btrfs-corrupt-block %{buildroot}/sbin

rm %{buildroot}/%{_lib}/libbtrfs.so
mkdir -p %{buildroot}%{_libdir}
ln -sr %{buildroot}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{_libdir}/libbtrfs.so

install -p -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/bash-completion/completions/btrfs

find %{buildroot} -name \*.a -delete

%files
%doc INSTALL
/sbin/btrfs
/sbin/btrfs-convert
/sbin/btrfs-debug-tree
/sbin/btrfs-find-root
/sbin/btrfs-image
/sbin/btrfs-map-logical
/sbin/btrfs-show-super
/sbin/btrfs-zero-log
/sbin/btrfsck
/sbin/btrfstune
/sbin/fsck.btrfs
/sbin/mkfs.btrfs
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
/sbin/btrfs-calc-size
/sbin/btrfs-corrupt-block
/sbin/btrfs-fragments
/sbin/btrfs-select-super

%files -n %{libname}
/%{_lib}/libbtrfs.so.%{major}*

%files -n %{devname}
%{_libdir}/libbtrfs.so
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*
