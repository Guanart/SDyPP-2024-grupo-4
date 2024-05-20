data "google_client_openid_userinfo" "me" {}

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
    name = "terraform-network-tp4-h2"
}

resource "google_compute_instance" "tp4-h2-services-app" {
    count        = var.num_instances
    name         = "tp4-h2-services-app"
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

resource "google_compute_firewall" "allow-http-https-ssh-rabbit" {
    name    = "allow-http-https-ssh-rabbit"
    network = "default"

    allow {
        protocol = "tcp"
        ports    = ["22", "80", "443", "5672", "6379", "5000"]
    }

    source_ranges = ["0.0.0.0/0"]
}
