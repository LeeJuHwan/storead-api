import pulumi
import pulumi_aws as aws


def generate_policy_document(bucket_name):
    import json

    return json.dumps(
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": ["s3:GetObject"],
                    "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
                }
            ],
        }
    )


def config_aws_simple_storage_service():
    bucket = aws.s3.Bucket(
        "bucket",
        bucket="storead-storage",
        tags={
            "Name": "storead-production-bucket",
            "Environment": "production",
        },
    )

    aws.s3.BucketPublicAccessBlock(
        resource_name="bucket_public_access_block",
        bucket=bucket.id,
        block_public_acls=False,
        block_public_policy=False,
        ignore_public_acls=False,
        restrict_public_buckets=False,
    )

    aws.s3.BucketPolicy(
        resource_name="bucket_public_read_policy", bucket=bucket.id, policy=bucket.id.apply(generate_policy_document)
    )

    pulumi.export("bucket_name", bucket.id)

    return bucket
