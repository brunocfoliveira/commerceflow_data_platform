terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file(var.credentials_file)
}

resource "google_storage_bucket" "raw_data_bucket" {
  name                        = var.gcs_bucket_name
  location                    = var.location
  uniform_bucket_level_access = true

  force_destroy = false

  lifecycle {
    ignore_changes = [
      encryption
    ]
  }
}

resource "google_bigquery_dataset" "raw" {
  dataset_id = var.raw_dataset_id
  location   = var.location
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = var.analytics_dataset_id
  location   = var.location
}

resource "google_service_account" "dbt_service_account" {
  account_id   = var.dbt_service_account_id
  display_name = "CommerceFlow dbt Service Account"
}

resource "google_project_iam_member" "dbt_bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.dbt_service_account.email}"
}

resource "google_project_iam_member" "dbt_bigquery_data_viewer" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.dbt_service_account.email}"
}

resource "google_project_iam_member" "dbt_bigquery_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.dbt_service_account.email}"
}