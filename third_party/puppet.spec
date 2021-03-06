%{!?ruby_sitelibdir: %define ruby_sitelibdir %(ruby -rrbconfig -e 'puts Config::CONFIG["sitelibdir"]')}
%define pbuild %{_builddir}/../third_party/%{name}-%{version}
%define confdir conf/suse

%if 0%{?_buildTag:1}
%define         _relstr      %{_buildTag}
%else
%define         _relstr      %(date -u +%y%m%d%H%M)
%endif
%{echo: "Building release %{_relstr}\n"}

Summary: Puppet Agent %{?_gitVer}
Name:    puppet
Version: 2.7.20
Release: %{_relstr}
License: Apache 2.0
Group:   Productivity/Networking/System

Source0: git_root

BuildArch: noarch
Requires: ruby >= 1.8.2
Requires: facter >= 1.5
Requires: cronie
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: ruby >= 1.8.2

%description
Puppet lets you centrally manage every important aspect of your system using a 
cross-platform specification language that manages all the separate elements 
normally aggregated in different files, like users, cron jobs, and hosts, 
along with obviously discrete elements like packages, services, and files.

%package server
Group:    Productivity/Networking/System
Summary: Puppet Server %{?_gitVer}
Requires: puppet = %{version}-%{release}

%description server
Provides the central puppet server daemon which provides manifests to clients.
The server can also function as a certificate authority and file server.

%prep
##pushd %{_builddir}/..
##pushd third_party/%{name}-%{version}
##%setup -D -T -n %{name}-%{version}


