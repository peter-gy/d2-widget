#!/bin/bash

VERSION=$(grep -m 1 'version = ' pyproject.toml | cut -d '"' -f 2)
git add pyproject.toml
git commit -m "chore: bump version to $VERSION"
git tag -a "v$VERSION" -m "Release v$VERSION"

echo "✅ Version $VERSION tagged"
echo ""
echo "Next steps:"
echo "  1. Push changes:    git push"
echo "  2. Push tags:       git push --tags"
echo "  3. Create release:  gh release create v$VERSION --title $VERSION --generate-notes"
