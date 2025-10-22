output "instance_id" {
  description = "EC2 Instance ID"
  value       = module.ec2.instance_id
}

output "public_ip" {
  description = "EC2 Public IP"
  value       = module.ec2.public_ip
}