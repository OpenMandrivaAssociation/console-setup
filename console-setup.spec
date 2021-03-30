%global optflags %{optflags} -Oz

Summary:	Tools for configuring the console using X Window System key maps
Name:		console-setup
Version:	1.201
Release:	1
Group:		Terminals
# For a breakdown of the licensing, see COPYRIGHT, copyright, copyright.fonts and copyright.xkb
License:	GPLv2+ and MIT and Public Domain
Url:		http://packages.debian.org/cs/sid/console-setup
Source0:	http://ftp.de.debian.org/debian/pool/main/c/%{name}/%{name}_%{version}.tar.xz
# Fixes installing paths to Fedora style
Patch0:		console-setup-1.76-paths.patch
# Fixes FSF address, sent to upstream
Patch1:		console-setup-1.76-fsf-address.patch
BuildRequires:	perl
BuildRequires:	perl(encoding)
BuildRequires:	pigz
BuildArch:	noarch
Requires:	kbd
# require 'xkeyboard-config' to have X Window keyboard descriptions?

%description
This package provides the console with the same keyboard configuration
scheme that X Window System has. Besides the keyboard, the package configures
also the font on the console.  It includes a rich collection of fonts and
supports several languages that would be otherwise unsupported on the console
(such as Armenian, Georgian, Lao and Thai).

%prep
%autosetup -p1

%build
%make_build build-linux

%install
make prefix="%{buildroot}" install-linux
# we don't want another set of keyboard descriptions, we want to use descriptions from
# xkeyboard-config (require it?), so removing it
# or maybe have these from tarball it in optional subpackage?
rm -rf %{buildroot}/etc/console-setup

# Make systemd happy by using standard paths
mkdir -p %{buildroot}/lib/kbd
mv %{buildroot}%{_datadir}/consolefonts %{buildroot}%{_datadir}/consoletrans %{buildroot}/lib/kbd/
ln -s ../../lib/kbd/consolefonts %{buildroot}%{_datadir}/consolefonts
ln -s ../../lib/kbd/consoletrans %{buildroot}%{_datadir}/consoletrans

# Nasty workaround for rpm being unable to replace directories with symlinks
# Changed to a symlink in 1.189-1 before the Lx4 release.
# Scriptlet can be dropped once we stop supporting upgrading from Lx3.
%pretrans -p <lua>
st = posix.stat("%{_datadir}/consolefonts")
if st and st.type == "directory" then
  os.execute("rm -rf %{_datadir}/consolefonts %{_datadir}/consoletrans")
end

%files
%doc README COPYRIGHT CHANGES copyright.fonts copyright.xkb Fonts/copyright
%{_bindir}/ckbcomp
%{_bindir}/setupcon
%config(noreplace) %{_sysconfdir}/default/console-setup
%config(noreplace) %{_sysconfdir}/default/keyboard
/lib/kbd/consolefonts/*
/lib/kbd/consoletrans/*
%{_datadir}/consolefonts
%{_datadir}/consoletrans
%{_mandir}/*/*
