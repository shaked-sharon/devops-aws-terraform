region           = "eu-central-1"
instance_type    = "t3.medium"
key_name         = "builder-key"
private_key_path = "./builder_key.pem"
home_cidr        = "185.23.101.42/32"
open_world_port  = 5001
name_prefix      = "builder"