terraform {
  required_version = ">= 1.5.0"
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
  }
}

variable "cloudflare_api_token" { type = string }
variable "account_id" { type = string }

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

resource "cloudflare_pages_project" "frontend" {
  account_id        = var.account_id
  name              = "quds-radio-ai-web"
  production_branch = "main"

  build_config {
    build_command   = "npm ci && npm run build --workspace @quds/web"
    destination_dir = "apps/web/.next"
  }
}
