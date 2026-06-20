data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_instance" "master" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.medium" # 4GB RAM - Ottimale per Kubernetes Standard
  key_name               = "vockey"    # Chiave pre-creata di AWS Academy
  vpc_security_group_ids = [aws_security_group.k8s_sg.id]

  tags = {
    Name = "k8s-master"
    Role = "master"
  }
}

resource "aws_instance" "worker" {
  count                  = 2
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.medium" # 4GB RAM - Ottimale per Kubernetes Standard
  key_name               = "vockey"    # Chiave pre-creata di AWS Academy
  vpc_security_group_ids = [aws_security_group.k8s_sg.id]

  tags = {
    Name = "k8s-worker-${count.index + 1}"
    Role = "worker"
  }
}