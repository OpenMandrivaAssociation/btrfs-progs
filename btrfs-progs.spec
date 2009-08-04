%define _root_sbindir	/sbin

Name:           btrfs-progs
Version:        0.18
Release:        %mkrel 3
Summary:        Userspace programs for btrfs

Group:          System/Kernel and hardware
License:        GPLv2
URL:            http://btrfs.wiki.kernel.org/index.php/Main_Page
Source0:        http://www.kernel.org/pub/linux/kernel/people/mason/btrfs/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

BuildRequires:  libuuid-devel
BuildRequires:  zlib1-devel
BuildRequires:  acl-devel

%description
The btrfs-progs package provides all the userpsace programs needed to create,
check, modify and correct any inconsistencies in the btrfs filesystem.

%prep
%setup -q

%build
%make
# for btrfs-convert
%make convert

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
%{_root_sbindir}/btrfs-image
%{_root_sbindir}/btrfstune
