#!/usr/bin/python

# Copyright: (c) 2018, Julien Jourdain <julien.jourdain@kapten.com>
# Github https://github.com/ChauffeurPrive/ansible-rundeck-key
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: kptn_rundeck_key
short_description: Manage rundeck keys
version_added: "2.8"
description:
    - "This module use rundeck API to manage keys in rundeck key storage."
options:
    url: 
        description:
            - Rundeck URL
        required: true
    token:
        description:
            - API token generated through an existing rundeck account that will be used for the authentication
        required: true
    name:
        description:
            - Rundeck key's name
        required: true
    path:
        description:
            - Rundeck key's parent directory
        required: true
    value:
        description:
            - Rundeck key's value
        required: true
    type:
        description:
            - Rundeck key's type
        default: password
    state:
        description:
            - Rundeck key's state
        default: present
author:
    - Julien Jourdain (@julienjourdain)
'''

EXAMPLES = '''
# Create a key
- name: Create rundeck key
  kptn_rundeck_key:
    url: https://rundeck.local
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    value: mystrongpassword
    path: foo

- name: Update an existing rundeck key
  kptn_rundeck_key:
    url: https://rundeck.local
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    value: mynewstrongpassword
    path: foo
    state: update

- name: Remove rundeck key
  kptn_rundeck_key:
    url: https://rundeck.local
    token: ABCDEFGHIJKLMNOPQRSTUVWXYZ
    name: bar
    path: foo
    state: absent
'''

from ansible.module_utils.basic import AnsibleModule
import requests

def create_key(data):
    r = requests.post("{}/api/11/storage/keys/{}/{}".format(data['url'], data['path'], data['name']), data=data['value'], headers={'X-Rundeck-Auth-Token': data['token'], 'Accept': 'application/json', 'Content-Type': data['type']})
    if r.status_code == 201:
        return False, True, r.json()
    elif r.status_code == 409:
        return False, False, r.json()
    
    # default
    meta = { "status": r.status_code, "response": r.json() }
    return True, False, meta

def update_key(data):
    r = requests.put("{}/api/11/storage/keys/{}/{}".format(data['url'], data['path'], data['name']), data=data['value'], headers={'X-Rundeck-Auth-Token': data['token'], 'Accept': 'application/json', 'Content-Type': data['type']})
    if r.status_code == 200:
        return False, True, r.json()
    elif r.status_code == 404:
        return False, False, r.json()
    
    # default
    meta = { "status": r.status_code, "response": r.json() }
    return True, False, meta

def delete_key(data):
    r = requests.delete("{}/api/11/storage/keys/{}/{}".format(data['url'], data['path'], data['name']), headers={'X-Rundeck-Auth-Token': data['token'], 'Accept': 'application/json'})
    if r.status_code == 204:
        return False, True, {"status": r.status_code, "response": "Key {} has been successfully deleted from keys/{} !".format(data['name'], data['path']) }
    elif r.status_code == 404:
        return False, False, r.json()
    
    # default
    meta = { "status": r.status_code, "response": r.json() }
    return True, False, meta


def run_module():
    fields = {
		"url": {"type": "str", "required": True},
        "token": {"type": "str", "required": True},
        "name": {"type": "str"},
        "path": {"type": "str"},
        "value": {"type": "str"},
        "type": {"type": "str", "default": "password"},
        "state": {"type": "str", "default": "present", "choices": ["absent", "present", "update"]}
	}

    choice_map = {
        "present": create_key,
        "absent": delete_key,
        "update": update_key
    }

    content_type_map = {
        "password": "application/x-rundeck-data-password",
        "private": "application/octet-stream",
        "public": "application/pgp-keys"
    }

    module = AnsibleModule(
        argument_spec=fields,
        required_if=[
            ["state", "absent", ["name", "path"]],
            ["state", "present", ["name", "path", "value"]],
            ["state", "update", ["name", "path", "value"]]
        ]
    )

    module.params['type'] = content_type_map.get(module.params['type'])

    is_error, has_changed, result = choice_map.get(module.params['state'])(module.params)

    if not is_error:
        module.exit_json(changed=has_changed, meta=result)
    else:
        module.fail_json(msg="Error !", meta=result)

def main():
    run_module()

if __name__ == '__main__':
    main()
