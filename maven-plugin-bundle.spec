%{?scl:%scl_package maven-plugin-bundle}
%{!?scl:%global pkg_name %{name}}

%if 0%{?fedora}
%bcond_without obr
%bcond_without reporting
%endif

%global site_name maven-bundle-plugin

Name:           %{?scl_prefix}maven-plugin-bundle
Version:        3.3.0
Release:        1.1%{?dist}
Summary:        Maven Bundle Plugin
License:        ASL 2.0
URL:            http://felix.apache.org
BuildArch:      noarch

Source0:        http://archive.apache.org/dist/felix/%{site_name}-%{version}-source-release.tar.gz

# Needs polishing to be sent upstream
Patch0:         0001-Port-to-current-maven-dependency-tree.patch
# New maven-archiver removed some deprecated methods we were using
Patch1:         0002-Fix-for-new-maven-archiver.patch
# Port to newer Plexus utils
Patch2:         0003-Port-to-plexus-utils-3.0.24.patch
# Port to newer Maven
Patch3:         0004-Use-Maven-3-APIs.patch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(biz.aQute.bnd:biz.aQute.bndlib)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:felix-parent:pom:)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:org.apache.felix.utils)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-archiver)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-compat)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven:maven-core)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.plexus:plexus-utils)
BuildRequires:  %{?scl_prefix}mvn(org.osgi:osgi.core)
BuildRequires:  %{?scl_prefix}mvn(org.sonatype.plexus:plexus-build-api)
%if %{with obr}
BuildRequires:  mvn(net.sf.kxml:kxml2)
BuildRequires:  mvn(org.apache.felix:org.apache.felix.bundlerepository)
BuildRequires:  %{?scl_prefix}mvn(xpp3:xpp3)
%endif
%if %{with reporting}
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-core)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-sink-api)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.doxia:doxia-site-renderer)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.reporting:maven-reporting-impl)
%endif

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

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

find -name '*.jar' -delete

%pom_change_dep :org.osgi.core :osgi.core

# Bundled class from old maven-dependency-tree
rm -r src/main/java/org/apache/maven/shared/dependency

# Bundled classes from old maven
rm -r src/main/java/org/apache/felix/bundleplugin/pom

# There is forked version of maven-osgi in
# src/{main,test}/java/org/apache/maven

%if %{with obr}
# Deps unbundled from felix-bundlerepository
%pom_add_dep xpp3:xpp3
%pom_add_dep net.sf.kxml:kxml2
%else
rm -rf src/main/java/org/apache/felix/obrplugin/
%pom_remove_dep :org.apache.felix.bundlerepository
%endif

%if %{without reporting}
rm -f src/main/java/org/apache/felix/bundleplugin/baseline/BaselineReport.java
%pom_remove_dep :doxia-sink-api
%pom_remove_dep :doxia-site-renderer
%pom_remove_dep :maven-reporting-impl
%endif

%build
# Tests depend on bundled JARs
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 3.3.0-1.1
- Automated package import and SCL-ization

* Wed Mar 29 2017 Michael Simacek <msimacek@redhat.com> - 3.3.0-1
- Update to upstream version 3.3.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Oct 12 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.2.0-3
- Add conditionals for building without OBR or Maven reports

* Thu Oct 06 2016 Michael Simacek <msimacek@redhat.com> - 3.2.0-2
- Use osgi APIs instead of felix-framework

* Tue Jul 19 2016 Michael Simacek <msimacek@redhat.com> - 3.2.0-1
- Update to upstream version 3.2.0

* Thu May 26 2016 Michael Simacek <msimacek@redhat.com> - 3.0.1-4
- Remove aqute downgrade patch

* Thu May 12 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.0.1-3
- Port to plexus-utils 3.0.24

* Thu Apr 14 2016 Mat Booth <mat.booth@redhat.com> - 3.0.1-2
- Fix build against new maven-archiver, which removed some deprecated methods
  that this plugin was using

* Fri Feb 12 2016 Michael Simacek <msimacek@redhat.com> - 3.0.1-1
- Update to upstream version 3.0.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jul 08 2015 Michael Simacek <msimacek@redhat.com> - 2.5.4-1
- Update to upstream version 2.5.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug  4 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-14
- Add build-requires on mockito

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-12
- Update to current packaging guidelines

* Thu Feb 20 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 2.3.7-11
- Remove unneeded R and BR: maven-wagon

* Fri Jul 26 2013 Tomas Radej <tradej@redhat.com> - 2.3.7-10
- Fixed release number

* Wed Jul 17 2013 Tomas Radej <tradej@redhat.com> - 2.3.7-9
- Updated source address (error 404)

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
