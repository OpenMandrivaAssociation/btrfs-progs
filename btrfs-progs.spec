%define _root_sbindir	/sbin

%define snapshot 20100412
Name:           btrfs-progs
Version:        0.19
Release:        %mkrel 1.%{snapshot}.0
Summary:        Userspace programs for btrfs

Group:          System/Kernel and hardware
License:        GPLv2
URL:            http://btrfs.wiki.kernel.org/index.php/Main_Page
#Source0:        http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
# git archive --prefix=btrfs-progs-0.19/ -o ../SOURCES/btrfs-progs-0.19-$(date +%Y%m%d).tar --format tar  HEAD
Source0:        %{name}-%{version}-%{snapshot}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

BuildRequires:  e2fsprogs-devel
BuildRequires:  libuuid-devel
BuildRequires:  zlib1-devel
BuildRequires:  acl-devel

%description
The btrfs-progs package provides all the userpsace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%prep
%setup -q

%build
%make CFLAGS="%{optflags}"
# for btrfs-convert
%make convert CFLAGS="%{optflags}"

%install
%makeinstall bindir=%{buildroot}/%{_root_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING INSTALL
%{_root_sbindir}/btrfsctl
%{_root_sbindir}/btrfsck
%{_root_sbindir}/mkfs.btrfs
%{_root_sbindir}/btrfs-debug-tree
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
