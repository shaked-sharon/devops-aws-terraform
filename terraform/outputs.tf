output "public_ip" {
  value       = aws_instance.builder.public_ip
  description = "Public IP for EC2 Instance"
}

output "security_group_id" {
  value       = aws_security_group.builder_sg.id
  description = "ID for Security Group"
}

output "private_key_local_path" {
  value       = var.private_key_path
  description = "Local file path for private key. Path only!"
}