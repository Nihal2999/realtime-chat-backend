output "ec2_public_ip" {
  value = aws_eip.app.public_ip
}

output "s3_bucket_name" {
  value = aws_s3_bucket.app.bucket
}

output "vpc_id" {
  value = aws_vpc.main.id
}