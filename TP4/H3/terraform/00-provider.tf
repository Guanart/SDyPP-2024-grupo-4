
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=5.26.0"
    }
  }

  backend "gcs" {
    bucket  = var.bucket_name
    prefix  = "terraform/state"
  }

  # required_version = ">= 1.7.5"
}

provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
}
