output "server_rabbitmq_ip" {
  value = google_compute_instance.tp4_h2_services_app[0]
  sensitive = true
}