#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	GN - meta-build system that generates build files for Ninja
Summary(pl.UTF-8):	GN - meta-system budowania generujący pliki dla narzędzia Ninja
Name:		gn
%define	snap	20201223
# git -C gn describe HEAD --match initial-commit
%define	gitdesc	initial-commit-1876-g0d67e272
Version:	0
Release:	0.%{snap}.1
License:	BSD
Group:		Development/Tools
# git clone https://gn.googlesource.com/gn
# tar cJf gn-%{snap}.tar.xz --exclude .git gn
Source0:	%{name}-%{snap}.tar.xz
# Source0-md5:	44a1bd6239e96ee902d60202c79aa82d
URL:		https://gn.googlesource.com/gn
BuildRequires:	libstdc++-devel
BuildRequires:	python3 >= 1:3
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GN is a meta-build system that generates build files for Ninja
(<https://ninja-build.org/>).

%description -l pl.UTF-8
GN to meta-system budowania, generujący pliki dla systemu budowania
Ninja (<https://ninja-build.org/>).

%prep
%setup -q -n %{name}

PY_CFLAGS="$(echo "%{rpmcflags}" | sed -e 's/  / /g' | sed -e "s/ /','/")"
%{__sed} \
	-e '/describe_output = subprocess.check_output(/,/cwd=REPO_ROOT)/ d' \
	-e "s/describe_output.decode()/'%{gitdesc}'/" \
	-i build/gen.py

%build
CXX="%{__cxx}" \
CXXFLAGS="%{rpmcxxflags}" \
LDFLAGS="%{rpmldflags}" \
%{__python3} build/gen.py \
	--no-static-libstdc++

%ninja_build -C out

%if %{with tests}
out/gn_unittests
%endif

%install
rm -rf $RPM_BUILD_ROOT

install -Dp out/gn $RPM_BUILD_ROOT%{_bindir}/gn

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE OWNERS README.md
%attr(755,root,root) %{_bindir}/gn
