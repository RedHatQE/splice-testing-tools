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
- supports tasks grouping into [libraries] (https://github.com/RedHatQE/splice-testing-tools/blob/master/deploy/common/iptables_ports.yml)
- [customize imports by variables] (https://github.com/RedHatQE/splice-testing-tools/blob/master/deploy/splice-installer.yml)
- generate configuration files from [jinja templates] (https://github.com/RedHatQE/rhui-testing-tools/blob/with_splice/deploy/rhui/templates/answers.j2)

### Host Groups --- Inventory
- group hosts based on roles they perform in an [inventory] (http://www.ansibleworks.com/docs/patterns.html#hosts-and-groups)
- apply tasks in parallel e.g. for all [web servers] (http://www.ansibleworks.com/docs/patterns.html#selecting-targets)
- provide [group-specific variables] (http://www.ansibleworks.com/docs/patterns.html#group-variables)
