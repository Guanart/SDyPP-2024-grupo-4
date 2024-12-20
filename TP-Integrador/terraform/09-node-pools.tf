# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/google_service_account
resource "google_service_account" "kubernetes" {
  account_id = "kubernetes"
  # lifecycle {
  #   prevent_destroy = true
  # }
}

# https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/container_node_pool
resource "google_container_node_pool" "general" {
  name       = "general"
  cluster    = google_container_cluster.primary.id
  node_count = 1

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 10
  }

  lifecycle {
    ignore_changes = [
      node_count
    ]
  }
  node_config {
    preemptible  = false
    machine_type = "e2-standard-2"
    # disk_size_gb = 15  # Tamaño del disco en GB

    labels = {
      role = "general"
    }

    service_account = google_service_account.kubernetes.email
    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform"
    ]
  }
}

# resource "google_container_node_pool" "spot" {
#   name       = "spot"
#   cluster    = google_container_cluster.primary.id
#   node_count = 1

#   management {
#     auto_repair  = true
#     auto_upgrade = true
#   }

#   autoscaling {
#     min_node_count = 1
#     max_node_count = 2
#   }

#   node_config {
#     preemptible  = true
#     machine_type = "e2-small"
#     disk_size_gb = 10  # Tamaño del disco en GB

#     labels = {
#       team = "devops"
#     }

#     taint {     // ESTO ME PERMITIRÁ INDICAR QUÉ TIPO DE MÁQUINA USAR EN LOS DEPLOYMENTS, agregando un toleration en los workers -> para que usen una SPOT
#       key    = "instance_type"
#       value  = "spot"
#       effect = "NO_SCHEDULE"
#     }

#     service_account = google_service_account.kubernetes.email
#     oauth_scopes = [
#       "https://www.googleapis.com/auth/cloud-platform"
#     ]
#   }
# }
