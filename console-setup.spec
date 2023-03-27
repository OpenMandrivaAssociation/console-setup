# (tpg) optimize it a bit
%global optflags %{optflags} -Oz --rtlib=compiler-rt

Summary:	Tools for configuring the console using X Window System key maps
Name:		console-setup
Version:	1.218
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
BuildRequires:	perl(open)
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

%pretrans -p <lua>
-- Used to be symlinks to /lib/kbd/console{fonts,trans}
posix.unlink("%{_datadir}/consolefonts")
posix.unlink("%{_datadir}/consoletrans")

%files
%doc README COPYRIGHT CHANGES copyright.fonts copyright.xkb Fonts/copyright
%{_bindir}/ckbcomp
%{_bindir}/setupcon
%config(noreplace) %{_sysconfdir}/default/console-setup
%config(noreplace) %{_sysconfdir}/default/keyboard
%{_datadir}/consolefonts
%{_datadir}/consoletrans
%doc %{_mandir}/*/*
