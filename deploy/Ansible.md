### Ansible
- orchestration framework
- host manipulation and inventory
- [Ansible] (http://www.ansibleworks.com/tech)


### Why
- almost plain English, utilizes [YAML] (http://en.wikipedia.org/wiki/Yaml)
- runs over SSH, no host-side service required
- Idempotence, fix & re-run possible
- [why Ansible] (http://www.ansibleworks.com/why-ansible/)


### Re-use with Playbooks
- supports tasks grouping into [libraries] (https://github.com/RedHatQE/splice-testing-tools/blob/master/deploy/common/mongodb.yml)
- libraries may be customized with [variable-import] (https://github.com/RedHatQE/splice-testing-tools/blob/master/deploy/master-splice-installer.yml)
- generate configuration files from [jinja templates] (https://github.com/RedHatQE/rhui-testing-tools/blob/with_splice/deploy/rhui/templates/answers.j2)
- even tasks may include some [in-line conde in jinja] (https://github.com/RedHatQE/splice-testing-tools/blob/master/deploy/common/ssh_keygen.yml)

### Host Groups --- Inventory
- group hosts based on roles they perform in an [inventory] (http://www.ansibleworks.com/docs/patterns.html#hosts-and-groups)
- apply tasks in parallel e.g. for all [web servers] (http://www.ansibleworks.com/docs/patterns.html#selecting-targets)
- provide [group-specific variables] (http://www.ansibleworks.com/docs/patterns.html#group-variables)

### Modules
- wide selection of [built-in modules] (http://www.ansibleworks.com/docs/modules.html)
- one can create [custom modules] (http://www.ansibleworks.com/docs/moduledev.html#tutorial)
- any language is supported just mind the output in JSON

### Best practices
- [just check them out] (http://www.ansibleworks.com/docs/bestpractices.html)
