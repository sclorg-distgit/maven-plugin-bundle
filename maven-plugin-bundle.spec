%global pkg_name maven-plugin-bundle
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global site_name maven-bundle-plugin

Name:           %{?scl_prefix}%{pkg_name}
Version:        2.3.7
Release:        12.10%{?dist}
Summary:        Maven Bundle Plugin

License:        ASL 2.0
URL:            http://felix.apache.org
Source0:        http://archive.apache.org/dist/felix/%{site_name}-%{version}-source-release.tar.gz

Patch0:         %{site_name}-dependency.patch
Patch1:         %{site_name}-unreported-exception.patch

BuildRequires: %{?scl_prefix}aqute-bndlib >= 1.50.0
BuildRequires: %{?scl_prefix}plexus-utils >= 1.4.5
BuildRequires: %{?scl_prefix}felix-osgi-obr
BuildRequires: %{?scl_prefix}kxml
BuildRequires: %{?scl_prefix_java_common}maven-local
BuildRequires: %{?scl_prefix}maven-dependency-tree >= 1.1-3
BuildRequires: %{?scl_prefix}maven-compiler-plugin
BuildRequires: %{?scl_prefix}maven-install-plugin
BuildRequires: %{?scl_prefix}maven-jar-plugin
BuildRequires: %{?scl_prefix}maven-javadoc-plugin
BuildRequires: %{?scl_prefix}maven-plugin-plugin
BuildRequires: %{?scl_prefix}maven-resources-plugin
BuildRequires: %{?scl_prefix}maven-surefire-plugin >= 2.3
BuildRequires: %{?scl_prefix}maven-doxia-sitetools
BuildRequires: %{?scl_prefix}maven-osgi
BuildRequires: %{?scl_prefix}maven-archiver
BuildRequires: %{?scl_prefix}maven-plugin-testing-harness
BuildRequires: %{?scl_prefix}plexus-archiver
BuildRequires: %{?scl_prefix}plexus-containers-container-default
BuildRequires: %{?scl_prefix}felix-parent
BuildRequires: %{?scl_prefix}felix-bundlerepository

BuildArch: noarch


%description
Provides a maven plugin that supports creating an OSGi bundle
from the contents of the compilation classpath along with its
resources and dependencies. Plus a zillion other features.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{site_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

%patch0 -p1
%patch1 -p1

# remove bundled stuff
#rm -rf src/main/java/org/apache/maven

%mvn_file : %{pkg_name}
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 2.3.7-12.10
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 2.3.7-12.9
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.8
- Mass rebuild 2014-05-26

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 2.3.7-12.7
- Adjust maven-wagon R/BR

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.5
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.4
- Rebuild to fix incorrect auto-requires

* Fri Feb 14 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.3
- SCL-ize requires and build-requires

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3.7-12
- Mass rebuild 2013-12-27

* Fri Aug 23 2013 Michal Srb <msrb@redhat.com> - 2.3.7-11
- Migrate away from mvn-rpmbuild (Resolves: #997487)

* Wed Jul 17 2013 Tomas Radej <tradej@redhat.com> - 2.3.7-10
- Updated source address (error 404)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-9
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-8
- Add missing BR: maven-plugin-testing-harness

* Mon Mar 11 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-7
- Re-enable tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.3.7-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 21 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.3.7-3
- Add kxml2 to pom as a dependency

* Mon Apr 30 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-2
- Add missing BuildRequires

* Wed Feb 29 2012 Jaromir Capik <jcapik@redhat.com> 2.3.7-1
- Update to 2.3.7

* Thu Jan 19 2012 Jaromir Capik <jcapik@redhat.com> 2.3.6-3
- Bundled maven sources readded (they seem to change the behaviour)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Jaromir Capik <jcapik@redhat.com> 2.3.6-1
- Update to 2.3.6

* Mon Dec 19 2011 Jaromir Capik <jcapik@redhat.com> 2.3.5-3
- Minimal aqute-bndlib VR set to 1.43.0-2 (older ones are broken)

* Mon Nov 14 2011 Jaromir Capik <jcapik@redhat.com> 2.3.5-2
- OBR plugin readded (it's been merged to the bundle plugin)

* Mon Oct 24 2011 Jaromir Capik <jcapik@redhat.com> 2.3.5-1
- Update to 2.3.5

* Tue Oct 17 2011 Jaromir Capik <jcapik@redhat.com> 2.0.0-11
- aqute-bndlib renamed to aqute-bnd

* Fri Jun 17 2011 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-10
- Do not depend on maven2.

* Thu Feb 10 2011 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-9
- BR maven-surefire-provider-junit4.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-7
- BR/R felix-parent.

* Thu Sep 9 2010 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-5
- Fix BuildRequires.

* Fri Sep 18 2009 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-4
- Add missing Requires.

* Wed Sep 9 2009 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-3
- BR doxia-sitetools.

* Mon Sep 7 2009 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-2
- Fix BR/Rs.

* Thu Sep 3 2009 Alexander Kurtakov <akurtako@redhat.com> 2.0.0-1
- Initial import.
