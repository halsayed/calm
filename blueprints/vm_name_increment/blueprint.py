# THIS FILE IS AUTOMATICALLY GENERATED.
# Disclaimer: Please test this file before using in production.
"""
Generated blueprint DSL (.py)
"""

import json  # no_qa
import os  # no_qa

from calm.dsl.builtins import *  # no_qa


# Secret Variables
BP_CRED_CENTOS_PASSWORD = read_local_file("BP_CRED_CENTOS_PASSWORD")
Profile_Default_variable_PASSWORD = read_local_file("Profile_Default_variable_PASSWORD")

# Credentials
BP_CRED_CENTOS = basic_cred(
    "centos",
    BP_CRED_CENTOS_PASSWORD,
    name="CENTOS",
    type="PASSWORD",
    default=True,
)


class Service1(Service):

    pass


class calm_project_nameAPP_TYPEVM_IDResources(AhvVmResources):

    memory = 8
    vCPUs = 2
    cores_per_vCPU = 2
    disks = [AhvVmDisk.Disk.Scsi.cloneFromImageService("centos-8.3", bootable=True)]
    nics = [AhvVmNic.NormalNic.ingress("NET-01", cluster="PHX-SPOC017-2")]

    guest_customization = AhvVmGC.CloudInit(
        filename=os.path.join(
            "specs", "calm_project_nameAPP_TYPEVM_ID_cloud_init_data.yaml"
        )
    )


class calm_project_nameAPP_TYPEVM_ID(AhvVm):

    name = "@@{calm_project_name}@@@@{APP_TYPE}@@@@{VM_ID}@@"
    resources = calm_project_nameAPP_TYPEVM_IDResources


class VM1(Substrate):

    os_type = "Linux"
    provider_type = "AHV_VM"
    provider_spec = calm_project_nameAPP_TYPEVM_ID
    provider_spec_editables = read_spec(
        os.path.join("specs", "VM1_create_spec_editables.yaml")
    )
    readiness_probe = readiness_probe(
        connection_type="SSH",
        disabled=True,
        retries="5",
        connection_port=22,
        address="@@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@@",
        delay_secs="60",
        credential=ref(BP_CRED_CENTOS),
    )

    @action
    def __pre_create__():

        CalmTask.SetVariable.escript(
            name="get_next_id",
            filename=os.path.join(
                "scripts", "Substrate_VM1_Action___pre_create___Task_get_next_id.py"
            ),
            target=ref(VM1),
            variables=["VM_ID"],
        )


class Package1(Package):

    services = [ref(Service1)]

    @action
    def __install__():

        CalmTask.Exec.ssh(
            name="enable_web_ui",
            filename=os.path.join(
                "scripts", "Package_Package1_Action___install___Task_enable_web_ui.sh"
            ),
            cred=ref(BP_CRED_CENTOS),
            target=ref(Service1),
        )


class fbfd3b05_deployment(Deployment):

    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(Package1)]
    substrate = ref(VM1)


class Default(Profile):

    deployments = [fbfd3b05_deployment]

    APP_TYPE = CalmVariable.WithOptions(
        ["APP", "SQL", "WWW"],
        label="Application Type",
        default="APP",
        is_mandatory=True,
        is_hidden=False,
        runtime=True,
        description="",
    )

    PASSWORD = CalmVariable.Simple.Secret(
        Profile_Default_variable_PASSWORD,
        label="Password",
        is_mandatory=True,
        is_hidden=False,
        runtime=True,
        description="",
    )

    USERNAME = CalmVariable.Simple(
        "user",
        label="CentOS Root User",
        regex="^[a-z_]([a-z0-9_-]{0,31}|[a-z0-9_-]{0,30}\$)$",
        validate_regex=True,
        is_mandatory=True,
        is_hidden=False,
        runtime=True,
        description="",
    )


class vm_name_increment(Blueprint):
    """CentOS 8.3

    Web UI access: https://@@{VM1.address}@@:9090/"""

    services = [Service1]
    packages = [Package1]
    substrates = [VM1]
    profiles = [Default]
    credentials = [BP_CRED_CENTOS]


class BpMetadata(Metadata):

    categories = {"TemplateType": "Vm"}
