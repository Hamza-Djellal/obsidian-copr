#!/usr/bin/env bash
set -euo pipefail

# Obsidian RPM build helper script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERSION=$(grep -E '^Version:' "${SCRIPT_DIR}/obsidian.spec" | awk '{print $2}')
RELEASE=$(grep -E '^Release:' "${SCRIPT_DIR}/obsidian.spec" | awk '{print $2}' | sed 's/%{?dist}//')

X86_URL="https://github.com/obsidianmd/obsidian-releases/releases/download/v${VERSION}/obsidian-${VERSION}.tar.gz"
ARM_URL="https://github.com/obsidianmd/obsidian-releases/releases/download/v${VERSION}/obsidian-${VERSION}-arm64.tar.gz"

X86_FILE="obsidian-${VERSION}.tar.gz"
ARM_FILE="obsidian-${VERSION}-arm64.tar.gz"

download_sources() {
    echo "==> Downloading sources for Obsidian ${VERSION}..."
    if command -v spectool &>/dev/null; then
        spectool -g -R "${SCRIPT_DIR}/obsidian.spec"
    else
        mkdir -p "${SCRIPT_DIR}/sources"
        if [ ! -f "${SCRIPT_DIR}/${X86_FILE}" ]; then
            echo "Downloading ${X86_FILE}..."
            curl -fLC - -o "${SCRIPT_DIR}/${X86_FILE}" "${X86_URL}"
        fi
        if [ ! -f "${SCRIPT_DIR}/${ARM_FILE}" ]; then
            echo "Downloading ${ARM_FILE}..."
            curl -fLC - -o "${SCRIPT_DIR}/${ARM_FILE}" "${ARM_URL}"
        fi
    fi
    echo "==> Sources ready."
}

build_srpm() {
    download_sources
    echo "==> Building Source RPM (SRPM)..."
    rpmbuild -bs \
        --define "_topdir ${SCRIPT_DIR}/rpmbuild" \
        --define "_sourcedir ${SCRIPT_DIR}" \
        "${SCRIPT_DIR}/obsidian.spec"
    echo "==> SRPM created in ${SCRIPT_DIR}/rpmbuild/SRPMS/"
}

build_rpm() {
    download_sources
    echo "==> Building Binary RPM..."
    rpmbuild -ba \
        --define "_topdir ${SCRIPT_DIR}/rpmbuild" \
        --define "_sourcedir ${SCRIPT_DIR}" \
        "${SCRIPT_DIR}/obsidian.spec"
    echo "==> RPM created in ${SCRIPT_DIR}/rpmbuild/RPMS/"
}

clean() {
    echo "==> Cleaning build artifacts..."
    rm -rf "${SCRIPT_DIR}/rpmbuild" "${SCRIPT_DIR}"/*.tar.gz
    echo "==> Clean complete."
}

case "${1:-build}" in
    download)
        download_sources
        ;;
    srpm)
        build_srpm
        ;;
    rpm|build)
        build_rpm
        ;;
    clean)
        clean
        ;;
    *)
        echo "Usage: $0 {download|srpm|rpm|clean}"
        exit 1
        ;;
esac
