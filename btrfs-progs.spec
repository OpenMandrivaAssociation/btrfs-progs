%define _root_sbindir	/sbin

%define snapshot 20110805
Name:		btrfs-progs
Version:	0.19
Release:	1.%{snapshot}.1
Summary:	Userspace programs for btrfs

Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/index.php/Main_Page
#Source0:	http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
# git archive --prefix=btrfs-progs-0.19/ -o ../SOURCES/btrfs-progs-0.19-$(date +%Y%m%d).tar --format tar  HEAD
Source0:	%{name}-%{version}-%{snapshot}.tar.xz
Patch0:		btrfs-progs-fix-labels.patch
Patch1:		btrfs-progs-0.19-build-everything.patch
Patch3:		btrfs-progs-0.19-fix-return-value.patch
Patch4:		btrfs-progs-0.19-build-fixes.patch
Patch5:		btrfs-progs-0.19-ignore-standard-fsck-switch.patch
Patch6:		btrfs-progs-0.19-recover-chunk.patch
# from suse
Patch7:		btrfs-progs-0.19-plug-memory-leak-in-find_and_setup_log_root.patch
Patch8:		btrfs-progs-0.19-fix-memleak.patch

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
%patch3 -p1 -b .return_value~
%patch4 -p1 -b .build_fixes~
%patch1 -p1 -b .everything~
%patch5 -p1 -b .ignore_switch~
%patch6 -p1 -b .recover_chunk~
%patch7 -p1 -b .plug_memory_luck~
%patch8 -p1 -b .memleak~

%build
%make CFLAGS="%{optflags} -Os -Wstrict-aliasing=3"

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
%{_root_sbindir}/btrfs-convert
%{_root_sbindir}/btrfs-debug-tree
%{_root_sbindir}/btrfs-image
%{_root_sbindir}/btrfs-recover-chunk
%{_root_sbindir}/btrfs-select-super
%{_root_sbindir}/btrfs-show
%{_root_sbindir}/btrfs-vol
%{_root_sbindir}/btrfs-zero-log
%{_root_sbindir}/btrfs
%{_root_sbindir}/btrfs-map-logical
%{_mandir}/man8/btrfs-image.8*
%{_mandir}/man8/btrfs-show.8*
%{_mandir}/man8/btrfsck.8*
%{_mandir}/man8/btrfsctl.8*
%{_mandir}/man8/mkfs.btrfs.8*
%{_mandir}/man8/btrfs.8.*
