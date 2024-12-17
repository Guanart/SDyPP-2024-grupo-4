resource "google_compute_instance" "worker_pool_manager" {
  name         = "worker-pool-manager"
  machine_type = "e2-small"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    git clone https://github.com/Guanart/SDyPP-2024-grupo-4.git
    echo "${var.metadata_startup_script}" > /home/packer/SDyPP-2024-grupo-4/TP-Integrador/docker-compose-worker-pool/.env
    cd /home/packer/SDyPP-2024-grupo-4/TP-Integrador/docker-compose-worker-pool
    docker compose up -d
  EOT
}

variable "metadata_startup_script" {
  type    = string
}