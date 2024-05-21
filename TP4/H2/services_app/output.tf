output "server_rabbitmq_ip" {
  value = google_compute_instance.tp4-h2-services-app
  sensitive = true
}