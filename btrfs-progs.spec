%bcond_without uclibc

%define _root_sbindir /sbin

%define major 0
%define libname %mklibname btrfs %{major}
%define devname %mklibname -d btrfs

Name:		btrfs-progs
Version:	3.17.3
Release:	1
Summary:	Userspace programs for btrfs

Group:		System/Kernel and hardware
License:	GPLv2
URL:            http://btrfs.wiki.kernel.org/
Source0:	https://www.kernel.org/pub/linux/kernel/people/kdave/%{name}/%{name}-v%{version}.tar.xz
# From http://www.spinics.net/lists/linux-btrfs/msg15899.html
Source1:        btrfs-completion.sh
Patch0:		btrfs-progs-recognize-fsck.btrfs-like-btrfsck.patch
Patch1:		btrfs-init-dev-list.patch

BuildRequires:	acl-devel
BuildRequires:	lzo-devel
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(zlib)
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

%description
The btrfs-progs package provides all the userspace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.
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
%endif

%package -n	%{devname}
Summary:	Development headers & libraries for btrfs
Group:		Development/C
Provides:	btrfs-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif

%description -n	%{devname}
This package contains headers & libraries for developing programs to create,
check, modify or correct any inconsistiencies in the btrfs filesystem.

%prep
%setup -q -n %{name}-v%{version}
%patch0 -p1 -b .fsck~
%patch1 -p1 -b .initdevlst~

%if %{with uclibc}
mkdir -p .uclibc
cp -a * .uclibc
%endif

%build
%make CC=%{__cc} Q= CFLAGS="%{optflags} -Os -Wstrict-aliasing=3" LDFLAGS="%{ldflags}"
%if %{with uclibc}
%make Q= CC=%{uclibc_cc} CFLAGS="%{uclibc_cflags} -Wstrict-aliasing=3" LDFLAGS="%{ldflags}" -C .uclibc
%endif


%install
%makeinstall bindir=%{buildroot}%{_root_sbindir}

#ln -f %{buildroot}%{_root_sbindir}/btrfs %{buildroot}%{_root_sbindir}/btrfsck
#ln -sv %{_root_sbindir}/btrfsck %{buildroot}%{_root_sbindir}/fsck.btrfs 
rm %{buildroot}%{_libdir}/libbtrfs.so
mkdir -p %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/libbtrfs.so.%{major}* %{buildroot}/%{_lib}
ln -sr %{buildroot}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{_libdir}/libbtrfs.so

%if %{with uclibc}
%makeinstall bindir=%{buildroot}%{uclibc_root}%{_root_sbindir} libdir=%{buildroot}%{uclibc_root}%{_libdir} -C .uclibc

#ln -f %{buildroot}%{uclibc_root}%{_root_sbindir}/btrfs %{buildroot}%{uclibc_root}%{_root_sbindir}/btrfsck
#ln -sv %{uclibc_root}%{_root_sbindir}/btrfsck %{buildroot}%{uclibc_root}%{_root_sbindir}/fsck.btrfs 
rm %{buildroot}%{uclibc_root}%{_libdir}/libbtrfs.so
mkdir -p %{buildroot}%{uclibc_root}/%{_lib}
mv %{buildroot}%{uclibc_root}%{_libdir}/libbtrfs.so.%{major}* %{buildroot}%{uclibc_root}/%{_lib}
ln -sr %{buildroot}%{uclibc_root}/%{_lib}/libbtrfs.so.%{major}.* %{buildroot}%{uclibc_root}%{_libdir}/libbtrfs.so
%endif

install -p -m644 %{SOURCE1} -D %{buildroot}%{_datadir}/bash-completion/completions/btrfs

%files
%doc INSTALL
%{_root_sbindir}/btrfs
%{_root_sbindir}/btrfs-convert
%{_root_sbindir}/btrfs-debug-tree
%{_root_sbindir}/btrfs-find-root
%{_root_sbindir}/btrfs-image
%{_root_sbindir}/btrfs-map-logical
%{_root_sbindir}/btrfs-zero-log
%{_root_sbindir}/btrfsck
%{_root_sbindir}/btrfstune
%{_root_sbindir}/btrfs-show-super
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

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_root_sbindir}/btrfs
%{uclibc_root}%{_root_sbindir}/btrfs-convert
%{uclibc_root}%{_root_sbindir}/btrfs-debug-tree
%{uclibc_root}%{_root_sbindir}/btrfs-find-root
%{uclibc_root}%{_root_sbindir}/btrfs-image
%{uclibc_root}%{_root_sbindir}/btrfs-map-logical
%{uclibc_root}%{_root_sbindir}/btrfs-zero-log
%{uclibc_root}%{_root_sbindir}/btrfsck
%{uclibc_root}%{_root_sbindir}/btrfstune
%{uclibc_root}%{_root_sbindir}/btrfs-show-super
%{uclibc_root}%{_root_sbindir}/fsck.btrfs
%{uclibc_root}%{_root_sbindir}/mkfs.btrfs
%endif

%files -n %{libname}
/%{_lib}/libbtrfs.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%{uclibc_root}/%{_lib}/libbtrfs.so.%{major}*
%endif

%files -n %{devname}
%{_libdir}/libbtrfs.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/libbtrfs.so
%attr(644,root,root) %{uclibc_root}%{_libdir}/libbtrfs.a
%endif
%attr(644,root,root) %{_libdir}/libbtrfs.a
%dir %{_includedir}/btrfs
%{_includedir}/btrfs/*

%changelog
* Thu May 31 2012 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.19-1.20120328.2
+ Revision: 801614
- fix ignore options patch

