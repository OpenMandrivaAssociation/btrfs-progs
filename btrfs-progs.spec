%define _root_sbindir	/sbin

%define	major	0
%define	libname	%mklibname btrfs %{major}
%define	devname	%mklibname -d btrfs

%define	gitdate	20130313
Name:		btrfs-progs
Version:	0.20
Release:	0.%{gitdate}.1
Summary:	Userspace programs for btrfs

Group:		System/Kernel and hardware
License:	GPLv2
URL:		http://btrfs.wiki.kernel.org/
#Source0:	http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/mason/btrfs-progs.git
# git archive --prefix=btrfs-progs-0.19/ --format tar  HEAD | xz > ../SOURCES/btrfs-progs-0.19-$(date +%Y%m%d).tar.xz
Source0:	%{name}-%{version}-%{gitdate}.tar.xz
Patch0:		btrfs-progs-fix-labels.patch
Patch1:		btrfs-progs-0.20-20130313-build-everything.patch
Patch3:		btrfs-progs-0.19-fix-return-value.patch
Patch4:		btrfs-progs-0.19-build-fixes.patch
Patch5:		btrfs-progs-0.19-20120328-ignore-standard-fsck-switch.patch
# do NOT enable
Patch6:		btrfs-progs-0.19-20120328-recover-chunk.patch
# from suse
Patch7:		btrfs-progs-0.19-plug-memory-leak-in-find_and_setup_log_root.patch
Patch8:		btrfs-progs-0.19-fix-memleak.patch
Patch9:		btrfs-progs-0.19-ignore-deleted-loopmounts.patch

BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	acl-devel

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%package -n	%{libname}
Summary:	Library for btrfs
Group:		System/Libraries

%description -n	%{libname}
This package contains libraries for creating, checking, modifying and
correcting any inconsistiencies in the btrfs filesystem.

%package -n	%{devname}
Summary:	Development headers & libraries for btrfs
Group:		Development/C

%description -n	%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%prep
%setup -q
#patch0 -p1 -b .labels~
%patch3 -p1 -b .return_value~
#patch4 -p1 -b .build_fixes~
%patch1 -p1 -b .everything~
#patch5 -p1 -b .ignore_switch~
#patch6 -p1 -b .recover_chunk~
#patch7 -p1 -b .plug_memory_luck~
#patch8 -p1 -b .memleak~
%patch9 -p1 -b .ignore_del_loopmnts~

%build
%make CFLAGS="%{optflags} -Os -Wstrict-aliasing=3"

%install
%makeinstall bindir=%{buildroot}%{_root_sbindir}
ln -sv %{_root_sbindir}/btrfsck %{buildroot}%{_root_sbindir}/fsck.btrfs 
rm %{buildroot}%{_libdir}/libbtrfs.so
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libbtrfs.so.%{major}* %{buildroot}/%{_lib}
ln -sr %{buildroot}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{_libdir}/libbtrfs.so

%files
%doc INSTALL
%{_root_sbindir}/btrfsctl
%{_root_sbindir}/btrfsck
%{_root_sbindir}/btrfstune
%{_root_sbindir}/fsck.btrfs
%{_root_sbindir}/mkfs.btrfs
%{_root_sbindir}/btrfs-calc-size
%{_root_sbindir}/btrfs-convert
%{_root_sbindir}/btrfs-corrupt-block
%{_root_sbindir}/btrfs-debug-tree
%{_root_sbindir}/btrfs-find-root
%{_root_sbindir}/btrfs-image
#%{_root_sbindir}/btrfs-recover-chunk
#%{_root_sbindir}/btrfs-restore
%{_root_sbindir}/btrfs-select-super
%{_root_sbindir}/btrfs-show
%{_root_sbindir}/btrfs-show-super
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

%files -n %{libname}
/%{_lib}/libbtrfs.so.%{major}*

%files -n %{devname}
%{_libdir}/libbtrfs.so
%{_libdir}/libbtrfs.a
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*

%changelog
* Thu May 31 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.19-1.20120328.2
+ Revision: 801614
- fix ignore options patch

