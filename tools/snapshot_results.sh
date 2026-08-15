#!/usr/bin/env bash
# Snapshot the frozen analysis artifacts to a checksummed archive.
#
# Every parquet and derived CSV the figure module reads is gitignored, so the whole
# frozen-artifact set lives only in the working tree. The .md summaries and TIER0 hold
# the *record*, and the analysis packages regenerate the artifacts, but regenerating is
# hours of compute and the f>0 flip pattern is only reproducible on the machine that
# produced it (TIER0 §6.4). So the artifacts are worth a copy that is not this disk.
#
#   tools/snapshot_results.sh                     # write to ./snapshots/
#   tools/snapshot_results.sh /mnt/c/backup       # write somewhere else
#   tools/snapshot_results.sh --verify FILE.tar.gz    # check an existing archive
#
# Not included: data/human/Suarez2021_Data (675 MB, third-party published release,
# re-downloadable, provenance in data/human/README.md) and data/human/built_consensus
# (a cache, regenerable via experiments/human/build_consensus.py).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

SOURCES=(
    experiments/human/analysis/results
    experiments/human/analysis/criticality_matched/results
    experiments/human/analysis/eigenspectrum/results
    experiments/human/analysis/phase_diagram/results
)

# --------------------------------------------------------------------- verify mode
if [[ "${1:-}" == "--verify" ]]; then
    archive="${2:?usage: $0 --verify ARCHIVE.tar.gz}"
    echo "Verifying $archive"
    tar -tzf "$archive" >/dev/null
    if [[ -f "${archive}.sha256" ]]; then
        (cd "$(dirname "$archive")" && sha256sum -c "$(basename "$archive").sha256")
    else
        echo "  no sidecar checksum found; archive structure is intact"
    fi
    echo "OK"
    exit 0
fi

# ---------------------------------------------------------------------- write mode
DEST="${1:-$REPO_ROOT/snapshots}"
mkdir -p "$DEST"

stamp="$(date -u +%Y%m%dT%H%M%SZ)"
commit="$(git rev-parse --short HEAD)"
dirty=""
git diff --quiet || dirty="-dirty"
name="results-${stamp}-${commit}${dirty}"
archive="$DEST/${name}.tar.gz"

for path in "${SOURCES[@]}"; do
    [[ -d "$path" ]] || { echo "missing source: $path" >&2; exit 1; }
done

# The manifest travels inside the archive: which commit produced it, what is in it, and
# a per-file checksum, so a restored copy can be proved identical rather than assumed.
manifest="$(mktemp)"
trap 'rm -f "$manifest"' EXIT
{
    echo "snapshot:   $name"
    echo "created:    $stamp"
    echo "commit:     $(git rev-parse HEAD)${dirty}"
    echo "branch:     $(git rev-parse --abbrev-ref HEAD)"
    echo "host:       $(hostname)"
    echo
    echo "sources:"
    for path in "${SOURCES[@]}"; do
        printf '  %-64s %s\n' "$path" "$(du -sh "$path" | cut -f1)"
    done
    echo
    echo "sha256:"
    find "${SOURCES[@]}" -type f -print0 | sort -z | xargs -0 sha256sum | sed 's/^/  /'
} > "$manifest"

n_files=$(grep -c '^  [0-9a-f]\{64\}' "$manifest")
echo "Snapshotting $n_files files from ${#SOURCES[@]} directories -> $archive"

cp "$manifest" MANIFEST.txt
tar -czf "$archive" MANIFEST.txt "${SOURCES[@]}"
rm -f MANIFEST.txt

(cd "$DEST" && sha256sum "$(basename "$archive")" > "$(basename "$archive").sha256")

echo "  archive:  $archive  ($(du -h "$archive" | cut -f1))"
echo "  checksum: ${archive}.sha256"
echo
echo "Verifying the archive just written:"
tar -tzf "$archive" >/dev/null && echo "  structure OK"
(cd "$DEST" && sha256sum -c "$(basename "$archive").sha256")
echo
echo "Off-machine copy, e.g.:"
echo "  rsync -avP $archive ada:/vol/bitbucket/\$USER/snapshots/"
echo "  cp $archive /mnt/c/Users/<you>/OneDrive/"
