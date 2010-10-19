#
# Conditional build:
%bcond_with	tests		# perform "make test"
#
%include	/usr/lib/rpm/macros.perl
%define	pdir	TheSchwartz
Summary:	TheSchwartz - reliable job queue
#Summary(pl.UTF-8):	
Name:		perl-TheSchwartz
Version:	1.07
Release:	1
# same as perl
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://search.cpan.org/CPAN/authors/id/B/BR/BRADFITZ/%{pdir}-%{version}.tar.gz
# Source0-md5:	c5c4c2a0c8a43f2c5e698e8d849f2382
URL:		http://search.cpan.org/dist/TheSchwartz/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	perl(Data::ObjectDriver) >= 0.04
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
TheSchwartz is a reliable job queue system. Your application can put jobs into
the system, and your worker processes can pull jobs from the queue atomically
to perform. Failed jobs can be left in the queue to retry later.

Abilities specify what jobs a worker process can perform. Abilities are the
names of TheSchwartz::Worker subclasses, as in the synopsis: the MyWorker
class name is used to specify that the worker script can perform the job. When
using the TheSchwartz client's work functions, the class-ability duality
is used to automatically dispatch to the proper class to do the actual work.

TheSchwartz clients will also prefer to do jobs for unused abilities before
reusing a particular ability, to avoid exhausting the supply of one kind of job
while jobs of other types stack up.

Some jobs with high setup times can be performed more efficiently if a group of
related jobs are performed together. TheSchwartz offers a facility to
coalesce jobs into groups, which a properly constructed worker can find and
perform at once. For example, if your worker were delivering email, you might
store the domain name from the recipient's address as the coalescing value. The
worker that grabs that job could then batch deliver all the mail for that
domain once it connects to that domain's mail server.



# %description -l pl.UTF-8
# TODO

%prep
%setup -q -n %{pdir}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES doc extras
%attr(755,root,root) %{_bindir}/schwartzmon
%{perl_vendorlib}//*.pm
%{perl_vendorlib}/TheSchwartz/
%{_mandir}/man3/*
