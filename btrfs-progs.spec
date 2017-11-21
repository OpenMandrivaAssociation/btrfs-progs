%define major 0
%define libname %mklibname btrfs %{major}
%define devname %mklibname -d btrfs

Summary:	Userspace programs for btrfs
Name:		btrfs-progs
Version:	4.14
Release:	1
Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/btrfs-progs/%{name}-v%{version}.tar.xz
# From http://www.spinics.net/lists/linux-btrfs/msg15899.html
Source1:	btrfs-completion.sh
Patch0:		btrfs-progs-recognize-fsck.btrfs-like-btrfsck.patch
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
BuildRequires:	pkgconfig(libzstd)
BuildRequires:	pkgconfig(libsystemd)

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

%description -n	%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%prep
%setup -qn %{name}-v%{version}
%apply_patches

%build
export UDEVDIR=%{_udevrulesdir}

./autogen.sh
%configure \
	--bindir=/sbin \
	--libdir=/%{_lib} \
	--enable-zstd

%make udevdir="%{_udevrulesdir}"

%install
%makeinstall_std
rm %{buildroot}/%{_lib}/libbtrfs.so
mkdir -p %{buildroot}%{_libdir}
ln -sr %{buildroot}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{_libdir}/libbtrfs.so

install -p -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/bash-completion/completions/btrfs

# (tpg) somehow makefile does not want to install this
install -m755 -d %{buildroot}%{_udevrulesdir}
install -m644 64-btrfs-dm.rules %{buildroot}%{_udevrulesdir}
	
find %{buildroot} -name \*.a -delete

%files
/sbin/btrfs
/sbin/btrfs-convert
/sbin/btrfs-debug-tree
/sbin/btrfs-find-root
/sbin/btrfs-image
/sbin/btrfs-map-logical
/sbin/btrfs-zero-log
/sbin/btrfsck
/sbin/btrfstune
/sbin/btrfs-select-super
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
%{_mandir}/man8/btrfs-select-super.8*
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
%{_udevrulesdir}/64-btrfs-dm.rules

%files -n %{libname}
/%{_lib}/libbtrfs.so.%{major}*

%files -n %{devname}
%doc INSTALL
%{_libdir}/libbtrfs.so
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*
