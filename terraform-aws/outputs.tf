output "master_ip" {
  value       = aws_instance.master.public_ip
  description = "IP pubblico del Master Node"
}

output "worker_ips" {
  value       = aws_instance.worker[*].public_ip
  description = "IP pubblici dei Worker Node"
}

output "rds_endpoint" {
  value       = split(":", aws_db_instance.postgres.endpoint)[0]
  description = "Indirizzo pulito dell'RDS PostgreSQL"
}

resource "local_file" "ansible_inventory" {
  filename = "${path.module}/../ansible/hosts.ini"
  content  = <<EOT
[control_plane]
master ansible_host=${aws_instance.master.public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/labsuser.pem

[workers]
%{ for idx, ip in aws_instance.worker[*].public_ip ~}
worker-${idx + 1} ansible_host=${ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/labsuser.pem
%{ endfor ~}

[k8s:children]
control_plane
workers
EOT
}