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

resource "google_compute_network" "vpc_network" {
    name = "terraform-network"
}

resource "google_compute_instance" "vm_instance" {
    count        = var.num_instances
    name         = "my-instance-${count.index}"
    machine_type = "e2-medium"
    zone         = var.zone

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

resource "google_compute_firewall" "allow-http-https-ssh" {
    name    = "allow-http-https-ssh"
    network = "default"

    allow {
        protocol = "tcp"
        ports    = ["22", "80", "443"]
    }

    source_ranges = ["0.0.0.0/0"]
}
