data "google_client_openid_userinfo" "me" {
    # email ="gonzalobenitounlu@gmail.com"
}

terraform {
    required_providers {
        google = {
            source = "hashicorp/google"
            version = "4.51.0"
        }
    }
}

provider "google" {
    credentials = file(var.credentials_file_path)
    project = var.project_id
    region  = var.region
    zone = var.zone
}

resource "google_compute_instance" "vm_instance" {
    count        = var.num_instances
    name         = "worker-${count.index+1}-tp4-h2"
    machine_type = "e2-small"
    zone         = var.zone

    scheduling {
        preemptible                 = true
        automatic_restart           = false
        provisioning_model          = "SPOT"
        instance_termination_action = "TERMINATE"
    }

    boot_disk {
        initialize_params {
            image = "ubuntu-os-cloud/ubuntu-2004-lts"
        }
    }

    network_interface {
        network = "default"
        access_config {
        // Ephemeral IP
        }
    }

    metadata = {
        ssh-keys = "${split("@", data.google_client_openid_userinfo.me.email)[0]}:${tls_private_key.ssh.public_key_openssh}"
        # user_data = file("${path.module}/script.sh")
    }

    metadata_startup_script = file(var.metadata_startup_script)
}