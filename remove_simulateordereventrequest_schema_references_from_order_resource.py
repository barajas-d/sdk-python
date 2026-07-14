#!/usr/bin/env python3
"""Migration script: Remove SimulateOrderEventRequest schema references from Order resource.

This script removes or updates any references to the SimulateOrderEventRequest
schema in mercadopago/resources/order.py. This schema was used by the event
simulation method that has been removed from the SDK.

The script performs the following checks and removals:
1. Removes imports of SimulateOrderEventRequest if present
2. Removes any method that uses SimulateOrderEventRequest as a parameter type
3. Removes references to the schema in docstrings
4. Updates any type hints that reference the schema

This is a cleanup operation following the removal of the simulate_event method.
"""

import os
import re
import sys


def remove_simulateordereventrequest_references():
    """Remove SimulateOrderEventRequest schema references from order.py."""
    order_file_path = os.path.join(
        os.path.dirname(__file__), "mercadopago", "resources", "order.py"
    )

    if not os.path.exists(order_file_path):
        print(f"Error: File not found: {order_file_path}")
        return False

    with open(order_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original_content = content
    changes_made = []

    # 1. Remove import statements for SimulateOrderEventRequest
    import_patterns = [
        r"from mercadopago\.resources\.order_simulate_event import SimulateOrderEventRequest\n",
        r"from mercadopago\.resources\.order_simulate_event import \([\s\S]*?SimulateOrderEventRequest[\s\S]*?\)\n",
        r"import mercadopago\.resources\.order_simulate_event\n",
    ]

    for pattern in import_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, "", content)
            changes_made.append(f"Removed import matching pattern: {pattern[:50]}...")

    # 2. Remove any method signatures or type hints using SimulateOrderEventRequest
    # This includes parameter types, return types, and variable annotations
    type_hint_pattern = r": ?SimulateOrderEventRequest"
    if re.search(type_hint_pattern, content):
        content = re.sub(type_hint_pattern, "", content)
        changes_made.append("Removed type hints for SimulateOrderEventRequest")

    # 3. Remove docstring references to SimulateOrderEventRequest
    docstring_pattern = r"(:class:`)?SimulateOrderEventRequest(`)?|``SimulateOrderEventRequest``"
    if re.search(docstring_pattern, content):
        content = re.sub(docstring_pattern, "event simulation request object", content)
        changes_made.append("Removed docstring references to SimulateOrderEventRequest")

    # 4. Look for any simulate_event method and remove it
    # This method would have been the primary consumer of SimulateOrderEventRequest
    simulate_method_pattern = (
        r"    def simulate_event\([\s\S]*?\n(?=    def |\Z)"
    )
    if re.search(simulate_method_pattern, content):
        content = re.sub(simulate_method_pattern, "", content)
        changes_made.append("Removed simulate_event method")

    # 5. Remove any validation logic specific to SimulateOrderEventRequest
    validation_pattern = r"if not isinstance\([^,]+, SimulateOrderEventRequest\):[\s\S]*?\n"
    if re.search(validation_pattern, content):
        content = re.sub(validation_pattern, "", content)
        changes_made.append("Removed validation for SimulateOrderEventRequest")

    # 6. Clean up multiple consecutive blank lines (formatting cleanup)
    content = re.sub(r"\n{3,}", "\n\n", content)

    # Check if any changes were made
    if content == original_content:
        print("✓ No SimulateOrderEventRequest references found in order.py")
        print("  The file is already clean.")
        return True

    # Write the updated content back to the file
    with open(order_file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("✓ Successfully removed SimulateOrderEventRequest references from order.py")
    print("\nChanges made:")
    for change in changes_made:
        print(f"  - {change}")

    return True


def main():
    """Execute the migration script."""
    print("=" * 70)
    print("Migration: Remove SimulateOrderEventRequest schema references")
    print("=" * 70)
    print()

    success = remove_simulateordereventrequest_references()

    print()
    print("=" * 70)
    if success:
        print("Migration completed successfully!")
        return 0
    else:
        print("Migration failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())