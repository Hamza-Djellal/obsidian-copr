%global debug_package %{nil}
%global __strip /bin/true

Name:           obsidian
Version:        1.14.5
Release:        1%{?dist}
Summary:        Obsidian - A powerful knowledge base on top of local Markdown files

License:        Commercial
URL:            https://obsidian.md
Source0:        https://github.com/obsidianmd/obsidian-releases/releases/download/v%{version}/obsidian-%{version}.tar.gz
Source1:        https://github.com/obsidianmd/obsidian-releases/releases/download/v%{version}/obsidian-%{version}-arm64.tar.gz
Source2:        obsidian.desktop

ExclusiveArch:  x86_64 aarch64
AutoReqProv:    no

BuildRequires:  desktop-file-utils

Requires:       alsa-lib
Requires:       cairo
Requires:       cups-libs
Requires:       dbus-libs
Requires:       expat
Requires:       glib2
Requires:       gtk3
Requires:       hicolor-icon-theme
Requires:       libX11
Requires:       libXcomposite
Requires:       libXcursor
Requires:       libXdamage
Requires:       libXext
Requires:       libXfixes
Requires:       libXi
Requires:       libXrandr
Requires:       libXrender
Requires:       libXtst
Requires:       libdrm
Requires:       libxcb
Requires:       libxshmfence
Requires:       mesa-libgbm
Requires:       nspr
Requires:       nss
Requires:       pango
Requires:       systemd-libs
Requires:       zlib

%description
Obsidian is a powerful and extensible knowledge base that works on top of a local
folder of plain text Markdown files. It lets you take notes, link concepts,
and build a personal wiki with bidirectional links and graph visualization.

%prep
%ifarch x86_64
%setup -q -n obsidian-%{version} -T -b 0
%endif
%ifarch aarch64
%setup -q -n obsidian-%{version}-arm64 -T -b 1
%endif

%build
# Pre-compiled Electron binary application; no compilation necessary.

%install
# Create application directories
install -d -m 0755 %{buildroot}%{_datadir}/obsidian
install -d -m 0755 %{buildroot}%{_bindir}
install -d -m 0755 %{buildroot}%{_datadir}/applications
install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/512x512/apps

# Copy bundled application files
cp -a * %{buildroot}%{_datadir}/obsidian/

# Clean up unwanted desktop files if bundled in the tarball
rm -f %{buildroot}%{_datadir}/obsidian/obsidian.desktop

# Fix executable permissions
chmod 0755 %{buildroot}%{_datadir}/obsidian/obsidian
if [ -f %{buildroot}%{_datadir}/obsidian/obsidian-cli ]; then
    chmod 0755 %{buildroot}%{_datadir}/obsidian/obsidian-cli
    ln -sf ../share/obsidian/obsidian-cli %{buildroot}%{_bindir}/obsidian-cli
fi
if [ -f %{buildroot}%{_datadir}/obsidian/chrome-sandbox ]; then
    chmod 4755 %{buildroot}%{_datadir}/obsidian/chrome-sandbox 2>/dev/null || chmod 0755 %{buildroot}%{_datadir}/obsidian/chrome-sandbox
fi

# Main binary symlink
ln -sf ../share/obsidian/obsidian %{buildroot}%{_bindir}/obsidian

# Install desktop entry
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    %{SOURCE2}

# Install application icon
install -D -p -m 0644 resources/icon.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/obsidian.png

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/obsidian.desktop

%post
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%postun
/usr/bin/update-desktop-database &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE.electron.txt LICENSES.chromium.html
%{_bindir}/obsidian
%{_bindir}/obsidian-cli
%{_datadir}/obsidian/
%{_datadir}/applications/obsidian.desktop
%{_datadir}/icons/hicolor/512x512/apps/obsidian.png

%changelog
* Thu Oct 29 2026 Hamza <user@example.com> - 1.14.5-1
- Initial Fedora Copr package for Obsidian 1.14.5
