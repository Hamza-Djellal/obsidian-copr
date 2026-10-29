# Obsidian for Fedora

[![Build RPM & Copr CI/CD](https://github.com/Hamza-Djellal/obsidian-copr/actions/workflows/build-rpm.yml/badge.svg)](https://github.com/Hamza-Djellal/obsidian-copr/actions/workflows/build-rpm.yml)
[![Copr Repository](https://img.shields.io/badge/Fedora%20Copr-hamz4%2Fobsidian-blue)](https://copr.fedorainfracloud.org/coprs/hamz4/obsidian/)

Native RPM packaging and automated CI/CD for **[Obsidian](https://obsidian.md)** on Fedora Linux.

---

## Installation

Enable the Copr repository and install Obsidian with `dnf`:

```bash
sudo dnf copr enable hamz4/obsidian
sudo dnf install obsidian
```

To update when a new version is released:

```bash
sudo dnf upgrade obsidian
```

---

## Features

- **Multi-Architecture Support**: Built for both `x86_64` (Intel/AMD) and `aarch64` (ARM64).
- **Desktop & URI Integration**:
  - Full desktop launcher (`md.obsidian.Obsidian.desktop`).
  - Registers the `obsidian://` protocol handler (`x-scheme-handler/obsidian`).
  - Associates with Markdown files (`text/markdown`).
- **CLI Support**: Installs `/usr/bin/obsidian-cli` alongside `/usr/bin/obsidian`.
- **Clean Packaging**: Excludes internal bundled Electron libraries from RPM provides/requires to avoid conflicts with system libraries.
- **Automated Upstream Tracking**: Daily CI/CD workflow checks for new upstream releases on GitHub and builds updated RPMs automatically.

---

## Local Building

If you prefer to build the RPM locally:

```bash
# Install packaging dependencies
sudo dnf install -y rpm-build desktop-file-utils curl

# Build RPM
make rpm

# Install generated package
sudo dnf install rpmbuild/RPMS/x86_64/obsidian-*.rpm
```

---

## Disclaimer & Licensing

- **Obsidian** is proprietary software developed by Dynalist Inc. and distributed under the [Obsidian Terms of Service](https://obsidian.md/terms).
- This repository contains packaging scripts and CI/CD automation only; no proprietary binaries are stored in Git.
