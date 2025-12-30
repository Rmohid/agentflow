#!/bin/bash
# Create a new feature specification
# Usage: ./create-feature.sh <feature-name>

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <feature-name>"
    echo "Example: $0 user-authentication"
    exit 1
fi

FEATURE_NAME="$1"
SPECS_DIR=".specify/specs"
TEMPLATES_DIR=".specify/templates"

# Find next feature number
LAST_NUM=$(ls -d ${SPECS_DIR}/[0-9]* 2>/dev/null | tail -1 | grep -o '[0-9]\+' | head -1 || echo "-1")
NEXT_NUM=$(printf "%03d" $((LAST_NUM + 1)))

FEATURE_DIR="${SPECS_DIR}/${NEXT_NUM}-${FEATURE_NAME}"

echo "Creating feature: ${FEATURE_DIR}"

mkdir -p "${FEATURE_DIR}"

# Copy templates
cp "${TEMPLATES_DIR}/spec-template.md" "${FEATURE_DIR}/spec.md"
cp "${TEMPLATES_DIR}/plan-template.md" "${FEATURE_DIR}/plan.md"
cp "${TEMPLATES_DIR}/tasks-template.md" "${FEATURE_DIR}/tasks.md"

# Update placeholders
DATE=$(date +%Y-%m-%d)
sed -i.bak "s/\[XXX-feature-name\]/${NEXT_NUM}-${FEATURE_NAME}/g" "${FEATURE_DIR}"/*.md
sed -i.bak "s/\[YYYY-MM-DD\]/${DATE}/g" "${FEATURE_DIR}"/*.md
rm -f "${FEATURE_DIR}"/*.bak

echo "✓ Created feature specification at ${FEATURE_DIR}"
echo ""
echo "Next steps:"
echo "  1. Edit ${FEATURE_DIR}/spec.md - Define requirements"
echo "  2. Edit ${FEATURE_DIR}/plan.md - Design solution"
echo "  3. Edit ${FEATURE_DIR}/tasks.md - Break into tasks"
echo "  4. Implement!"
