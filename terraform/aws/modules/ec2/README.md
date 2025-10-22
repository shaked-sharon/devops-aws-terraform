# EC2 module

### Usage
```hcl
module "ec2" {
  source             = "../../modules/ec2"
  instance_type      = "t3.micro"
  subnet_id          = var.subnet_id              # e.g., from a data source
  security_group_ids = [module.security_group.security_group_id]
  key_name           = "devops-key"
  name               = "devops-ec2"
  user_data          = null
}

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| <a name="provider_aws"></a> [aws](#provider\_aws) | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [aws_instance.this](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/instance) | resource |
| [aws_ami.ubuntu](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/ami) | data source |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_common_tags"></a> [common\_tags](#input\_common\_tags) | Extra tags merged with Name | `map(any)` | `{}` | no |
| <a name="input_instance_type"></a> [instance\_type](#input\_instance\_type) | EC2 Instance Type | `string` | `"t3.micro"` | no |
| <a name="input_key_name"></a> [key\_name](#input\_key\_name) | Name of EC2 Key Pair | `string` | `null` | no |
| <a name="input_name"></a> [name](#input\_name) | Instance Name Tag | `string` | `"devops-ec2"` | no |
| <a name="input_security_group_ids"></a> [security\_group\_ids](#input\_security\_group\_ids) | Lists Security Group ID | `list(any)` | n/a | yes |
| <a name="input_subnet_id"></a> [subnet\_id](#input\_subnet\_id) | Subnet ID for instance | `string` | n/a | yes |
| <a name="input_user_data"></a> [user\_data](#input\_user\_data) | Cloud Initialization Script | `string` | `""` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_instance_id"></a> [instance\_id](#output\_instance\_id) | EC2 Instance ID |
| <a name="output_public_ip"></a> [public\_ip](#output\_public\_ip) | Public IP address |
