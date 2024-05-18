variable "credentials_file_path" {
  default = "credentials.json"
}
variable "project_id" {
  default = "sharp-technique-416800"
}
variable "region" {
  default = "us-east1"
}
variable "zone" {
  default = "us-east1-d"
}
variable "num_instances" {
  type = number
  # default = 1
}

variable "metadata_startup_script" {
  type    = string
  default = "script.sh"
}






variable "vpc" {
  type    = string
  default = "unlu-default-vpc2"
}

variable "project-tags" {
  type = map(string)
  default = {
    "key"   = "unlu"
    "magic" = "unlu2"
  }
}
