%global gem_name diff-lcs

# %%check section needs rspec-expectations, however rspec-expectations depends
# on diff-lcs.
%{!?need_bootstrap:	%global	need_bootstrap	1}

Summary: Provide a list of changes between two sequenced collections
Name: rubygem-%{gem_name}
Version: 1.2.5
Release: 2%{?dist}
Group: Development/Languages
License: MIT and Perl Artistic v2 and GNU GPL v2
URL: http://diff-lcs.rubyforge.org/
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
Requires: ruby(release)
Requires: rubygems
BuildRequires: rubygems-devel
%if 0%{?need_bootstrap} < 1
BuildRequires: rubygem(rspec)
%endif
BuildRequires: ruby(release)
# the following BuildRequires are development dependencies
# BuildRequires: rubygem(rubyforge) >= 2.0.4
# BuildRequires: rubygem(hoe-bundler) >= 1.2
# BuildRequires: rubygem(hoe-bundler) < 2
# BuildRequires: rubygem(hoe-doofus) >= 1.0
# BuildRequires: rubygem(hoe-doofus) < 2
# BuildRequires: rubygem(hoe-gemspec2) >= 1.1
# BuildRequires: rubygem(hoe-gemspec2) < 2
# BuildRequires: rubygem(hoe-git) >= 1.5
# BuildRequires: rubygem(hoe-git) < 2
# BuildRequires: rubygem(hoe-rubygems) >= 1.0
# BuildRequires: rubygem(hoe-rubygems) < 2
# BuildRequires: rubygem(hoe-travis) >= 1.2
# BuildRequires: rubygem(hoe-travis) < 2
# BuildRequires: rubygem(rspec) >= 2.0
# BuildRequires: rubygem(rspec) < 3
# BuildRequires: rubygem(hoe) >= 3.7
# BuildRequires: rubygem(hoe) < 4
BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

%description
Diff::LCS computes the difference between two Enumerable sequences using the
McIlroy-Hunt longest common subsequence (LCS) algorithm. It includes utilities
to create a simple HTML diff output format and a standard diff-like tool.
This is release 1.2.4, fixing a bug introduced after diff-lcs 1.1.3 that did
not properly prune common sequences at the beginning of a comparison set.
Thanks to Paul Kunysch for fixing this issue.
Coincident with the release of diff-lcs 1.2.3, we reported an issue with
Rubinius in 1.9 mode
({rubinius/rubinius#2268}[https://github.com/rubinius/rubinius/issues/2268]).
We are happy to report that this issue has been resolved.


%package doc
Summary: Documentation for %{name}
Group: Documentation

Requires: %{name} = %{version}-%{release}

%description doc
This package contains documentation for %{name}.

%prep
gem unpack %{SOURCE0}

%setup -q -D -T -n  %{gem_name}-%{version}

gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec

%build
# Create the gem as gem install only works on a gem file
gem build %{gem_name}.gemspec

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%gem_install

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/


mkdir -p %{buildroot}%{_bindir}
cp -pa .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%if 0%{?need_bootstrap} < 1
%check
pushd .%{gem_instdir}
rspec spec
popd
%endif

%files
%dir %{gem_instdir}
%{_bindir}/htmldiff
%{_bindir}/ldiff
%{gem_instdir}/.autotest
%exclude %{gem_instdir}/.gemtest
%exclude %{gem_instdir}/.hoerc
%{gem_instdir}/.rspec
%exclude %{gem_instdir}/.travis.yml
%{gem_instdir}/Manifest.txt
%{gem_instdir}/autotest
%{gem_instdir}/bin
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/Contributing.rdoc
%{gem_instdir}/Gemfile
%doc %{gem_instdir}/History.rdoc
%doc %{gem_instdir}/License.rdoc
%doc %{gem_instdir}/README.rdoc
%{gem_instdir}/Rakefile
%doc %{gem_instdir}/docs
%{gem_instdir}/spec

%changelog
* Wed Sep 28 2016 Rich Megginson <rmeggins@redhat.com> - 1.2.5-2
- bump rel to rebuild for rhlog-buildrequires

* Fri Aug 26 2016 Rich Megginson <rmeggins@redhat.com> - 1.2.5-1
- Update to 1.2.5

* Wed Feb 20 2013 Vít Ondruch <vondruch@redhat.com> - 1.1.3-3
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0
- Change the dependency to rubygem(rspec).
- Add bootstrap code.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 17 2012 Vít Ondruch <vondruch@redhat.com> - 1.1.3-1
- Update to diff-lcs 1.1.3.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jan 22 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 1.1.2-7
- Rebuild against ruby 1.9

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-3
- Get rid of duplicate files (thanks to Mamoru Tasaka)

* Mon Jun 08 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-2
- Depend on ruby(abi)
- Replace defines with globals

* Fri Jun 05 2009 Lubomir Rintel (Good Data) <lubo.rintel@gooddata.com> - 1.1.2-1
- Package generated by gem2rpm
- Strip useless shebangs
- Fix up License