%install
pushd %{_builddir}/..
pushd third_party/%{name}-%{version}
%{__install} -d -m0755 %{buildroot}%{_sbindir}
%{__install} -d -m0755 %{buildroot}%{_bindir}
%{__install} -d -m0755 %{buildroot}%{_confdir}
%{__install} -d -m0755 %{buildroot}%{ruby_sitelibdir}
%{__install} -d -m0755 %{buildroot}%{_sysconfdir}/puppet/manifests
%{__install} -d -m0755 %{buildroot}%{_docdir}/%{name}-%{version}
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/lib/puppet
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/run/puppet
%{__install} -d -m0755 %{buildroot}%{_localstatedir}/log/puppet
%{__install} -d -m0755 %{buildroot}/opt/contrail/puppet
%{__install} -d -m0755 %{buildroot}/opt/contrail/puppet/store
%{__install} -Dp -m0755 %{pbuild}/bin/* %{buildroot}%{_bindir}
%{__install} -Dp -m0755 %{pbuild}/sbin/* %{buildroot}%{_sbindir}
%{__install} -Dp -m0644 %{pbuild}/lib/puppet.rb %{buildroot}%{ruby_sitelibdir}/puppet.rb
%{__install} -Dp -m0644 %{pbuild}/lib/semver.rb %{buildroot}%{ruby_sitelibdir}/semver.rb
%{__cp} -a %{pbuild}/lib/puppet %{buildroot}%{ruby_sitelibdir}
find %{buildroot}%{ruby_sitelibdir} -type f -perm +ugo+x -exec chmod a-x '{}' \;
%{__cp} -a %{pbuild}/conf/redhat/client.sysconfig %{buildroot}%{_confdir}/client.sysconfig
%{__install} -Dp -m0644 %{buildroot}%{_confdir}/client.sysconfig %{buildroot}/var/adm/fillup-templates/sysconfig.puppet
%{__cp} -a %{pbuild}/conf/redhat/server.sysconfig %{buildroot}%{_confdir}/server.sysconfig
%{__install} -Dp -m0644 %{buildroot}%{_confdir}/server.sysconfig %{buildroot}/var/adm/fillup-templates/sysconfig.puppetmaster
%{__cp} -a %{pbuild}/conf/redhat/fileserver.conf %{buildroot}%{_confdir}/fileserver.conf
%{__install} -Dp -m0644 %{buildroot}%{_confdir}/fileserver.conf %{buildroot}%{_sysconfdir}/puppet/fileserver.conf
%{__cp} -a %{pbuild}/conf/redhat/puppet.conf %{buildroot}%{_confdir}/puppet.conf
%{__install} -Dp -m0644 %{buildroot}%{_confdir}/puppet.conf %{buildroot}%{_sysconfdir}/puppet/puppet.conf
%{__cp} -a %{pbuild}/conf/redhat/logrotate %{buildroot}%{_confdir}/logrotate
%{__install} -Dp -m0644 %{buildroot}%{_confdir}/logrotate %{buildroot}%{_sysconfdir}/logrotate.d/puppet
%{__install} -Dp -m0644 %{pbuild}/puppetagent.service %{buildroot}/usr/lib/systemd/system/puppetagent.service
%{__install} -Dp -m0644 %{pbuild}/puppetmaster.service %{buildroot}/usr/lib/systemd/system/puppetmaster.service
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/setup-pki.sh %{buildroot}/opt/contrail/puppet/setup-pki.sh
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/pupp_const.py %{buildroot}/opt/contrail/puppet/pupp_const.py
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/pupp_config_init.py %{buildroot}/opt/contrail/puppet/pupp_config_init.py
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/pupp_cmn.py %{buildroot}/opt/contrail/puppet/pupp_cmn.py
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/pupp_sqlite.py %{buildroot}/opt/contrail/puppet/pupp_sqlite.py
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/example.json %{buildroot}/opt/contrail/puppet/example.json
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/example-1.json %{buildroot}/opt/contrail/puppet/example-1.json
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/schema_trans.erb %{buildroot}/opt/contrail/puppet/store/schema_trans.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/quantum_server.erb %{buildroot}/opt/contrail/puppet/store/quantum_server.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/ctrl_details_template.erb %{buildroot}/opt/contrail/puppet/store/ctrl_details_template.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/control_conf.erb %{buildroot}/opt/contrail/puppet/store/control_conf.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/compute-server-setup.erb %{buildroot}/opt/contrail/puppet/store/compute-server-setup.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/api_server_template.erb %{buildroot}/opt/contrail/puppet/store/api_server_template.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/service.token %{buildroot}/opt/contrail/puppet/store/service.token
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/contrail_all_init.pp %{buildroot}/opt/contrail/puppet/store/contrail_all_init.pp
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/agent_conf_template.erb %{buildroot}/opt/contrail/puppet/store/agent_conf_template.erb
%{__install} -Dp -m0644 %{pbuild}/ext/contrail/store/agent_conf.py %{buildroot}/opt/contrail/puppet/store/agent_conf.py

%files
%defattr(-, root, root, 0755)
%{_bindir}/puppet
%{_bindir}/puppetdoc
%{_bindir}/filebucket
%{_bindir}/ralsh
%{_bindir}/pi
%{_sbindir}/puppetd
%{ruby_sitelibdir}/*
/var/adm/fillup-templates/sysconfig.puppet
%config(noreplace) %{_sysconfdir}/puppet/puppet.conf
##%doc CHANGELOG LICENSE README.md examples
%config(noreplace) %{_sysconfdir}/logrotate.d/puppet
%dir %{_sysconfdir}/puppet
/usr/lib/systemd/system/puppetagent.service
# These need to be owned by puppet so the server can
# write to them
%attr(-, puppet, puppet) %{_localstatedir}/run/puppet
%attr(-, puppet, puppet) %{_localstatedir}/log/puppet
%attr(-, puppet, puppet) %{_localstatedir}/lib/puppet

%files server
%defattr(-, root, root, 0755)
%{_sbindir}/puppetmasterd
%{_sbindir}/puppetqd
%{_sbindir}/puppetrun
%{_sbindir}/puppetca
%config(noreplace) %{_sysconfdir}/puppet/*
%exclude %{_sysconfdir}/puppet/puppet.conf
/var/adm/fillup-templates/sysconfig.puppetmaster
%dir %{_sysconfdir}/puppet
/usr/lib/systemd/system/puppetmaster.service
/opt/contrail/puppet/setup-pki.sh
/opt/contrail/puppet/pupp_const.py
/opt/contrail/puppet/pupp_config_init.py
/opt/contrail/puppet/pupp_cmn.py
/opt/contrail/puppet/pupp_sqlite.py
/opt/contrail/puppet/pupp_const.pyc
/opt/contrail/puppet/pupp_config_init.pyc
/opt/contrail/puppet/pupp_cmn.pyc
/opt/contrail/puppet/pupp_sqlite.pyc
/opt/contrail/puppet/pupp_const.pyo
/opt/contrail/puppet/pupp_config_init.pyo
/opt/contrail/puppet/pupp_cmn.pyo
/opt/contrail/puppet/pupp_sqlite.pyo
/opt/contrail/puppet/example.json
/opt/contrail/puppet/example-1.json
/opt/contrail/puppet/store/schema_trans.erb
/opt/contrail/puppet/store/quantum_server.erb
/opt/contrail/puppet/store/ctrl_details_template.erb
/opt/contrail/puppet/store/control_conf.erb
/opt/contrail/puppet/store/compute-server-setup.erb
/opt/contrail/puppet/store/api_server_template.erb
/opt/contrail/puppet/store/service.token
/opt/contrail/puppet/store/contrail_all_init.pp
/opt/contrail/puppet/store/agent_conf_template.erb
/opt/contrail/puppet/store/agent_conf.py
/opt/contrail/puppet/store/agent_conf.pyc
/opt/contrail/puppet/store/agent_conf.pyo

%pre
/usr/sbin/groupadd -r puppet 2>/dev/null || :
/usr/sbin/useradd -g puppet -c "Puppet" \
    -s /sbin/nologin -r -d /var/puppet puppet 2> /dev/null || :

#%post
#%{fillup_and_insserv -y puppet}

#%post server
#%{fillup_and_insserv -n -y puppetmaster}

#%preun
#%stop_on_removal puppet

#%preun server
#%stop_on_removal puppetmaster

#%postun
#%restart_on_update puppet
#%{insserv_cleanup}

#%postun server
#%restart_on_update puppetmaster
#%{insserv_cleanup}

%clean
%{__rm} -rf %{buildroot}

%changelog
* Wed May 02 2012 Moses Mendoza <moses@puppetlabs.com> - 2.7.14-1
- Update for 2.7.14

* Mon Mar 12 2012 Michael Stahnke <stahnma@puppetlabs.com> - 2.7.12-1
- Update for 2.7.12

* Wed Jan 25 2012 Michael Stahnke <stahnma@puppetlabs.com> - 2.7.10-1
- Update for 2.7.10

* Wed Nov 30 2011 Michael Stahnke <stahnma@puppetlabs.com> - 2.7.8-0.1rc1
- Update for 2.7.8rc1

* Mon Nov 21 2011 Michael Stahnke <stahnma@puppetlabs.com> - 2.7.7-1
- Release 2.7.7

* Wed Jul 06 2011 Michael Stahnke <stahnma@puppetlabs.com> - 2.7.2-0.1rc1
- Updating to 2.7.2rc1

* Tue Sep 14 2010 Ben Kevan <ben.kevan@gmail.com> - 2.6.1
- New version to 2.6.1
- Add client.init and server.init from source since it's now included in the packages
- Change BuildRequires Ruby version to match Requires Ruby version
- Removed ruby-env patch, replaced with sed in prep
- Update urls to puppetlabs.com

* Wed Jul 21 2010 Ben Kevan <ben.kevan@gmail.com> - 2.6.0
- New version and ruby version bump
- Add puppetdoc to %_bindir (unknown why original suse package, excluded or forgot to add)
- Corrected patch for ruby environment
- Move binaries back to the correct directories

* Wed Jul 14 2010 Ben Kevan <ben.kevan@gmail.com> - 0.25.5
- New version.
- Use original client, server.init names
- Revert to puppetmaster
- Fixed client.init and server.init and included $null and Should-Stop for both

* Tue Mar 2 2010 Martin Vuk  <martin.vuk@fri.uni-lj.si> - 0.25.4
- New version.

* Sun Aug 9 2009 Noah Fontes <nfontes@transtruct.org>
- Fix build on SLES 9.
- Enable puppet and puppet-server services by default.

* Sat Aug 8 2009 Noah Fontes <nfontes@transtruct.org>
- Fix a lot of relevant warnings from rpmlint.
- Build on OpenSUSE 11.1 correctly.
- Rename puppetmaster init scripts to puppet-server to correspond to the package name.

* Wed Apr 22 2009 Leo Eraly  <leo@unstable.be> - 0.24.8
- New version.

* Tue Dec 9 2008 Leo Eraly  <leo@unstable.be> - 0.24.6
- New version.

* Fri Sep 5 2008 Leo Eraly  <leo@unstable.be> - 0.24.5
- New version.

* Fri Jun 20 2008 Martin Vuk  <martin.vuk@fri.uni-lj.si> - 0.24.4
- Removed symlinks to old configuration files

* Fri Dec 14 2007 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.24.0
- New version.

* Fri Jun  29 2007 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.23.0
- New version.

* Wed May  2 2007 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.22.4
- New version. Includes provider for rug package manager.

* Wed Apr 25  2007 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.22.3
- New version. Added links /sbin/rcpuppet and /sbin/rcpuppetmaster

* Sun Jan  7  2007 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.22.0
- version bump

* Tue Oct  3  2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.19.3-3
- Made package arch dependant.

* Sat Sep 23  2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.19.3-1
- New version

* Sun Sep 17  2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.19.1-1
- New version

* Tue Aug  30 2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.19.0-1
- New version
- No need to patch anymore :-), since my changes went into official release.

* Tue Aug  3 2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.18.4-3
- Replaced puppet-bin.patch with %build section from David's spec

* Tue Aug  1 2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.18.4-2
- Added supprot for enabling services in SuSE
 
* Tue Aug  1 2006 Martin Vuk <martin.vuk@fri.uni-lj.si> - 0.18.4-1
- New version and support for SuSE

* Wed Jul  5 2006 David Lutterkort <dlutter@redhat.com> - 0.18.2-1
- New version

* Wed Jun 28 2006 David Lutterkort <dlutter@redhat.com> - 0.18.1-1
- Removed lsb-config.patch and yumrepo.patch since they are upstream now

* Mon Jun 19 2006 David Lutterkort <dlutter@redhat.com> - 0.18.0-1
- Patch config for LSB compliance (lsb-config.patch)
- Changed config moves /var/puppet to /var/lib/puppet, /etc/puppet/ssl 
  to /var/lib/puppet, /etc/puppet/clases.txt to /var/lib/puppet/classes.txt,
  /etc/puppet/localconfig.yaml to /var/lib/puppet/localconfig.yaml

* Fri May 19 2006 David Lutterkort <dlutter@redhat.com> - 0.17.2-1
- Added /usr/bin/puppetrun to server subpackage
- Backported patch for yumrepo type (yumrepo.patch)

* Wed May  3 2006 David Lutterkort <dlutter@redhat.com> - 0.16.4-1
- Rebuilt

* Fri Apr 21 2006 David Lutterkort <dlutter@redhat.com> - 0.16.0-1
- Fix default file permissions in server subpackage
- Run puppetmaster as user puppet
- rebuilt for 0.16.0

* Mon Apr 17 2006 David Lutterkort <dlutter@redhat.com> - 0.15.3-2
- Don't create empty log files in post-install scriptlet

* Fri Apr  7 2006 David Lutterkort <dlutter@redhat.com> - 0.15.3-1
- Rebuilt for new version

* Wed Mar 22 2006 David Lutterkort <dlutter@redhat.com> - 0.15.1-1
- Patch0: Run puppetmaster as root; running as puppet is not ready 
  for primetime

* Mon Mar 13 2006 David Lutterkort <dlutter@redhat.com> - 0.15.0-1
- Commented out noarch; requires fix for bz184199

* Mon Mar  6 2006 David Lutterkort <dlutter@redhat.com> - 0.14.0-1
- Added BuildRequires for ruby

* Wed Mar  1 2006 David Lutterkort <dlutter@redhat.com> - 0.13.5-1
- Removed use of fedora-usermgmt. It is not required for Fedora Extras and
  makes it unnecessarily hard to use this rpm outside of Fedora. Just
  allocate the puppet uid/gid dynamically

* Sun Feb 19 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-4
- Use fedora-usermgmt to create puppet user/group. Use uid/gid 24. Fixed 
problem with listing fileserver.conf and puppetmaster.conf twice

* Wed Feb  8 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-3
- Fix puppetd.conf

* Wed Feb  8 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-2
- Changes to run puppetmaster as user puppet

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 0.13.0-1
- Don't mark initscripts as config files

* Mon Feb  6 2006 David Lutterkort <dlutter@redhat.com> - 0.12.0-2
- Fix BuildRoot. Add dist to release

* Tue Jan 17 2006 David Lutterkort <dlutter@redhat.com> - 0.11.0-1
- Rebuild

* Thu Jan 12 2006 David Lutterkort <dlutter@redhat.com> - 0.10.2-1
- Updated for 0.10.2 Fixed minor kink in how Source is given

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-3
- Added basic fileserver.conf

* Wed Jan 11 2006 David Lutterkort <dlutter@redhat.com> - 0.10.1-1
- Updated. Moved installation of library files to sitelibdir. Pulled 
initscripts into separate files. Folded tools rpm into server

* Thu Nov 24 2005 Duane Griffin <d.griffin@psenterprise.com>
- Added init scripts for the client

* Wed Nov 23 2005 Duane Griffin <d.griffin@psenterprise.com>
- First packaging
