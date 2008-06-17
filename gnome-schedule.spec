%define	version	1.1.0
%define release	%mkrel 2

Summary:	Managing cron job or at job using GUI
Name:		gnome-schedule
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		System/Configuration/Other
URL:		http://gnome-schedule.sourceforge.net/
Source:		http://prdownloads.sourceforge.net/gnome-schedule/%{name}-%{version}.tar.bz2
Patch0:		gnome-schedule-1.1.0_fix_documentation_build.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	pygtk2.0-devel
BuildRequires:	yelp
BuildRequires:	at
BuildRequires:	desktop-file-utils
BuildRequires:  pygtk2.0-libglade gnome-python-devel gnome-python-gconf libxslt-proc
BuildRequires:  gnome-common intltool
Requires:	at
Requires:	pygtk2.0-libglade
Requires:	gnome-python
Requires:	gnome-python-gconf

%description
Gnome-schedule is a tool for managing a users crontab or at jobs
using a GUI. Its key features include:

  * View and edit cron and at jobs in a GUI
  * You can add templates like "Build Kernel" or "Scan for viruses" for
easy reuse of jobs
  * Change other users cron and at jobs if you are root
  * Icons and titles for jobs
  * A human readable text string of cron jobs, to make it easier for
users to understand something like: 5 0 * * *, gnome-schedule translates
it into: At every day at 00:05
  * There is also some predefined common expressions like; every day,
every minute, every week, tomorrow, next week. Depending whether you are
adding a cron job or at job.
  * An advanced view to make it more efficient for the experienced user
to manage his crontabs.
  * A calendar to choose when an at job should be added.

WARNING: This is still a beta release and not ready for user consumption
yet. It is uploaded for software testing. Please submit bug reports to
GNOME bugzilla (bugzilla.gnome.org).

%prep
%setup -q

%patch0 -p1 -b .gnomedoc

%build
#gnome-doc-prepare --force; aclocal; autoconf; automake

%configure2_5x --disable-scrollkeeper
%make


%install
rm -rf %{buildroot}
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std


desktop-file-install --vendor="" \
  --remove-category="Application" \
  --add-category="GNOME" \
  --add-category="GTK" \
  --add-category="X-MandrivaLinux-System-Configuration-Other;Settings" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %name --with-gnome
for omf in %buildroot%_datadir/omf/%name/%name-??*.omf;do
echo "%lang($(basename $omf|sed -e s/%name-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done


%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/*
%{_libdir}/bonobo/servers/GNOME_GnomeSchedule.server
%{_datadir}/omf/%name/*.omf


