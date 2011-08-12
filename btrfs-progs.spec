%define _root_sbindir	/sbin

%define snapshot 20110812
Name:		btrfs-progs
Version:	0.19
Release:	1.%{snapshot}.5
Summary:	Userspace programs for btrfs

Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/index.php/Main_Page
#Source0:	http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
# git archive --prefix=btrfs-progs-0.19/ -o ../SOURCES/btrfs-progs-0.19-$(date +%Y%m%d).tar --format tar  HEAD
Source0:	%{name}-%{version}-%{snapshot}.tar.xz
Patch0:		btrfs-progs-fix-labels.patch
Patch1:		btrfs-progs-build-everything.patch
Patch2:		btrfs-progs-0.19-valgrind.patch
Patch3:		btrfs-progs-0.19-fix-return-value.patch
Patch4:		btrfs-progs-0.19-build-fixes.patch
Patch5:		btrfs-progs-0.19-ignore-standard-fsck-switch.patch

BuildRequires:	e2fsprogs-devel
BuildRequires:	libuuid-devel
BuildRequires:	zlib-devel
BuildRequires:	acl-devel

%description
The btrfs-progs package provides all the userpsace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%prep
%setup -q
%patch0 -p1 -b .labels~
%patch2 -p1 -b .valgrind~
%patch3 -p1 -b .return_value~
%patch4 -p1 -b .build_fixes~
%patch1 -p1 -b .everything~
%patch5 -p1 -b .ignore_switch~

%build
%make CFLAGS="%{optflags} -Wstrict-aliasing=3"
# for btrfs-convert
%make convert CFLAGS="%{optflags} -Wstrict-aliasing=3"

%install
%makeinstall bindir=%{buildroot}/%{_root_sbindir}
ln -sv %{_root_sbindir}/btrfsck %{buildroot}/%{_root_sbindir}/fsck.btrfs 

%files
%doc INSTALL
%{_root_sbindir}/btrfsctl
%{_root_sbindir}/btrfsck
%{_root_sbindir}/btrfstune
%{_root_sbindir}/fsck.btrfs
%{_root_sbindir}/mkfs.btrfs
%{_root_sbindir}/btrfs-debug-tree
%{_root_sbindir}/btrfs-image
%{_root_sbindir}/btrfs-show
%{_root_sbindir}/btrfs-vol
%{_root_sbindir}/btrfs-convert
%{_root_sbindir}/btrfs
%{_root_sbindir}/btrfs-map-logical
%{_mandir}/man8/btrfs-image.8*
%{_mandir}/man8/btrfs-show.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/btrfsctl.8*
%{_mandir}/man8/mkfs.btrfs.8*
%{_mandir}/man8/btrfs.8.*
