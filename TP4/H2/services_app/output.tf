output "server_rabbitmq_ip" {
  value = google_compute_instance.tp4_h2_services_app.network_interface.0.access_config.0.nat_ip
}