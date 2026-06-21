resource "aws_db_instance" "postgres" {
  identifier           = "taskdb-rds"
  engine               = "postgres"
  engine_version       = "14"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  storage_type         = "gp2" 
  db_name              = "taskdb"
  username             = "postgres" 
  password             = "SuperSecretPassword123!" 
  parameter_group_name = "default.postgres14"
  skip_final_snapshot  = true
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}