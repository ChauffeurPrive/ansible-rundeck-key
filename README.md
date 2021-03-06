# Rundeck secret key management module

The `rundeck_key` module has been designed to help up manage our rundeck secret keys through Ansible.

## How to

Here is a simple way to create password kind secret key in rundeck using this module:
```yaml
- name: Create a rundeck key
  rundeck_key:
    url: https://rundeck.foo.bar
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    value: mystrongpassword
    path: foo
```

As you can see, the state default behaviour for the `state` argument is `present`, which that the key will be created if it doesn't exist. But if you want to update or delete a key, you can use the following arguments:
* **update:** Update a key
* **absent:** Delete a key

If you want to create private key instead _(you can also create a public one by the way)_, you can use `type` argument:
```yaml
- name: Create a rundeck key
  rundeck_key:
    url: https://rundeck.foo.bar
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    value: my_super_private_key
    type: private
    path: foo
```

Others exemples:
```yaml
- name: Update an existing rundeck key
  rundeck_key:
    url: https://rundeck.foo.bar
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    value: mynewstrongpassword
    path: foo
    state: update
```
```yaml
- name: Remove rundeck key
  rundeck_key:
    url: https://rundeck.foo.bar
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    path: foo
    state: absent
```
