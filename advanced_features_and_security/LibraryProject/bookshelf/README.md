# Permissions and Groups Setup

## Custom Permissions

The `Book` model includes custom permissions:
- `can_view`: Can view book
- `can_create`: Can create book
- `can_edit`: Can edit book
- `can_delete`: Can delete book

## Groups

- **Editors**: Assigned `can_create` and `can_edit` permissions.
- **Viewers**: Assigned `can_view` permission.
- **Admins**: Assigned all custom permissions.

## Enforcing Permissions in Views

Permissions are enforced using the `@permission_required` decorator in views.

## Testing

- Create users and assign them to groups.
- Verify that permissions are enforced correctly by attempting various actions.